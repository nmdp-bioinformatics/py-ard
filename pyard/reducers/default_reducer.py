# -*- coding: utf-8 -*-
"""
Default HLA Allele Reduction Strategy with Validation.

This module implements the default reduction strategy that serves as a fallback
for other reducers and provides stringent validation of HLA alleles, particularly
those with P and G group suffixes.
"""

from .base_reducer import Reducer
from ..exceptions import InvalidAlleleError


class DefaultReducer(Reducer):
    """
    Default strategy for HLA allele validation and P/G suffix handling.

    The DefaultReducer serves as the base validation strategy and fallback
    for other reduction strategies. It performs stringent validation of
    HLA alleles, with special handling for P group and G group suffixes.

    This reducer is particularly important for:
    1. Validating P and G group designations against official mappings
    2. Serving as a fallback when other reduction strategies cannot process an allele
    3. Providing comprehensive allele validation before returning results
    4. Raising appropriate exceptions for invalid alleles

    The validation process:
    1. Check P group suffixes against official P group mappings
    2. Check G group suffixes against official G group mappings
    3. Validate general allele format and existence
    4. Raise InvalidAlleleError for invalid alleles

    Examples:
        - A*01:01P -> A*01:01P (if valid P group)
        - A*01:01:01G -> A*01:01:01G (if valid G group)
        - A*01:01:01:01 -> A*01:01:01:01 (if valid allele)
        - A*99:99 -> InvalidAlleleError (if invalid)

    Attributes:
        ard: The ARD (Antigen Recognition Domain) object containing mapping data
    """

    def reduce(self, allele: str) -> str:
        """
        Validate and return HLA allele with stringent P/G suffix checking.

        This method performs comprehensive validation of HLA alleles, with
        special attention to P and G group suffixes. It ensures that any
        allele with these suffixes actually exists in the official mapping
        tables before accepting them as valid.

        Args:
            allele (str): The HLA allele to validate (e.g., "A*01:01P", "A*01:01:01G")

        Returns:
            str: The validated allele unchanged if valid

        Raises:
            InvalidAlleleError: If the allele is invalid or suffix is not in official mappings

        Examples:
            >>> reducer = DefaultReducer(ard)
            >>> reducer.reduce("A*01:01P")
            "A*01:01P"  # if valid P group
            >>> reducer.reduce("A*01:01:01G")
            "A*01:01:01G"  # if valid G group
            >>> reducer.reduce("A*01:01:01:01")
            "A*01:01:01:01"  # if valid allele
            >>> reducer.reduce("A*99:99")
            InvalidAlleleError: A*99:99 is an invalid allele.

        Process:
            1. Check P group suffix validation against official mappings
            2. Check G group suffix validation against official mappings
            3. Perform general allele validation
            4. Raise exception for invalid alleles
        """
        # Step 1: Stringent validation for P group suffixes
        if allele.endswith("P"):
            # Verify that this P group designation exists in official P group mappings
            # This prevents acceptance of arbitrary P suffixes
            if allele in self.ard.ars_mappings.p_group.values():
                return allele
            # If P suffix but not in official mappings, fall through to general validation

        # Step 2: Stringent validation for G group suffixes
        elif allele.endswith("G"):
            # Verify that this G group designation exists in official G group mappings
            # This prevents acceptance of arbitrary G suffixes
            if allele in self.ard.ars_mappings.g_group.values():
                return allele
            # If G suffix but not in official mappings, fall through to general validation

        # Step 3: General allele validation
        if self.ard.is_valid_allele(allele):
            return allele
        else:
            # Step 4: Raise exception for invalid alleles
            # This ensures that invalid alleles are caught and reported
            raise InvalidAlleleError(f"{allele} is an invalid allele.")
