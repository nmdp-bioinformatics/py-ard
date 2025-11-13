# -*- coding: utf-8 -*-
"""
HLA Allele Reduction Strategy for Exon-Level (3-Field) Reduction.

This module implements the exon reduction strategy for HLA alleles.
Exon reduction reduces alleles to the 3-field level, which typically
represents the exon-level resolution including intron variations.
"""

from .base_reducer import Reducer
from ..constants import expression_chars


class ExonReducer(Reducer):
    """
    Strategy for exon (3-field) reduction of HLA alleles.

    Exon reduction reduces HLA alleles to their 3-field representation,
    which captures exon-level sequence differences including variations
    in non-coding regions (introns). This level of resolution is useful
    when intron variations are relevant for analysis.

    The reduction process:
    1. Check for pre-computed exon group mappings
    2. Handle expression character preservation (N, L, S, etc.)
    3. For unmapped alleles, expand to WHO level first, then reduce
    4. Avoid infinite recursion with appropriate termination conditions

    Examples:
        - A*01:01:01:01 -> A*01:01:01
        - A*01:01:01:02N -> A*01:01:01N (preserves expression character)
        - B*07:02:01:01 -> B*07:02:01
        - DRB1*15:01:01:01 -> DRB1*15:01:01

    Note:
        Expression characters (N, L, S, etc.) are preserved when they
        represent consistent expression patterns across all 4-field variants.

    Attributes:
        ard: The ARD (Antigen Recognition Domain) object containing mapping data
    """

    def reduce(self, allele: str) -> str:
        """
        Reduce an HLA allele to its exon (3-field) representation.

        This method performs exon reduction by first checking for pre-computed
        exon group mappings, handling expression character preservation, and
        using WHO expansion as a fallback strategy for unmapped alleles.

        Args:
            allele (str): The HLA allele to reduce (e.g., "A*01:01:01:01")

        Returns:
            str: The reduced allele in exon (3-field) format (e.g., "A*01:01:01")

        Examples:
            >>> reducer = ExonReducer(ard)
            >>> reducer.reduce("A*01:01:01:01")
            "A*01:01:01"
            >>> reducer.reduce("A*01:01:01:02N")
            "A*01:01:01N"  # expression character preserved
            >>> reducer.reduce("B*07:02:01:01")
            "B*07:02:01"

        Process:
            1. Check for pre-computed exon group mapping
            2. Handle expression character preservation if applicable
            3. For unmapped alleles, expand to WHO level first
            4. Recursively apply exon reduction to WHO-expanded form
        """
        # Step 1: Check for pre-computed exon group mapping
        if allele in self.ard.ars_mappings.exon_group:
            # Get the base 3-field exon group allele
            exon_group_allele = self.ard.ars_mappings.exon_group[allele]

            # Step 2: Handle expression character preservation
            # Check if original allele has an expression character (N, L, S, etc.)
            last_char = allele[-1]
            if last_char in expression_chars:
                # Create 3-field allele with preserved expression character
                exon_short_null_allele = exon_group_allele + last_char

                # Verify that this expression variant is valid (shortnull check)
                if self.ard.is_shortnull(exon_short_null_allele):
                    return exon_short_null_allele

            # Return base exon group allele (no expression character needed)
            return exon_group_allele
        else:
            # Step 3: Fallback strategy for unmapped alleles
            # First expand to WHO level to get complete nomenclature
            w_redux = self.ard.redux(allele, "W")

            # Step 4: Avoid infinite recursion
            # If WHO reduction doesn't change the allele or results in 2-field,
            # return original to prevent recursion
            if w_redux == allele or len(w_redux.split(":")) == 2:
                return allele
            else:
                # Recursively apply exon reduction to the WHO-expanded form
                # This handles cases where WHO expansion provides mappable alleles
                return self.ard.redux(w_redux, "exon")
