# -*- coding: utf-8 -*-
"""
HLA Allele Reduction Strategy for WHO Nomenclature.

This module implements the W (WHO) reduction strategy for HLA alleles.
WHO reduction expands or reduces alleles to conform to the official
WHO nomenclature standards for HLA typing.
"""

from .base_reducer import Reducer


class WReducer(Reducer):
    """
    Strategy for W (WHO) reduction of HLA alleles.

    WHO reduction ensures that HLA alleles conform to the official World Health
    Organization (WHO) nomenclature standards. This reduction can both expand
    and reduce alleles to their proper WHO-compliant representation, which
    typically means full-field nomenclature (4, 3, or 2 fields as appropriate).

    The WHO nomenclature system is the official standard defined by the
    WHO Nomenclature Committee for Factors of the HLA System and ensures
    consistent representation of HLA alleles across different systems and
    databases.

    The reduction logic:
    1. If allele is already WHO-compliant, return as-is
    2. If allele has WHO group mapping, expand to WHO-compliant form
    3. If no mapping exists, return original allele unchanged

    Examples:
        - A*01:01 -> A*01:01:01:01 (expansion to full WHO nomenclature)
        - B*07:02 -> B*07:02:01 (expansion to appropriate WHO level)
        - DRB1*15:01 -> DRB1*15:01:01:01 (full WHO expansion)

    Note:
        WHO reduction may result in expansion rather than reduction,
        as it aims for the most complete and standardized representation.

    Attributes:
        ard: The ARD (Antigen Recognition Domain) object containing mapping data
    """

    def reduce(self, allele: str) -> str:
        """
        Reduce/expand an HLA allele to WHO nomenclature standard.

        This method performs WHO reduction by checking if the allele already
        conforms to WHO standards, and if not, attempts to expand it using
        WHO group mappings. The process may result in expansion rather than
        reduction to achieve WHO compliance.

        Args:
            allele (str): The HLA allele to process (e.g., "A*01:01")

        Returns:
            str: The WHO-compliant allele representation (e.g., "A*01:01:01:01")

        Examples:
            >>> reducer = WReducer(ard)
            >>> reducer.reduce("A*01:01")
            "A*01:01:01:01"  # expanded to full WHO nomenclature
            >>> reducer.reduce("B*07:02")
            "B*07:02:01"     # expanded to appropriate WHO level
            >>> reducer.reduce("A*01:01:01:01")
            "A*01:01:01:01"  # already WHO-compliant, returned as-is

        Process:
            1. Check if allele is already WHO-compliant
            2. If not, look up WHO group mapping
            3. Recursively apply WHO reduction to mapped alleles
            4. Return original if no mapping exists
        """
        # Step 1: Check if allele already conforms to WHO nomenclature
        if self.ard._is_who_allele(allele):
            return allele

        # Step 2: Look up WHO group mapping for expansion
        if allele in self.ard.code_mappings.who_group:
            # Get the list of WHO-compliant alleles for this input
            who_alleles = self.ard.code_mappings.who_group[allele]

            # Recursively apply WHO reduction to the mapped alleles
            # This handles cases where the mapping itself needs further WHO processing
            return self.ard.redux("/".join(who_alleles), "W")
        else:
            # Step 3: No WHO mapping found - return original allele
            # This preserves alleles that don't have WHO group mappings
            return allele
