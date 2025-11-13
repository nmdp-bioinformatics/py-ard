# -*- coding: utf-8 -*-
"""
HLA Allele Reduction Strategy for G Groups.

This module implements the G group reduction strategy for HLA alleles.
G groups represent alleles that have identical nucleotide sequences across
the exons encoding the antigen recognition domain (ARD).
"""

from .default_reducer import DefaultReducer


class GGroupReducer(DefaultReducer):
    """
    Strategy for G group reduction of HLA alleles.

    G groups are collections of HLA alleles that have identical nucleotide
    sequences in the exons encoding the antigen recognition domain (ARD).
    This reduction is important for HLA matching as alleles within the same
    G group are functionally equivalent for transplantation purposes.

    The G group reduction follows this priority:
    1. Check for duplicate G group mappings (dup_g) - handles special cases
    2. Use standard G group mappings (g_group)
    3. Fall back to default reduction if no G group mapping exists

    Examples:
        - A*01:01:01:01 -> A*01:01:01G
        - A*01:01:01:02N -> A*01:01:01G (same G group as above)
        - B*07:02:01 -> B*07:02:01G

    Attributes:
        ard: The ARD (Antigen Recognition Domain) object containing mapping data
    """

    def reduce(self, allele: str) -> str:
        """
        Reduce an HLA allele to its G group representation.

        This method performs G group reduction by checking multiple mapping tables
        in order of priority. It first checks for duplicate G group mappings,
        then standard G group mappings, and finally falls back to default reduction.

        Args:
            allele (str): The HLA allele to reduce (e.g., "A*01:01:01:01")

        Returns:
            str: The reduced allele in G group format (e.g., "A*01:01:01G")

        Examples:
            >>> reducer = GGroupReducer(ard)
            >>> reducer.reduce("A*01:01:01:01")
            "A*01:01:01G"
            >>> reducer.reduce("A*01:01:01:02N")
            "A*01:01:01G"
            >>> reducer.reduce("B*07:02:01")
            "B*07:02:01G"

        Note:
            If the allele is not found in any G group mapping, it falls back
            to the default reduction strategy from the parent class.
        """
        # Check if allele has a G group mapping
        if allele in self.ard.ars_mappings.g_group:
            # Priority 1: Check for duplicate G group mappings (special cases)
            if allele in self.ard.ars_mappings.dup_g:
                return self.ard.ars_mappings.dup_g[allele]
            else:
                # Priority 2: Use standard G group mapping
                return self.ard.ars_mappings.g_group[allele]

        # Priority 3: Fall back to default reduction if no G group mapping exists
        return super().reduce(allele)
