# -*- coding: utf-8 -*-
#
#    py-ard
#    Copyright (c) 2020 Be The Match operated by National Marrow Donor Program. All Rights Reserved.
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
import gc
import re
from typing import Iterable

from . import db
from .data_repository import generate_ars_mapping, generate_mac_codes, generate_alleles_and_xx_codes, \
    generate_serology_mapping
from .db import is_valid_mac_code, mac_code_to_alleles
from .smart_sort import smart_sort_comparator

HLA_regex = re.compile("^HLA-")


class ARD(object):
    """
    ARD reduction for HLA
    Allows reducing alleles and allele code(MAC) to G, lg and lgx levels.
    """

    def __init__(self, imgt_version: str = 'Latest',
                 remove_invalid: bool = True,
                 data_dir: str = None,
                 refresh_mac: bool = False) -> None:
        """
        ARD will load valid alleles, xx codes and MAC mappings for the given
        version of IMGT database, downloading and generating the database if
        not already present.

        :param imgt_version: IMGT HLA database version
        :param remove_invalid: report only valid alleles for this version
        :param data_dir: directory path to store cached data
        """
        self._remove_invalid = remove_invalid

        # Create a database connection for writing
        self.db_connection = db.create_db_connection(data_dir, imgt_version)

        # Load MAC codes
        generate_mac_codes(self.db_connection, refresh_mac)
        # Load Alleles and XX Codes
        self.valid_alleles, self.xx_codes = generate_alleles_and_xx_codes(self.db_connection, imgt_version)
        # Load ARS mappings
        self.dup_g, self._G, self._lg, self._lgx = generate_ars_mapping(self.db_connection, imgt_version)
        # Load Serology mappings
        generate_serology_mapping(self.db_connection, imgt_version)

        # Close the current read-write db connection
        self.db_connection.close()

        # reference data is read-only and can be frozen
        gc.freeze()

        # Re-open the connection in read-only mode as we're not updating it anymore
        self.db_connection = db.create_db_connection(data_dir, imgt_version, ro=True)

    def __del__(self):
        """
        Close the db connection, when ARD instance goes away
        :return:
        """
        self.db_connection.close()

    @functools.lru_cache(maxsize=1000)
    def redux(self, allele: str, ars_type: str) -> str:
        """
        Does ARS reduction with allele and ARS type

        :param allele: An HLA allele.
        :type: str
        :param ars_type: The ARS ars_type.
        :type: str
        :return: ARS reduced allele
        :rtype: str
        """

        # deal with leading 'HLA-'
        if HLA_regex.search(allele):
            hla, allele_name = allele.split("-")
            redux_allele = self.redux(allele_name, ars_type)
            if redux_allele:
                return "HLA-" + redux_allele
            else:
                return redux_allele

        # Alleles ending with P or G are valid_alleles
        if allele.endswith(('P', 'G')):
            allele = allele[:-1]

        if ars_type == "G" and allele in self._G:
            if allele in self.dup_g:
                return self.dup_g[allele]
            else:
                return self._G[allele]
        elif ars_type == "lg":
            if allele in self._lg:
                return self._lg[allele]
            else:
                # for 'lg' when allele is not in G group,
                # return allele with only first 2 field
                return ':'.join(allele.split(':')[0:2]) + 'g'
        elif ars_type == "lgx":
            if allele in self._lgx:
                return self._lgx[allele]
            else:
                # for 'lgx' when allele is not in G group,
                # return allele with only first 2 field
                return ':'.join(allele.split(':')[0:2])
        else:
            if self._remove_invalid:
                if self._is_valid_allele(allele):
                    return allele
                else:
                    return ''
            else:
                return allele

    @functools.lru_cache(maxsize=1000)
    def redux_gl(self, glstring: str, redux_type: str) -> str:
        """
        Does ARS reduction with gl string and ARS type

        :param glstring: A GL String
        :type: str
        :param redux_type: The ARS ars_type.
        :type: str
        :return: ARS reduced allele
        :rtype: str
        """

        if not self.isvalid_gl(glstring):
            return ""

        if re.search(r"\^", glstring):
            return "^".join(sorted(set([self.redux_gl(a, redux_type) for a in glstring.split("^")]),
                                   key=functools.cmp_to_key(smart_sort_comparator)))

        if re.search(r"\|", glstring):
            return "|".join(sorted(set([self.redux_gl(a, redux_type) for a in glstring.split("|")]),
                                   key=functools.cmp_to_key(smart_sort_comparator)))

        if re.search(r"\+", glstring):
            return "+".join(sorted([self.redux_gl(a, redux_type) for a in glstring.split("+")],
                                   key=functools.cmp_to_key(smart_sort_comparator)))

        if re.search("~", glstring):
            return "~".join([self.redux_gl(a, redux_type) for a in glstring.split("~")])

        if re.search("/", glstring):
            return "/".join(sorted(set([self.redux_gl(a, redux_type) for a in glstring.split("/")]),
                                   key=functools.cmp_to_key(smart_sort_comparator)))

        # Handle Serology
        if self.is_serology(glstring):
            alleles = self._get_alleles_from_serology(glstring)
            return self.redux_gl("/".join(alleles), redux_type)

        loc_allele = glstring.split(":")
        loc_antigen, code = loc_allele[0], loc_allele[1]

        # Handle XX codes
        if self.is_mac(glstring) and code == "XX" and loc_antigen in self.xx_codes:
            return self.redux_gl("/".join(self.xx_codes[loc_antigen]), redux_type)

        # Handle MAC
        if self.is_mac(glstring) and is_valid_mac_code(self.db_connection, code):
            if HLA_regex.search(glstring):
                # Remove HLA- prefix
                allele_name = glstring.split("-")[1]
                loc_antigen, code = allele_name.split(":")
                alleles = self._get_alleles(code, loc_antigen)
                alleles = ["HLA-" + a for a in alleles]
            else:
                alleles = self._get_alleles(code, loc_antigen)
            return self.redux_gl("/".join(alleles), redux_type)

        return self.redux(glstring, redux_type)

    @staticmethod
    def is_serology(allele: str) -> bool:
        """
        A serology has the locus name (first 2 letters for DRB1, DRB3, DQB1, DQA1, DPB1 and DPA1)
        of the allele followed by numerical antigen.

        :param allele: The allele to test for serology
        :return: True if serology
        """
        if '*' in allele or ':' in allele:
            return False

        locus = allele[0:2]
        if locus in ['DR', 'DP', 'DQ']:
            antigen = allele[2:]
            return antigen.isdigit()

        locus = allele[0:1]
        if locus in ['A', 'B', 'C', 'D']:
            antigen = allele[1:]
            return antigen.isdigit()

        return False

    @staticmethod
    def is_mac(gl: str) -> bool:
        """
        MAC has there are non-digit characters after the : character,
        then it's a MAC.
        :param gl: glstring to test if it has a MAC code
        :return: True if MAC
        """
        return re.search(r":\D+", gl) is not None

    def _is_valid_allele(self, allele):
        """
        Test if allele is valid in the current imgt database
        :param allele: Allele to test
        :return: bool to indicate if allele is valid
        """
        if self._remove_invalid:
            return allele in self.valid_alleles
        return True

    def _get_alleles(self, code, locus_antigen) -> Iterable[str]:
        """
        Look up allele code in database and generate alleles
        :param code: allele code to look up
        :param locus_antigen: locus name for alleles
        :return: valid alleles corresponding to allele code
        """
        alleles = mac_code_to_alleles(self.db_connection, code)

        # It's an allelic expansion if any of the alleles have a `:`
        # else it's a group expansion
        is_allelic_expansion = any([':' in allele for allele in alleles])
        if is_allelic_expansion:
            locus = locus_antigen.split('*')[0] # Just keep the locus name
            alleles = [f'{locus}*{a}' for a in alleles]
        else:
            alleles = [f'{locus_antigen}:{a}' for a in alleles]

        if self._remove_invalid:
            return filter(self._is_valid_allele, alleles)
        else:
            return alleles

    def _get_alleles_from_serology(self, serology) -> Iterable[str]:
        alleles = db.serology_to_alleles(self.db_connection, serology)
        if self._remove_invalid:
            return filter(self._is_valid_allele, alleles)
        else:
            return alleles

    def isvalid(self, allele: str) -> bool:
        """
        Determines validity of an allele

        :param allele: An HLA allele.
        :type: str
        :return: allele or empty
        :rtype: bool
        """
        if allele == '':
            return False
        if not self.is_mac(allele) and not self.is_serology(allele):
            # Alleles ending with P or G are valid_alleles
            if allele.endswith(('P', 'G')):
                # remove the last character
                allele = allele[:-1]
            # validate allele without the 'HLA-' prefix
            if HLA_regex.search(allele):
                # remove 'HLA-' prefix
                allele = allele[4:]
            return self._is_valid_allele(allele)
        return True

    def isvalid_gl(self, glstring: str) -> bool:
        """
        Determines validity of glstring

        :param glstring
        :type: str
        :return: result
        :rtype: bool
        """

        if re.search(r"\^", glstring):
            return all(map(self.isvalid_gl, glstring.split("^")))
        if re.search(r"\|", glstring):
            return all(map(self.isvalid_gl, glstring.split("|")))
        if re.search(r"\+", glstring):
            return all(map(self.isvalid_gl, glstring.split("+")))
        if re.search("~", glstring):
            return all(map(self.isvalid_gl, glstring.split("~")))
        if re.search("/", glstring):
            return all(map(self.isvalid_gl, glstring.split("/")))

        # what falls through here is an allele
        return self.isvalid(glstring)

    def mac_toG(self, allele: str) -> str:
        """
        Does ARS reduction with allele and ARS type

        :param allele: An HLA allele.
        :type: str
        :return: ARS reduced allele
        :rtype: str
        """
        locus_antigen, code = allele.split(":")
        if HLA_regex.search(allele):
            locus_antigen = locus_antigen.split("-")[1] # Remove HLA- prefix
        if is_valid_mac_code(self.db_connection, code):
            alleles = self._get_alleles(code, locus_antigen)
            group = [self.toG(a) for a in alleles]
            if "X" in group:
                return ''
            else:
                return "/".join(group)
        else:
            return ''

    def toG(self, allele: str) -> str:
        """
        Does ARS reduction to the G group level

        :param allele: An HLA allele.
        :type: str
        :return: ARS G reduced allele
        :rtype: str
        """
        if allele in self._G:
            if allele in self.dup_g:
                return self.dup_g[allele]
            else:
                return self._G[allele]
        else:
            return "X"

    def expand_mac(self, mac_code: str):
        """
        Expands mac codes

        :param mac_code: An HLA allele.
        :type: str
        :return: List
        :rtype: List
        """
        locus_antigen, code = mac_code.split(":")
        if is_valid_mac_code(self.db_connection, code):
            if HLA_regex.search(mac_code):
                locus_antigen = locus_antigen.split("-")[1] # Remove HLA- prefix
                return ['HLA-' + a for a in self._get_alleles(code, locus_antigen)]
            else:
                return list(self._get_alleles(code, locus_antigen))

        return ''
