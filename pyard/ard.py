# -*- coding: utf-8 -*-
#
#    py-ard
#    Copyright (c) 2023 Be The Match operated by National Marrow Donor Program.
#    All Rights Reserved.
#
#    This library is free software; you can redistribute it and/or modify it
#    under the terms of the GNU Lesser General Public License as published
#    by the Free Software Foundation; either version 3 of the License, or (at
#    your option) any later version.
#
#    This library is distributed in the hope that it will be useful, but WITHOUT
#    ANY WARRANTY; with out even the implied warranty of MERCHANTABILITY or
#    FITNESS FOR A PARTICULAR PURPOSE.  See the GNU Lesser General Public
#    License for more details.
#
#    You should have received a copy of the GNU Lesser General Public License
#    along with this library;  if not, write to the Free Software Foundation,
#    Inc., 59 Temple Place, Suite 330, Boston, MA 02111-1307  USA.
#
#    > http://www.fsf.org/licensing/licenses/lgpl.html
#    > http://www.opensource.org/licenses/lgpl-license.php
#
import functools
import re
import sys
from typing import Iterable, List

from . import broad_splits, smart_sort
from . import data_repository as dr
from . import db
from .exceptions import InvalidAlleleError, InvalidMACError, InvalidTypingError
from .misc import (
    get_n_field_allele,
    get_2field_allele,
    validate_reduction_type,
)
from .constants import (
    HLA_regex,
    VALID_REDUCTION_TYPES,
    expression_chars,
    DEFAULT_CACHE_SIZE,
)

default_config = {
    "reduce_serology": True,
    "reduce_v2": True,
    "reduce_3field": True,
    "reduce_P": True,
    "reduce_XX": True,
    "reduce_MAC": True,
    "reduce_shortnull": True,
    "ping": False,
    "map_drb345_to_drbx": True,
    "verbose_log": True,
}


# Typing information


class ARD(object):
    """
    ARD reduction for HLA
    Allows reducing alleles, allele code(MAC), Serology to
    G, lg, lgx, W, exon and U2 levels.
    """

    def __init__(
        self,
        imgt_version: str = "Latest",
        data_dir: str = None,
        load_mac: bool = True,
        max_cache_size: int = DEFAULT_CACHE_SIZE,
        config: dict = None,
    ):
        """
        ARD will load valid alleles, xx codes and MAC mappings for the given
        version of IMGT database, downloading and generating the database if
        not already present.

        :param imgt_version: IMGT HLA database version
        :param data_dir: directory path to store cached data
        :param config: directory of configuration options
        """
        self._data_dir = data_dir
        self._config = default_config.copy()
        if config:
            self._config.update(config)

        # Create a database connection for writing
        self.db_connection, _ = db.create_db_connection(data_dir, imgt_version)

        # Load ARD mappings
        self.ars_mappings = dr.generate_ard_mapping(self.db_connection, imgt_version)
        # Load Alleles and XX Codes
        (
            self.code_mappings,
            self.allele_group,
        ) = dr.generate_alleles_and_xx_codes_and_who(
            self.db_connection, imgt_version, self.ars_mappings
        )

        # Generate short nulls from WHO mapping
        self.shortnulls = dr.generate_short_nulls(
            self.db_connection, self.code_mappings.who_group
        )

        # Load Serology mappings
        broad_splits.broad_splits_ser_mapping = (
            dr.generate_serology_broad_split_mapping(self.db_connection, imgt_version)
        )
        dr.generate_serology_mapping(self.db_connection, imgt_version)
        # Load V2 to V3 mappings
        dr.generate_v2_to_v3_mapping(self.db_connection, imgt_version)
        # Save IMGT database version
        dr.set_db_version(self.db_connection, imgt_version)
        # Load MAC codes
        dr.generate_mac_codes(self.db_connection, refresh_mac=False, load_mac=load_mac)
        # Load CIWD mapping
        dr.generate_cwd_mapping(self.db_connection)

        # Close the current read-write db connection
        self.db_connection.close()

        # Adjust the cache for redux
        if max_cache_size != DEFAULT_CACHE_SIZE:
            self._redux_allele = functools.lru_cache(maxsize=max_cache_size)(
                self._redux_allele
            )
            self.redux = functools.lru_cache(maxsize=max_cache_size)(self.redux)
            self.is_mac = functools.lru_cache(maxsize=max_cache_size)(self.is_mac)
            self.smart_sort_comparator = functools.lru_cache(maxsize=max_cache_size)(
                smart_sort.smart_sort_comparator
            )
        else:
            self.smart_sort_comparator = smart_sort.smart_sort_comparator

        # reference data is read-only and can be frozen
        # Works only for Python >= 3.9
        if sys.version_info.major == 3 and sys.version_info.minor >= 9:
            import gc

            gc.freeze()

        # Re-open the connection in read-only mode as we're not updating it anymore
        self.db_connection, _ = db.create_db_connection(data_dir, imgt_version, ro=True)

    def __del__(self):
        """
        Close the db connection, when ARD instance goes away
        :return:
        """
        if hasattr(self, "db_connection") and self.db_connection:
            self.db_connection.close()

    @functools.lru_cache(maxsize=DEFAULT_CACHE_SIZE)
    def _redux_allele(
        self, allele: str, redux_type: VALID_REDUCTION_TYPES, re_ping=True
    ) -> str:
        """
        Does ARD reduction with allele and reduction type

        :param allele: An HLA allele.
        :type: str
        :param redux_type: reduction type.
        :type: str
        :return: reduced allele
        :rtype: str
        """

        validate_reduction_type(redux_type)

        # deal with leading 'HLA-'
        if HLA_regex.search(allele):
            hla, allele_name = allele.split("-")
            redux_allele = self._redux_allele(allele_name, redux_type)
            if redux_allele:
                return "HLA-" + redux_allele
            else:
                return redux_allele

        # g_group maps alleles to their g_group
        # note: this includes mappings for shortened version of alleles
        # C*12:02:02:01 => C*12:02:01G
        # C*12:02:02    => C*12:02:01G
        # C*12:02       => C*12:02:01G

        if allele.endswith(("P", "G")):
            if redux_type in ["lg", "lgx", "G"]:
                allele = allele[:-1]
        if self._config["ping"] and re_ping:
            if redux_type in ("lg", "lgx", "U2"):
                if allele in self.ars_mappings.p_not_g:
                    return self.ars_mappings.p_not_g[allele]
                else:
                    return self._redux_allele(allele, redux_type, False)

        if redux_type == "G" and allele in self.ars_mappings.g_group:
            if allele in self.ars_mappings.dup_g:
                return self.ars_mappings.dup_g[allele]
            else:
                return self.ars_mappings.g_group[allele]
        elif redux_type == "P" and allele in self.ars_mappings.p_group:
            return self.ars_mappings.p_group[allele]
        elif redux_type in ["lgx", "lg"]:
            if allele in self.ars_mappings.dup_lgx:
                redux_allele = self.ars_mappings.dup_lgx[allele]
            elif allele in self.ars_mappings.lgx_group:
                redux_allele = self.ars_mappings.lgx_group[allele]
            else:
                # for 'lgx' or 'lg' mode when allele is not in G group,
                # return allele with only first 2 field
                redux_allele = ":".join(allele.split(":")[0:2])
            if redux_type == "lg":
                # lg mode has g appended with lgx reduction
                return redux_allele + "g"
            return redux_allele
        elif redux_type == "W":
            # new redux_type which is full WHO expansion
            if self._is_who_allele(allele):
                return allele
            if allele in self.code_mappings.who_group:
                return self.redux(
                    "/".join(self.code_mappings.who_group[allele]), redux_type
                )
            else:
                return allele
        elif redux_type == "exon":
            if allele in self.ars_mappings.exon_group:
                exon_group_allele = self.ars_mappings.exon_group[allele]
                # Check if the 3 field exon allele has a 4 field alleles
                # that all have the same expression characters
                last_char = allele[-1]
                if last_char in expression_chars:
                    exon_short_null_allele = exon_group_allele + last_char
                    if self.is_shortnull(exon_short_null_allele):
                        return exon_short_null_allele

                return exon_group_allele
            else:
                # for 'exon' return allele with only first 3 fields
                return ":".join(allele.split(":")[0:3])
        elif redux_type == "U2":
            allele_fields = allele.split(":")
            # If resolved out to second field leave alone
            if len(allele_fields) == 2:
                return allele
            # If the 2 field reduction is unambiguous, reduce to 2 field level
            allele_2_fields = get_n_field_allele(allele, 2, preserve_expression=True)
            if self._is_valid_allele(allele_2_fields):
                return allele_2_fields
            else:
                # If ambiguous, reduce to G group level
                return self._redux_allele(allele, "lgx")
        else:
            # Make this an explicit lookup to the g_group or p_group table
            # for stringent validation
            if allele.endswith("P"):
                if allele in self.ars_mappings.p_group.values():
                    return allele
            elif allele.endswith("G"):
                if allele in self.ars_mappings.g_group.values():
                    return allele

            if self._is_valid_allele(allele):
                return allele
            else:
                raise InvalidAlleleError(f"{allele} is an invalid allele.")

    def _sorted_unique_gl(self, gls: List[str], delim: str) -> str:
        """
        Make a list of sorted unique GL Strings separated by delim.
        As the list may itself contains elements that are separated by the
        delimiter, split the elements first and then make them unique.

        :param gls: List of gl strings that need to be joined by delim
        :param delim: Delimiter of concern
        :return: a GL string sorted and made of unique GL
        """
        if delim == "~":
            # No need to sort
            return delim.join(gls)

        if delim == "+":
            # No need to make unique. eg. homozygous cases are valid for SLUGs
            return delim.join(
                sorted(gls, key=functools.cmp_to_key(self.smart_sort_comparator))
            )

        # generate a unique list over a delimiter
        # e.g. [A, A/B] => [ A, B ] for / delimiter
        all_gls = []
        for gl in gls:
            all_gls += gl.split(delim)
        unique_gls = set(all_gls)
        return delim.join(
            sorted(unique_gls, key=functools.cmp_to_key(self.smart_sort_comparator))
        )

    @functools.lru_cache(maxsize=DEFAULT_CACHE_SIZE)
    def redux(self, glstring: str, redux_type: VALID_REDUCTION_TYPES) -> str:
        """
        Does ARD reduction with gl string and reduction type

        :param glstring: A GL String
        :type: str
        :param redux_type: The reduction_type.
        :type: str
        :return: reduced allele
        :rtype: str
        """

        validate_reduction_type(redux_type)

        self.validate(glstring)

        if "^" in glstring:
            return self._sorted_unique_gl(
                [self.redux(a, redux_type) for a in glstring.split("^")], "^"
            )

        if "|" in glstring:
            return self._sorted_unique_gl(
                [self.redux(a, redux_type) for a in glstring.split("|")], "|"
            )

        if "+" in glstring:
            return self._sorted_unique_gl(
                [self.redux(a, redux_type) for a in glstring.split("+")], "+"
            )

        if "~" in glstring:
            return self._sorted_unique_gl(
                [self.redux(a, redux_type) for a in glstring.split("~")], "~"
            )

        if "/" in glstring:
            return self._sorted_unique_gl(
                [self.redux(a, redux_type) for a in glstring.split("/")], "/"
            )

        # Handle V2 to V3 mapping
        if self.is_v2(glstring):
            glstring = self._map_v2_to_v3(glstring)
            return self.redux(glstring, redux_type)

        # Handle Serology
        if self._config["reduce_serology"] and self.is_serology(glstring):
            alleles = self._get_alleles_from_serology(glstring)
            return self.redux("/".join(alleles), redux_type)

        if ":" in glstring:
            loc_allele = glstring.split(":")
            loc_antigen, code = loc_allele[0], loc_allele[1]
        else:
            raise InvalidTypingError(
                f"{glstring} is not a valid V2 or Serology typing."
            )

        # Handle XX codes
        if self._config["reduce_XX"]:
            is_hla_prefix = HLA_regex.search(loc_antigen)
            if is_hla_prefix:
                loc_antigen = loc_antigen.split("-")[1]
            if self.is_XX(glstring, loc_antigen, code):
                if is_hla_prefix:
                    reduced_alleles = self.redux(
                        "/".join(self.code_mappings.xx_codes[loc_antigen]), redux_type
                    )
                    return "/".join(["HLA-" + a for a in reduced_alleles.split("/")])
                else:
                    return self.redux(
                        "/".join(self.code_mappings.xx_codes[loc_antigen]), redux_type
                    )

        # Handle MAC
        if self._config["reduce_MAC"] and self.is_mac(glstring):
            if db.is_valid_mac_code(self.db_connection, code):
                if HLA_regex.search(glstring):
                    # Remove HLA- prefix
                    allele_name = glstring.split("-")[1]
                    loc_antigen, code = allele_name.split(":")
                    alleles = self._get_alleles(code, loc_antigen)
                    alleles = ["HLA-" + a for a in alleles]
                else:
                    alleles = self._get_alleles(code, loc_antigen)
                return self.redux("/".join(alleles), redux_type)
            else:
                raise InvalidMACError(f"{glstring} is an invalid MAC.")

        # Handle short nulls
        if self._config["reduce_shortnull"] and self.is_shortnull(glstring):
            return self.redux("/".join(self.shortnulls[glstring]), redux_type)

        return self._redux_allele(glstring, redux_type)

    def validate(self, glstring):
        """
        Validates GL String
        Raise an exception if not valid.

        :param glstring: GL String to validate
        :return: boolean indicating success
        """
        try:
            return self._is_valid_gl(glstring)
        except InvalidAlleleError as e:
            raise InvalidTypingError(
                f"{glstring} is not valid GL String. \n {e.message}", e
            ) from None

    def is_XX(self, glstring: str, loc_antigen: str = None, code: str = None) -> bool:
        if loc_antigen is None or code is None:
            if ":" in glstring:
                loc_allele = glstring.split(":")
                loc_antigen, code = loc_allele[0], loc_allele[1]
            else:
                return False
        return code == "XX" and loc_antigen in self.code_mappings.xx_codes

    def is_serology(self, allele: str) -> bool:
        """

        Strict validation of serology:
        Does not have * or : in serology.
        If it exists in the database, it's serology otherwise it's not serology.

        A serology has the locus name (first 2 letters for DRB1, DQB1)
        of the allele followed by numerical antigen.
        Cw is the serological designation for HLA-C

        :param allele: The allele to test for serology
        :return: True if serology
        """
        if "*" in allele or ":" in allele:
            return False

        return db.is_valid_serology(self.db_connection, allele)

    @functools.lru_cache(maxsize=DEFAULT_CACHE_SIZE)
    def is_mac(self, allele: str) -> bool:
        """
        MAC has non-digit characters after the : character.

        Strict validation of MAC.
        The allele is a MAC code if it exists in the database.
        Not all strings are MACs e.g. ":THISISNOTAMAC"

        :param allele: test if it is a MAC code
        :return: True if MAC
        """
        if ":" in allele:
            code = allele.split(":")[1]
            return db.is_valid_mac_code(self.db_connection, code)
        return False

    def is_v2(self, allele: str) -> bool:
        """
        Version 2 of the nomenclature is a single field.
        It does not have any ':' field separator.
            Eg: A*0104
        Exceptions:
            Not all strings with "*" but not ":" are v2 nomenclature
            DRB3*NNNN is not v2 allele
        Stricter Check:
            if the conversion of v2 to v3 is the same, then
            it's not a V2 typing
        Set 'reduce_v2' option to False to skip the check for V2.

        :param allele: Possible allele
        :return: Is the allele in V2 nomenclature
        """
        return (
            self._config["reduce_v2"]
            and "*" in allele
            and ":" not in allele
            and allele != self._map_v2_to_v3(allele)
        )

    def _is_who_allele(self, allele):
        """
        Test if allele is a WHO allele in the current imgt database
        :param allele: Allele to test
        :return: bool to indicate if allele is valid
        """
        return allele in self.allele_group.who_alleles

    def _is_valid_allele(self, allele):
        """
        Test if allele is valid in the current imgt database
        :param allele: Allele to test
        :return: bool to indicate if allele is valid
        """
        return allele in self.allele_group.alleles

    def is_shortnull(self, allele):
        """
        Test if allele is valid in list of shortnull alleles and
        the reduce_shortnull is configured to True (WMDA rules)
        :param allele: Allele to test
        :return: bool to indicate if allele is valid
        """
        return allele in self.shortnulls and self._config["reduce_shortnull"]

    def is_exp_allele(self, allele):
        """
        Test if allele is valid as a shortening (WHO rules)
        :param allele: Allele to test
        :return: bool to indicate if allele is valid
        """
        return allele in self.allele_group.exp_alleles

    def _get_alleles(self, code, locus_antigen) -> Iterable[str]:
        """
        Look up allele code in database and generate alleles
        :param code: allele code to look up
        :param locus_antigen: locus name for alleles
        :return: valid alleles corresponding to allele code
        """
        alleles = db.mac_code_to_alleles(self.db_connection, code)

        # It's an allelic expansion if any of the alleles have a `:`
        # else it's a group expansion
        is_allelic_expansion = any([":" in allele for allele in alleles])
        if is_allelic_expansion:
            locus = locus_antigen.split("*")[0]  # Just keep the locus name
            alleles = [f"{locus}*{a}" for a in alleles]
        else:
            alleles = [f"{locus_antigen}:{a}" for a in alleles]

        return list(filter(self._is_valid_allele, alleles))

    def _get_alleles_from_serology(self, serology) -> Iterable[str]:
        alleles = db.serology_to_alleles(self.db_connection, serology)
        return filter(self._is_valid_allele, alleles)

    @staticmethod
    def _combine_with_colon(digits_field):
        num_of_digits = len(digits_field)
        return ":".join(digits_field[i : i + 2] for i in range(0, num_of_digits, 2))

    def _predict_v3(self, v2_allele: str) -> str:
        """
        Use heuristic to predict V3 from V2

        :param v2_allele: Allele in V2 format
        :return: V3 format of V2 allele
        """
        # Separate out the locus and the allele name part
        locus, allele_name = v2_allele.split("*")
        # Separate out the numeric and non-numeric components
        components = re.findall(r"^(\d+)(.*)", allele_name)
        if not components:
            return v2_allele
        digits_field, non_digits_field = components.pop()
        # final_allele is the result of the transformation
        final_allele = digits_field
        num_of_digits = len(digits_field)
        if num_of_digits == 1:
            return v2_allele
        if num_of_digits > 2:
            if (
                locus.startswith("DP") and num_of_digits == 5
            ):  # covers DPs with 5 digits
                final_allele = (
                    digits_field[:3] + ":" + (digits_field[3:]) + non_digits_field
                )
            elif num_of_digits % 2 == 0:  # covers digits with 2, 4, 6, 8
                final_allele = self._combine_with_colon(digits_field) + non_digits_field
            else:
                final_allele = (
                    digits_field[:2] + ":" + (digits_field[2:]) + non_digits_field
                )
        else:
            if non_digits_field:
                final_allele = digits_field + ":" + non_digits_field
        return locus + "*" + final_allele

    def _map_v2_to_v3(self, v2_allele):
        """
        Get V3 version of V2 versioned allele
        :param v2_allele: V2 versioned allele
        :return: V3 versioned allele
        """
        # Check if it's in the exception case mapping
        v3_allele = db.v2_to_v3_allele(self.db_connection, v2_allele)
        if not v3_allele:
            # Try and predict V3
            v3_allele = self._predict_v3(v2_allele)
        return v3_allele

    def _is_valid(self, allele: str) -> bool:
        """
        Determines validity of an allele in various forms

        :param allele: An HLA allele.
        :type: str
        :return: allele or empty
        :rtype: bool
        """
        if allele == "" or allele.endswith("*"):
            return False

        # validate allele without the 'HLA-' prefix
        if HLA_regex.search(allele):
            # remove 'HLA-' prefix
            allele = allele[4:]

        if "*" in allele:
            alphanum_allele = allele.replace("*", "").replace(":", "")
            if not alphanum_allele.isalnum():
                return False

        if (
            not self.is_mac(allele)
            and not self.is_XX(allele)
            and not self.is_serology(allele)
            and not self.is_v2(allele)
            and not self.is_shortnull(allele)
        ):
            # Alleles ending with P or G are valid_alleles
            if allele.endswith(("P", "G")):
                # remove the last character
                allele = allele[:-1]
                if self._is_valid_allele(allele):
                    return True
                else:
                    allele = get_2field_allele(allele)
                    if self._is_valid_allele(allele):
                        return True

            return self._is_valid_allele(allele)
        return True

    def _is_valid_gl(self, glstring: str) -> bool:
        """
        Determines validity of glstring

        :param glstring
        :type: str
        :return: result
        :rtype: bool
        """

        if "^" in glstring:
            return all(map(self._is_valid_gl, glstring.split("^")))
        if "|" in glstring:
            return all(map(self._is_valid_gl, glstring.split("|")))
        if "+" in glstring:
            return all(map(self._is_valid_gl, glstring.split("+")))
        if "~" in glstring:
            return all(map(self._is_valid_gl, glstring.split("~")))
        if "/" in glstring:
            return all(map(self._is_valid_gl, glstring.split("/")))

        # what falls through here is an allele
        is_valid_allele = self._is_valid(glstring)
        if not is_valid_allele:
            raise InvalidAlleleError(f"{glstring} is not a valid Allele")
        return is_valid_allele

    def expand_mac(self, mac_code: str):
        """
        Expands MAC code into its

        :param mac_code: A MAC code
        :type: str
        :return: GL String of expanded alleles
        :rtype: str
        """
        locus_antigen, code = mac_code.split(":")
        if db.is_valid_mac_code(self.db_connection, code):
            if HLA_regex.search(mac_code):
                locus_antigen = locus_antigen.split("-")[1]  # Remove HLA- prefix
                return "/".join(
                    ["HLA-" + a for a in self._get_alleles(code, locus_antigen)]
                )
            else:
                return "/".join(self._get_alleles(code, locus_antigen))

        raise InvalidMACError(f"{mac_code} is an invalid MAC.")

    def lookup_mac(self, allelelist_gl: str):
        """
        Finds a MAC code corresponding to

        :param allelelist_gl: Allelelist GL String
        :type: str
        :return: MAC code
        :rtype: str
        """
        alleles = allelelist_gl.split("/")
        allele_fields = [allele.split("*")[1] for allele in alleles]
        antigen_groups = sorted({allele.split(":")[0] for allele in allele_fields})
        if len(antigen_groups) == 1:
            mac_expansion = "/".join(
                sorted({allele.split(":")[1] for allele in allele_fields})
            )
            # See if the 2nd field lists is in the database
            mac_code = db.alleles_to_mac_code(self.db_connection, mac_expansion)
            if mac_code:
                locus = allelelist_gl.split("*")[0]
                return f"{locus}*{antigen_groups[0]}:{mac_code}"

        # Try the list of first_field:second_field combinations
        mac_expansion = "/".join(sorted(allele_fields))
        mac_code = db.alleles_to_mac_code(self.db_connection, mac_expansion)

        if mac_code:
            locus = allelelist_gl.split("*")[0]
            return f"{locus}*{antigen_groups[0]}:{mac_code}"

        raise InvalidMACError(f"{allelelist_gl} does not have a MAC.")

    def cwd_redux(self, allele_list_gl):
        lgx_redux = self.redux(allele_list_gl, "lgx")
        locus = allele_list_gl.split("*")[0]
        if HLA_regex.search(locus):
            locus = locus.split("-")[1]
        ciwd_for_locus = db.load_cwd(self.db_connection, locus)
        lgx_redux_alleles = set(lgx_redux.split("/"))
        alleles_in_ciwd = ciwd_for_locus.intersection(lgx_redux_alleles)
        sorted_alleles = sorted(
            alleles_in_ciwd, key=functools.cmp_to_key(self.smart_sort_comparator)
        )
        return "/".join(sorted_alleles)

    def v2_to_v3(self, v2_allele) -> str:
        """
        Convert Version 2 Allele Name to Version 3 Allele Name

        :param v2_allele: Version 2 Allele Name
        :return: Version 3 Allele Name
        """
        if self.is_v2(v2_allele):
            return self._map_v2_to_v3(v2_allele)
        return v2_allele

    def refresh_mac_codes(self) -> None:
        """
        Refreshes MAC code for the current IMGT db version.
        :return: None
        """
        dr.generate_mac_codes(self.db_connection, refresh_mac=True)

    def get_db_version(self) -> str:
        """
        Get the IMGT DB Version Number
        @return:
        """
        return dr.get_db_version(self.db_connection)
