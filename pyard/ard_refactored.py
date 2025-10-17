# -*- coding: utf-8 -*-

import functools
import sys
from typing import Union, List

from . import data_repository as dr
from . import db
from . import smart_sort
from .constants import (
    HLA_regex,
    DEFAULT_CACHE_SIZE,
    G_GROUP_LOCI,
    VALID_REDUCTION_TYPE,
)
from .exceptions import InvalidMACError, InvalidTypingError
from .handlers import (
    AlleleReducer,
    GLStringProcessor,
    MACHandler,
    SerologyHandler,
    V2Handler,
    XXHandler,
    ShortNullHandler,
)
from .misc import get_2field_allele, is_2_field_allele
from .serology import SerologyMapping

default_config = {
    "reduce_serology": True,
    "reduce_v2": True,
    "reduce_3field": True,
    "reduce_P": True,
    "reduce_XX": True,
    "reduce_MAC": True,
    "reduce_shortnull": True,
    "ping": True,
    "verbose_log": False,
    "ARS_as_lg": False,
    "strict": True,
    "ignore_allele_with_suffixes": (),
}


class ARD(object):
    """
    ARD reduction for HLA - Refactored with specialized handlers
    """

    def __init__(
        self,
        imgt_version: str = "Latest",
        data_dir: str = None,
        load_mac: bool = True,
        max_cache_size: int = DEFAULT_CACHE_SIZE,
        config: dict = None,
    ):
        self._data_dir = data_dir
        self._config = default_config.copy()
        if config:
            self._config.update(config)

        # Initialize specialized handlers
        self._initialize_handlers()

        # Setup caching
        self._setup_caching(max_cache_size)

        # Initialize database and mappings
        self._initialize_database(imgt_version, load_mac)

        # Freeze reference data for Python >= 3.9
        self._freeze_reference_data()

        # Reopen connection in read-only mode
        self.db_connection, _ = db.create_db_connection(data_dir, imgt_version, ro=True)

    def _initialize_database(self, imgt_version: str, load_mac: bool):
        """Initialize database connection and load all mappings"""
        self.db_connection, _ = db.create_db_connection(self._data_dir, imgt_version)

        # Load ARD mappings
        self.ars_mappings = dr.generate_ard_mapping(self.db_connection, imgt_version)

        # Load Alleles and XX Codes
        (
            self.code_mappings,
            self.allele_group,
        ) = dr.generate_alleles_and_xx_codes_and_who(
            self.db_connection, imgt_version, self.ars_mappings
        )

        # Generate short nulls
        self.shortnulls = dr.generate_short_nulls(
            self.db_connection, self.code_mappings.who_group
        )

        # Load Serology mappings
        broad_splits_mapping, associated_mapping = dr.generate_broad_splits_mapping(
            self.db_connection, imgt_version
        )
        self.serology_mapping = SerologyMapping(
            broad_splits_mapping, associated_mapping
        )
        dr.generate_serology_mapping(
            self.db_connection, imgt_version, self.serology_mapping, self._redux_allele
        )
        self.valid_serology_set = SerologyMapping.get_valid_serology_names()

        # Load other mappings
        dr.generate_v2_to_v3_mapping(self.db_connection, imgt_version)
        dr.set_db_version(self.db_connection, imgt_version)
        dr.generate_mac_codes(self.db_connection, refresh_mac=False, load_mac=load_mac)
        dr.generate_cwd_mapping(self.db_connection)

        self.db_connection.close()

    def _initialize_handlers(self):
        """Initialize all specialized handlers"""
        self.allele_reducer = AlleleReducer(self)
        self.gl_processor = GLStringProcessor(self)
        self.mac_handler = MACHandler(self)
        self.serology_handler = SerologyHandler(self)
        self.v2_handler = V2Handler(self)
        self.xx_handler = XXHandler(self)
        self.shortnull_handler = ShortNullHandler(self)

    def _setup_caching(self, max_cache_size: int):
        """Setup caching for performance"""
        if max_cache_size != DEFAULT_CACHE_SIZE:
            self._redux_allele = functools.lru_cache(maxsize=max_cache_size)(
                self._redux_allele
            )
            self.redux = functools.lru_cache(maxsize=max_cache_size)(self.redux)
            self.is_mac = functools.lru_cache(maxsize=max_cache_size)(
                self.mac_handler.is_mac
            )
            self.smart_sort_comparator = functools.lru_cache(maxsize=max_cache_size)(
                smart_sort.smart_sort_comparator
            )
        else:
            self.smart_sort_comparator = smart_sort.smart_sort_comparator

    @staticmethod
    def _freeze_reference_data():
        """Freeze reference data for Python >= 3.9"""
        if sys.version_info.major == 3 and sys.version_info.minor >= 9:
            import gc

            gc.freeze()

    def __del__(self):
        """Close database connection when ARD instance is destroyed"""
        if hasattr(self, "db_connection") and self.db_connection:
            self.db_connection.close()

    @functools.lru_cache(maxsize=DEFAULT_CACHE_SIZE)
    def _redux_allele(
        self, allele: str, redux_type: VALID_REDUCTION_TYPE, re_ping=True
    ) -> str:
        """Core allele reduction with ping logic"""
        # Handle HLA- prefix
        if HLA_regex.search(allele):
            hla, allele_name = allele.split("-")
            redux_allele = self._redux_allele(allele_name, redux_type)
            if redux_allele:
                if "/" in redux_allele:
                    return "/".join([f"HLA-{ra}" for ra in redux_allele.split("/")])
                return f"HLA-{redux_allele}"
            return redux_allele

        if not self._config["strict"]:
            allele = self._get_non_strict_allele(allele)

        # Handle P/G suffixes
        if allele.endswith(("P", "G")) and redux_type in ["lg", "lgx", "G"]:
            allele = allele[:-1]

        # Handle ping mode
        if self._config["ping"] and re_ping and redux_type in ("lg", "lgx", "U2"):
            if allele in self.ars_mappings.p_not_g:
                not_g_allele = self.ars_mappings.p_not_g[allele]
                if redux_type == "lg":
                    return self.allele_reducer._add_lg_suffix(not_g_allele)
                return not_g_allele
            else:
                redux_allele = self._redux_allele(allele, redux_type, False)
                if redux_allele.endswith("g"):
                    no_suffix_allele = redux_allele[:-1]
                elif redux_allele.endswith("ARS"):
                    no_suffix_allele = redux_allele[:-3]
                else:
                    no_suffix_allele = redux_allele

                if (
                    no_suffix_allele == allele
                    or "/" in no_suffix_allele
                    or no_suffix_allele in self.ars_mappings.p_not_g.values()
                ):
                    return redux_allele

                twice_redux_allele = self._redux_allele(
                    no_suffix_allele, redux_type, False
                )
                if "/" in twice_redux_allele:
                    return twice_redux_allele
                if self._is_valid_allele(twice_redux_allele):
                    return twice_redux_allele

        return self.allele_reducer.reduce_allele(allele, redux_type, re_ping)

    @functools.lru_cache(maxsize=DEFAULT_CACHE_SIZE)
    def redux(self, glstring: str, redux_type: VALID_REDUCTION_TYPE = "lgx") -> str:
        """Main redux method using specialized handlers"""
        # Handle GL string delimiters first
        processed_gl = self.gl_processor.process_gl_string(glstring, redux_type)
        if processed_gl != glstring or self.is_glstring(processed_gl):
            return processed_gl

        # Handle ignored allele suffixes
        if self._config["ignore_allele_with_suffixes"]:
            _, fields = glstring.split("*")
            if fields in self._config["ignore_allele_with_suffixes"]:
                return glstring

        # Handle V2 to V3 mapping
        if self.v2_handler.is_v2(glstring):
            glstring = self.v2_handler.map_v2_to_v3(glstring)
            return self.redux(glstring, redux_type)

        # Handle Serology
        if self._config["reduce_serology"] and self.serology_handler.is_serology(
            glstring
        ):
            alleles = self.serology_handler.get_alleles_from_serology(glstring)
            if alleles:
                return self.redux("/".join(alleles), redux_type)
            return ""

        is_hla_prefix = HLA_regex.search(glstring)
        if is_hla_prefix:
            allele = glstring.split("-")[1]
        else:
            allele = glstring
        # Validate format
        if ":" in allele:
            loc_allele = allele.split(":")
            if len(loc_allele) < 2:
                raise InvalidTypingError(
                    f"{glstring} is not a valid V2 or Serology typing."
                )
            loc_antigen, code = loc_allele[0], loc_allele[1]
            # Check for empty fields (like DQA1*01:01:01:G where G is after empty field)
            if any(field == "" for field in loc_allele[1:]):
                raise InvalidTypingError(
                    f"{glstring} is not a valid V2 or Serology typing."
                )
        else:
            if "*" in allele:
                locus, _ = allele.split("*")
                if locus not in G_GROUP_LOCI:
                    return glstring
            raise InvalidTypingError(
                f"{glstring} is not a valid V2 or Serology typing."
            )

        # Handle XX codes
        if (
            self._config["reduce_XX"]
            and code == "XX"
            and self.xx_handler.is_xx(allele, loc_antigen, code)
        ):
            reduced_alleles = self.redux(
                "/".join(self.code_mappings.xx_codes[loc_antigen]), redux_type
            )
            if is_hla_prefix:
                return "/".join([f"HLA-{a}" for a in reduced_alleles.split("/")])
            return reduced_alleles

        # Handle MAC
        if self._config["reduce_MAC"] and code.isalpha():
            if self.mac_handler.is_mac(allele):
                alleles = self.mac_handler._get_alleles(code, loc_antigen)
                if is_hla_prefix:
                    alleles = [f"HLA-{a}" for a in alleles]
                return self.redux("/".join(alleles), redux_type)
            else:
                raise InvalidMACError(f"{glstring} is an invalid MAC.")

        # Handle short nulls
        if self._config["reduce_shortnull"] and self.shortnull_handler.is_shortnull(
            glstring
        ):
            return self.redux("/".join(self.shortnulls[glstring]), redux_type)

        return self._redux_allele(glstring, redux_type)

    @staticmethod
    def is_glstring(gl_string: str) -> bool:
        return (
            "/" in gl_string or "+" in gl_string or "^" in gl_string or "~" in gl_string
        )

    # Delegate methods to handlers
    def is_mac(self, allele: str) -> bool:
        return self.mac_handler.is_mac(allele)

    def is_serology(self, allele: str) -> bool:
        return self.serology_handler.is_serology(allele)

    def is_v2(self, allele: str) -> bool:
        return self.v2_handler.is_v2(allele)

    def is_XX(self, glstring: str, loc_antigen: str = None, code: str = None) -> bool:
        return self.xx_handler.is_xx(glstring, loc_antigen, code)

    def is_shortnull(self, allele: str) -> bool:
        return self.shortnull_handler.is_shortnull(allele)

    def is_null(self, allele: str) -> bool:
        return self.shortnull_handler.is_null(allele)

    def expand_mac(self, mac_code: str) -> str:
        return self.mac_handler.expand_mac(mac_code)

    def lookup_mac(self, allelelist_gl: str) -> str:
        return self.mac_handler.lookup_mac(allelelist_gl)

    def find_broad_splits(self, allele: str) -> tuple:
        return self.serology_handler.find_broad_splits(allele)

    def find_associated_antigen(self, serology: str) -> str:
        return self.serology_handler.find_associated_antigen(serology)

    def find_xx_from_serology(self, serology: str) -> str:
        return self.serology_handler.find_xx_from_serology(serology)

    def v2_to_v3(self, v2_allele: str) -> str:
        return self.v2_handler.map_v2_to_v3(v2_allele)

    # Keep existing methods that don't fit into handlers
    def validate(self, glstring: str) -> bool:
        return self.gl_processor.validate_gl_string(glstring)

    def _get_non_strict_allele(self, allele: str) -> str:
        """Handle non-strict allele validation"""
        from .constants import expression_chars

        if not self._is_allele_in_db(allele):
            for expr_char in expression_chars:
                if self._is_allele_in_db(allele + expr_char):
                    if self._config["verbose_log"]:
                        print(f"{allele} is not valid. Using {allele}{expr_char}")
                    allele = allele + expr_char
                    break
        return allele

    def _is_who_allele(self, allele: str) -> bool:
        return allele in self.allele_group.who_alleles

    def _is_allele_in_db(self, allele: str) -> bool:
        return allele in self.allele_group.alleles

    def _is_valid_allele(self, allele: str) -> bool:
        if allele.endswith(("P", "G")):
            allele = allele[:-1]
        if "*" in allele:
            _, fields = allele.split("*")
            if not all(map(str.isalnum, fields.split(":"))):
                return False
        if self._is_allele_in_db(allele):
            return True
        else:
            allele = get_2field_allele(allele)
            return self._is_allele_in_db(allele)

    def _is_valid(self, allele: str) -> bool:
        """Validate allele in various forms"""
        if allele == "" or allele.endswith("*"):
            return False

        if HLA_regex.search(allele):
            allele = allele[4:]

        if "*" in allele:
            alphanum_allele = allele.replace("*", "").replace(":", "")
            if not alphanum_allele.isalnum():
                return False

            if self._config["ignore_allele_with_suffixes"]:
                locus, fields = allele.split("*")
                if fields in self._config["ignore_allele_with_suffixes"]:
                    return True

        if not self._config["strict"]:
            allele = self._get_non_strict_allele(allele)

        if (
            not self.is_mac(allele)
            and not self.is_XX(allele)
            and not self.is_serology(allele)
            and not self.is_v2(allele)
            and not self.is_shortnull(allele)
        ):
            return self._is_valid_allele(allele)

        return True

    # Keep remaining methods unchanged
    def is_exp_allele(self, allele: str) -> bool:
        return allele in self.allele_group.exp_alleles

    def cwd_redux(self, allele_list_gl: str) -> str:
        """CWD reduction using existing logic"""
        alleles = []
        for allele in allele_list_gl.split("/"):
            if self.is_mac(allele):
                alleles.extend(self.expand_mac(allele).split("/"))
            elif is_2_field_allele(allele) and not self.is_XX(allele):
                alleles.append(allele)
            else:
                alleles.extend(self.redux(allele, "lgx").split("/"))

        locus = allele_list_gl.split("*")[0]
        if HLA_regex.search(locus):
            locus = locus.split("-")[1]
        ciwd_for_locus = db.load_cwd(self.db_connection, locus)

        alleles_in_ciwd = ciwd_for_locus.intersection(alleles)
        return "/".join(sorted(alleles_in_ciwd))

    def refresh_mac_codes(self) -> None:
        dr.generate_mac_codes(self.db_connection, refresh_mac=True)

    def get_db_version(self) -> str:
        return dr.get_db_version(self.db_connection)

    def similar_alleles(self, prefix: str) -> Union[List, None]:
        """Find similar alleles using existing logic"""
        if "*" not in prefix:
            return None

        locus, fields = prefix.split("*")
        if fields:
            if len(fields.split(":")) == 2:
                first_field, mac_prefix = fields.split(":")
                if mac_prefix.isalpha():
                    similar_mac_names = db.similar_mac(self.db_connection, mac_prefix)
                    if similar_mac_names:
                        locus_prefix = f"{locus}*{first_field}"
                        mac_codes = [
                            f"{locus_prefix}:{code}" for code in similar_mac_names
                        ]
                        return sorted(filter(lambda mac: self.is_mac(mac), mac_codes))

            similar_allele_names = db.similar_alleles(self.db_connection, prefix)
            if similar_allele_names:
                return sorted(
                    similar_allele_names,
                    key=functools.cmp_to_key(smart_sort.smart_sort_comparator),
                )

        return None
