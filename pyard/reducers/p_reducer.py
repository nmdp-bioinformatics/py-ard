# -*- coding: utf-8 -*-
"""
HLA Allele Reduction Strategy for P Groups.

This module implements the P group reduction strategy for HLA alleles.
P groups represent alleles that have identical protein sequences when
expressed, making them functionally equivalent at the protein level.
"""

from .default_reducer import DefaultReducer


class PGroupReducer(DefaultReducer):
    """
    Strategy for P group reduction of HLA alleles.

    P groups are collections of HLA alleles that encode identical protein
    sequences when expressed. This reduction is particularly useful when
    the focus is on the functional protein product rather than the specific
    nucleotide sequence differences that don't affect the final protein.

    P group reduction is broader than G group reduction, as it groups together
    alleles that may have different nucleotide sequences but produce the same
    protein. This makes P groups useful for functional analysis and certain
    types of HLA matching where protein-level equivalence is sufficient.

    Examples:
        - A*01:01:01:01 -> A*01:01P
        - A*01:01:01:02N -> A*01:01P (same protein as above)
        - B*07:02:01 -> B*07:02P

    Note:
        In py-ard's "ping" mode (default), when an allele doesn't have a G group,
        its corresponding P group is used instead, making P groups particularly
        important for comprehensive allele reduction.

    Attributes:
        ard: The ARD (Antigen Recognition Domain) object containing mapping data
    """

    def reduce(self, allele: str) -> str:
        """
        Reduce an HLA allele to its P group representation.

        This method performs P group reduction by checking if the allele exists
        in the P group mapping table. If found, it returns the corresponding
        P group designation. If not found, it falls back to the default
        reduction strategy from the parent class.

        Args:
            allele (str): The HLA allele to reduce (e.g., "A*01:01:01:01")

        Returns:
            str: The reduced allele in P group format (e.g., "A*01:01P")

        Examples:
            >>> reducer = PGroupReducer(ard)
            >>> reducer.reduce("A*01:01:01:01")
            "A*01:01P"
            >>> reducer.reduce("A*01:01:01:02N")
            "A*01:01P"
            >>> reducer.reduce("B*07:02:01")
            "B*07:02P"

        Note:
            If the allele is not found in the P group mapping, it falls back
            to the default reduction strategy from the parent class.
        """
        # Check if allele has a P group mapping
        if allele in self.ard.ars_mappings.p_group:
            return self.ard.ars_mappings.p_group[allele]

        # Fall back to default reduction if no P group mapping exists
        return super().reduce(allele)
