# -*- coding: utf-8 -*-
"""
HLA Allele Reduction Strategy for Unambiguous 2-Field Reduction.

This module implements the U2 (Unambiguous 2-field) reduction strategy for HLA alleles.
U2 reduction attempts to reduce alleles to 2-field level only when it results in
an unambiguous representation, otherwise falls back to LGX reduction.
"""

from .base_reducer import Reducer
from ..misc import get_n_field_allele


class U2Reducer(Reducer):
    """
    Strategy for U2 (Unambiguous 2-field) reduction of HLA alleles.

    U2 reduction is a conservative approach that only reduces alleles to
    2-field level when the reduction is unambiguous. This ensures that
    the reduced form maintains the same specificity as the original allele
    without introducing ambiguity.

    The reduction logic:
    1. If allele is already 2-field, return as-is
    2. If 2-field reduction exists unambiguously in database, use it
    3. If 2-field reduction would be ambiguous, fall back to LGX reduction

    This approach is particularly useful when you need to reduce resolution
    but want to avoid creating ambiguous typings that could represent
    multiple distinct alleles.

    Examples:
        - A*01:01:01:01 -> A*01:01 (if A*01:01 is unambiguous)
        - A*01:01:01:01 -> A*01:01 (if A*01:01 would be ambiguous, falls back to LGX)
        - B*07:02 -> B*07:02 (already 2-field, returned as-is)

    Attributes:
        ard: The ARD (Antigen Recognition Domain) object containing mapping data
    """

    def reduce(self, allele: str) -> str:
        """
        Reduce an HLA allele using U2 (Unambiguous 2-field) strategy.

        This method performs U2 reduction by checking if a 2-field reduction
        would be unambiguous. If the 2-field form exists as a valid allele
        in the database, it's considered unambiguous and returned. Otherwise,
        the method falls back to LGX reduction to avoid ambiguity.

        Args:
            allele (str): The HLA allele to reduce (e.g., "A*01:01:01:01")

        Returns:
            str: The reduced allele in U2 format (e.g., "A*01:01" or LGX fallback)

        Examples:
            >>> reducer = U2Reducer(ard)
            >>> reducer.reduce("A*01:01:01:01")
            "A*01:01"  # if unambiguous
            >>> reducer.reduce("B*07:02:01")
            "B*07:02"  # if unambiguous
            >>> reducer.reduce("C*01:02:01")
            "C*01:02"  # falls back to LGX if 2-field would be ambiguous

        Process:
            1. Check if allele is already 2-field (return as-is)
            2. Extract 2-field version while preserving expression suffixes
            3. Verify if 2-field version exists unambiguously in database
            4. Return 2-field if unambiguous, otherwise fall back to LGX
        """
        # Step 1: Parse allele fields
        allele_fields = allele.split(":")

        # Step 2: If already at 2-field level, no reduction needed
        if len(allele_fields) == 2:
            return allele

        # Step 3: Attempt 2-field reduction with expression preservation
        # Extract first 2 fields while preserving any expression suffixes (N, L, S, etc.)
        allele_2_fields = get_n_field_allele(allele, 2, preserve_expression=True)

        # Step 4: Check if 2-field reduction is unambiguous
        if self.ard._is_allele_in_db(allele_2_fields):
            # 2-field form exists in database - it's unambiguous
            return allele_2_fields
        else:
            # 2-field form would be ambiguous - fall back to LGX reduction
            # This ensures we don't create ambiguous typings
            return self.ard._redux_allele(allele, "lgx")
