# -*- coding: utf-8 -*-
"""
HLA Allele Reduction Strategy for Serology Groups.

This module implements the serology reduction strategy for HLA alleles.
Serology reduction converts molecular HLA alleles back to their corresponding
serological equivalents, which were historically used before DNA-based typing.
"""

import functools

from .base_reducer import Reducer
from .. import db
from ..misc import is_2_field_allele


class SReducer(Reducer):
    """
    Strategy for serology reduction of HLA alleles.

    Serology reduction converts molecular HLA alleles to their corresponding
    serological equivalents. This is important for compatibility with legacy
    systems and historical HLA typing data that used serological methods
    before DNA-based typing became standard.

    The reduction process:
    1. Determines if the allele is 2-field and reduces to LGX if needed
    2. Queries the serology mapping database to find corresponding serologies
    3. Handles both direct matches and LGX-reduced matches
    4. Returns sorted serology designations

    Examples:
        - A*01:01:01:01 -> A1
        - A*02:01:01:01 -> A2
        - B*07:02:01 -> B7
        - DRB1*15:01:01:01 -> DR15

    Note:
        Some alleles may map to multiple serological equivalents,
        in which case they are returned as a slash-separated list.

    Attributes:
        ard: The ARD (Antigen Recognition Domain) object containing mapping data
    """

    def reduce(self, allele: str) -> str:
        """
        Reduce an HLA allele to its serological equivalent(s).

        This method performs serology reduction by querying the serology mapping
        database to find which serological designations correspond to the given
        molecular allele. It handles both 2-field and multi-field alleles with
        appropriate fallback strategies.

        Args:
            allele (str): The HLA allele to reduce (e.g., "A*01:01:01:01")

        Returns:
            str: The serological equivalent(s) (e.g., "A1" or "A1/A36" for multiple matches)

        Examples:
            >>> reducer = SReducer(ard)
            >>> reducer.reduce("A*01:01:01:01")
            "A1"
            >>> reducer.reduce("A*02:01:01:01")
            "A2"
            >>> reducer.reduce("B*07:02:01")
            "B7"

        Process:
            1. Check if allele is 2-field and reduce to LGX if necessary
            2. Query serology mapping database
            3. Find matching serologies by checking allele lists
            4. If no matches and allele is 2-field, try LGX-reduced matching
            5. Return sorted serology designations
        """
        # Step 1: Handle 2-field alleles by reducing to LGX first
        if is_2_field_allele(allele):
            allele = self.ard._redux_allele(allele, "lgx")
            # Query serology mapping using LGX-specific allele lists
            serology_mapping = db.find_serology_for_allele(
                self.ard.db_connection, allele, "lgx_allele_list"
            )
        else:
            # Query serology mapping for multi-field alleles
            serology_mapping = db.find_serology_for_allele(
                self.ard.db_connection, allele
            )

        # Step 2: Find serologies that contain this allele in their allele lists
        serology_set = set()
        for serology, allele_list in serology_mapping.items():
            # Check if our allele is in the slash-separated allele list
            if allele in allele_list.split("/"):
                serology_set.add(serology)

        # Step 3: Fallback strategy for 2-field alleles with no direct matches
        if not serology_set and is_2_field_allele(allele):
            # Try matching against LGX-reduced versions of the allele lists
            for serology, allele_list in serology_mapping.items():
                # Reduce the entire allele list to LGX and check for matches
                allele_list_lgx = self.ard.redux(allele_list, "lgx")
                if allele in allele_list_lgx.split("/"):
                    serology_set.add(serology)

        # Step 4: Return sorted serology designations
        # Use smart sort comparator to ensure proper HLA ordering
        return "/".join(
            sorted(
                serology_set, key=functools.cmp_to_key(self.ard.smart_sort_comparator)
            )
        )
