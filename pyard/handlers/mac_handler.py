# -*- coding: utf-8 -*-

import functools
import sqlite3
from collections import Counter
from typing import Iterable, TYPE_CHECKING

from .. import db
from ..constants import HLA_regex, DEFAULT_CACHE_SIZE
from ..exceptions import InvalidMACError

if TYPE_CHECKING:
    from ..ard import ARD


class MACHandler:
    """Handles MAC (Multiple Allele Code) operations

    MAC codes are shorthand representations for groups of HLA alleles that
    share common characteristics. This class provides functionality to:
    - Validate MAC codes
    - Expand MAC codes to their constituent alleles
    - Find MAC codes for given allele lists
    """

    def __init__(self, ard_instance: "ARD"):
        """Initialize the MACHandler with an ARD instance

        Args:
            ard_instance: The main ARD object for database access
        """
        self.ard = ard_instance

    @functools.lru_cache(maxsize=DEFAULT_CACHE_SIZE)
    def is_mac(self, allele: str) -> bool:
        """Check if allele is a valid MAC code

        MAC codes have the format 'LOCUS*ANTIGEN:CODE' where CODE is alphabetic.
        Validates by checking if the code exists in the database and if the
        antigen group matches the provided locus.

        Args:
            allele: String to check (e.g., 'A*01:AB', 'B*15:XX')

        Returns:
            True if the string is a valid MAC code, False otherwise
        """
        # MAC codes must contain a colon separator
        if ":" in allele:
            allele_split = allele.split(":")
            if len(allele_split) == 2:
                locus_antigen, code = allele_split
                # MAC codes have alphabetic suffixes (not numeric)
                if code.isalpha():
                    try:
                        # Query database for alleles associated with this MAC code
                        alleles = db.mac_code_to_alleles(self.ard.db_connection, code)
                        if alleles:
                            # Check if MAC expands to full allele names (contains ':')
                            if any(map(lambda a: ":" in a, alleles)):
                                # Validate that the antigen group matches
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
        """Expand MAC code into GL string of alleles

        Converts a MAC code into its constituent alleles as a GL string
        with '/' delimiters. Handles both HLA-prefixed and non-prefixed formats.

        Args:
            mac_code: MAC code to expand (e.g., 'A*01:AB', 'HLA-A*01:AB')

        Returns:
            GL string of alleles separated by '/' (e.g., 'A*01:01/A*01:02')

        Raises:
            InvalidMACError: If the MAC code is invalid
        """
        if self.is_mac(mac_code):
            locus_antigen, code = mac_code.split(":")
            # Handle HLA-prefixed format
            if HLA_regex.search(mac_code):
                locus_antigen = locus_antigen.split("-")[1]
                return "/".join(
                    ["HLA-" + a for a in self.get_alleles(code, locus_antigen)]
                )
            else:
                # Handle standard format without HLA prefix
                return "/".join(self.get_alleles(code, locus_antigen))
        raise InvalidMACError(f"{mac_code} is an invalid MAC.")

    def lookup_mac(self, allelelist_gl: str) -> str:
        """Find MAC code corresponding to allele list

        Searches for a MAC code that represents the given list of alleles.
        Tries multiple strategies: single antigen group optimization,
        original order, and sorted order.

        Args:
            allelelist_gl: GL string of alleles separated by '/'
                          (e.g., 'A*01:01/A*01:02/A*01:03')

        Returns:
            MAC code representing the allele list (e.g., 'A*01:AB')

        Raises:
            InvalidMACError: If no MAC code exists for the allele list
        """
        alleles = allelelist_gl.split("/")
        allele_fields = [allele.split("*")[1] for allele in alleles]
        antigen_groups = sorted({allele.split(":")[0] for allele in allele_fields})

        # Optimization: if all alleles share same antigen group, use field suffixes only
        if len(antigen_groups) == 1:
            mac_expansion = "/".join(
                sorted({allele.split(":")[1] for allele in allele_fields})
            )
            mac_code = db.alleles_to_mac_code(self.ard.db_connection, mac_expansion)
            if mac_code:
                locus = allelelist_gl.split("*")[0]
                return f"{locus}*{antigen_groups[0]}:{mac_code}"

        # Strategy 1: Try alleles in given order
        mac_expansion = "/".join(allele_fields)
        mac_code = db.alleles_to_mac_code(self.ard.db_connection, mac_expansion)
        if mac_code:
            locus = allelelist_gl.split("*")[0]
            return f"{locus}*{antigen_groups[0]}:{mac_code}"

        # Strategy 2: Try alleles in sorted order
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

    def get_alleles(self, code, locus_antigen) -> Iterable[str]:
        """Get alleles for MAC code

        Retrieves the list of alleles that a MAC code represents from the database.
        Handles two formats: full allele expansions and field suffix expansions.

        Args:
            code: MAC code suffix (e.g., 'AB', 'XX')
            locus_antigen: Locus and antigen part (e.g., 'A*01', 'B*15')

        Returns:
            List of alleles that the MAC code represents, filtered to only
            include alleles present in the current database
        """
        # Query database for alleles associated with this MAC code
        alleles = db.mac_code_to_alleles(self.ard.db_connection, code)

        # Check if MAC expands to full allele names (contains ':')
        is_allelic_expansion = any([":" in allele for allele in alleles])
        if is_allelic_expansion:
            # Full allele format: prepend locus only
            locus = locus_antigen.split("*")[0]
            alleles = [f"{locus}*{a}" for a in alleles]
        else:
            # Field suffix format: append to locus_antigen
            alleles = [f"{locus_antigen}:{a}" for a in alleles]

        # Filter to only include alleles that exist in current database
        return list(filter(self.ard._is_allele_in_db, alleles))
