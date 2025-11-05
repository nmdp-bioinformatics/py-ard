# -*- coding: utf-8 -*-

import re
from typing import TYPE_CHECKING

from .. import db

if TYPE_CHECKING:
    from ..ard import ARD


class V2Handler:
    """Handles V2 to V3 nomenclature conversion

    HLA nomenclature has evolved over time. V2 (version 2) nomenclature used
    a different format than the current V3 (version 3) standard. This class
    provides functionality to:
    - Identify V2 format alleles
    - Convert V2 alleles to V3 format
    - Use heuristics when direct mappings are unavailable
    """

    def __init__(self, ard_instance: "ARD"):
        """Initialize the V2Handler with an ARD instance

        Args:
            ard_instance: The main ARD object for database access and configuration
        """
        self.ard = ard_instance

    def is_v2(self, allele: str) -> bool:
        """Check if allele is V2 nomenclature

        V2 alleles are characterized by having a '*' but no ':' separator,
        and exclude certain loci (MICA, MICB, HFE). The method validates
        by attempting conversion to V3 format and checking database existence.

        Args:
            allele: Allele string to check (e.g., 'A*0101', 'B*2705')

        Returns:
            True if the allele is valid V2 nomenclature and V2 reduction is enabled,
            False otherwise
        """
        # Check basic V2 format criteria
        matches_v2_format = (
            self.ard.config.v2_enabled  # V2 reduction must be enabled
            and "*" in allele  # Must have locus separator
            and ":" not in allele  # Must not have field separators (V3 feature)
            and allele.split("*")[0]
            not in ["MICA", "MICB", "HFE"]  # Exclude these loci
        )

        if matches_v2_format:
            # Attempt conversion to V3 format for validation
            v3_format_allele = self.map_v2_to_v3(allele)
            if v3_format_allele != allele:
                # Check if converted allele is valid (MAC code or database allele)
                if v3_format_allele.split(":").pop().isalpha():
                    return self.ard.is_mac(v3_format_allele)
                return self.ard._is_allele_in_db(v3_format_allele)

        return False

    def map_v2_to_v3(self, v2_allele: str) -> str:
        """Convert V2 allele to V3 format

        Attempts to convert a V2 format allele to V3 format using database
        mappings first, then falls back to heuristic prediction if no
        direct mapping exists.

        Args:
            v2_allele: V2 format allele (e.g., 'A*0101')

        Returns:
            V3 format allele (e.g., 'A*01:01') or original if conversion fails
        """
        # Try database lookup first
        v3_allele = db.v2_to_v3_allele(self.ard.db_connection, v2_allele)
        if not v3_allele:
            # Fall back to heuristic prediction
            v3_allele = self._predict_v3(v2_allele)
        return v3_allele

    def _predict_v3(self, v2_allele: str) -> str:
        """Use heuristic to predict V3 from V2

        Applies pattern-based rules to convert V2 format to V3 format when
        no database mapping exists. Uses digit grouping and locus-specific
        rules to insert colon separators appropriately.

        Args:
            v2_allele: V2 format allele to convert

        Returns:
            Predicted V3 format allele
        """
        locus, allele_name = v2_allele.split("*")
        # Extract numeric and non-numeric parts
        components = re.findall(r"^(\d+)(.*)", allele_name)
        if not components:
            return v2_allele

        digits_field, non_digits_field = components.pop()
        final_allele = digits_field
        num_of_digits = len(digits_field)

        # Single digit alleles remain unchanged
        if num_of_digits == 1:
            return v2_allele

        # Apply conversion rules based on digit count and locus
        if num_of_digits > 2:
            # Special case for DP locus with 5 digits
            if locus.startswith("DP") and num_of_digits == 5:
                final_allele = (
                    digits_field[:3] + ":" + (digits_field[3:]) + non_digits_field
                )
            # Even number of digits: group in pairs
            elif num_of_digits % 2 == 0:
                final_allele = self._combine_with_colon(digits_field) + non_digits_field
            # Odd number of digits: first 2, then remainder
            else:
                final_allele = (
                    digits_field[:2] + ":" + (digits_field[2:]) + non_digits_field
                )
        else:
            # 2 digits: add colon before non-digit suffix if present
            if non_digits_field:
                final_allele = digits_field + ":" + non_digits_field

        return locus + "*" + final_allele

    @staticmethod
    def _combine_with_colon(digits_field: str) -> str:
        """Combine digits with colon separator

        Groups digits into pairs separated by colons for V3 format conversion.
        Used when converting even-length digit sequences from V2 to V3.

        Args:
            digits_field: String of digits to group (e.g., '0101')

        Returns:
            Colon-separated digit pairs (e.g., '01:01')
        """
        num_of_digits = len(digits_field)
        return ":".join(digits_field[i : i + 2] for i in range(0, num_of_digits, 2))
