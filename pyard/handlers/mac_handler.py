# -*- coding: utf-8 -*-

import functools
import sqlite3
from collections import Counter
from typing import Iterable, TYPE_CHECKING

from ..constants import HLA_regex, DEFAULT_CACHE_SIZE
from ..exceptions import InvalidMACError
from .. import db

if TYPE_CHECKING:
    from ..ard import ARD


class MACHandler:
    """Handles MAC (Multiple Allele Code) operations"""

    def __init__(self, ard_instance: "ARD"):
        self.ard = ard_instance

    @functools.lru_cache(maxsize=DEFAULT_CACHE_SIZE)
    def is_mac(self, allele: str) -> bool:
        """Check if allele is a valid MAC code"""
        if ":" in allele:
            allele_split = allele.split(":")
            if len(allele_split) == 2:
                locus_antigen, code = allele_split
                if code.isalpha():
                    try:
                        alleles = db.mac_code_to_alleles(self.ard.db_connection, code)
                        if alleles:
                            if any(map(lambda a: ":" in a, alleles)):
                                antigen_groups = map(lambda a: a.split(":")[0], alleles)
                                antigen_counts = Counter(antigen_groups)
                                valid_antigen = antigen_counts.most_common(1).pop()[0]
                                provided_antigen = locus_antigen.split("*").pop()
                                return provided_antigen == valid_antigen
                            return True
                    except sqlite3.OperationalError as e:
                        print("Error: ", e)
        return False

    def expand_mac(self, mac_code: str) -> str:
        """Expand MAC code into GL string of alleles"""
        if self.is_mac(mac_code):
            locus_antigen, code = mac_code.split(":")
            if HLA_regex.search(mac_code):
                locus_antigen = locus_antigen.split("-")[1]
                return "/".join(
                    ["HLA-" + a for a in self._get_alleles(code, locus_antigen)]
                )
            else:
                return "/".join(self._get_alleles(code, locus_antigen))
        raise InvalidMACError(f"{mac_code} is an invalid MAC.")

    def lookup_mac(self, allelelist_gl: str) -> str:
        """Find MAC code corresponding to allele list"""
        alleles = allelelist_gl.split("/")
        allele_fields = [allele.split("*")[1] for allele in alleles]
        antigen_groups = sorted({allele.split(":")[0] for allele in allele_fields})

        if len(antigen_groups) == 1:
            mac_expansion = "/".join(
                sorted({allele.split(":")[1] for allele in allele_fields})
            )
            mac_code = db.alleles_to_mac_code(self.ard.db_connection, mac_expansion)
            if mac_code:
                locus = allelelist_gl.split("*")[0]
                return f"{locus}*{antigen_groups[0]}:{mac_code}"

        # Try given list order
        mac_expansion = "/".join(allele_fields)
        mac_code = db.alleles_to_mac_code(self.ard.db_connection, mac_expansion)
        if mac_code:
            locus = allelelist_gl.split("*")[0]
            return f"{locus}*{antigen_groups[0]}:{mac_code}"

        # Try sorted list
        mac_expansion = "/".join(
            sorted(
                allele_fields, key=functools.cmp_to_key(self.ard.smart_sort_comparator)
            )
        )
        mac_code = db.alleles_to_mac_code(self.ard.db_connection, mac_expansion)
        if mac_code:
            locus = allelelist_gl.split("*")[0]
            return f"{locus}*{antigen_groups[0]}:{mac_code}"

        raise InvalidMACError(f"{allelelist_gl} does not have a MAC.")

    def _get_alleles(self, code, locus_antigen) -> Iterable[str]:
        """Get alleles for MAC code"""
        alleles = db.mac_code_to_alleles(self.ard.db_connection, code)

        is_allelic_expansion = any([":" in allele for allele in alleles])
        if is_allelic_expansion:
            locus = locus_antigen.split("*")[0]
            alleles = [f"{locus}*{a}" for a in alleles]
        else:
            alleles = [f"{locus_antigen}:{a}" for a in alleles]

        return list(filter(self.ard._is_allele_in_db, alleles))
