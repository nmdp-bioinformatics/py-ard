# -*- coding: utf-8 -*-
"""
HLA Allele Reduction Strategies for LG and LGX levels.

This module implements reduction strategies for HLA alleles to the LG (2-field + 'g' suffix)
and LGX (2-field only) levels, which are commonly used in HLA typing and matching.
"""

from .base_reducer import Reducer


class LGXReducer(Reducer):
    """
    Strategy for LGX (2-field) reduction of HLA alleles.

    The LGX reduction reduces HLA alleles to their 2-field representation,
    which corresponds to the Antigen Recognition Domain (ARD) level.
    This is the most commonly used reduction level for HLA matching.

    Examples:
        - A*01:01:01:01 -> A*01:01
        - B*07:02:01 -> B*07:02
        - DRB1*15:01:01:01 -> DRB1*15:01

    Attributes:
        ard: The ARD (Antigen Recognition Domain) object containing mapping data
    """

    def reduce(self, allele: str) -> str:
        """
        Reduce an HLA allele to its LGX (2-field) representation.

        This method first checks if the allele exists in the pre-computed LGX group
        mappings. If found, it returns the mapped value. Otherwise, it performs
        a simple field-based reduction by taking only the first two fields.

        Args:
            allele (str): The HLA allele to reduce (e.g., "A*01:01:01:01")

        Returns:
            str: The reduced allele in LGX format (e.g., "A*01:01")

        Examples:
            >>> reducer = LGXReducer(ard)
            >>> reducer.reduce("A*01:01:01:01")
            "A*01:01"
            >>> reducer.reduce("B*07:02:01")
            "B*07:02"
        """
        # Check if allele has a pre-computed LGX mapping
        if allele in self.ard.ars_mappings.lgx_group:
            return self.ard.ars_mappings.lgx_group[allele]
        else:
            # Fallback: manually extract first 2 fields (locus + first two numeric fields)
            return ":".join(allele.split(":")[0:2])


class LGReducer(Reducer):
    """
    Strategy for LG reduction of HLA alleles (LGX + 'g' suffix).

    The LG reduction is similar to LGX but adds a 'g' suffix to indicate
    that the allele has been reduced to the 2-field level. This suffix
    helps distinguish between original 2-field typings and reduced typings.

    Examples:
        - A*01:01:01:01 -> A*01:01g
        - B*07:02:01 -> B*07:02g
        - DRB1*15:01:01:01 -> DRB1*15:01g

    Note:
        If the ARD configuration has 'ARS_as_lg' set to True, the suffix
        'ARS' is used instead of 'g'.

    Attributes:
        ard: The ARD (Antigen Recognition Domain) object containing mapping data
    """

    def reduce(self, allele: str) -> str:
        """
        Reduce an HLA allele to its LG representation (LGX + suffix).

        This method first performs LGX reduction and then adds the appropriate
        suffix ('g' or 'ARS' depending on configuration).

        Args:
            allele (str): The HLA allele to reduce (e.g., "A*01:01:01:01")

        Returns:
            str: The reduced allele in LG format (e.g., "A*01:01g")

        Examples:
            >>> reducer = LGReducer(ard)
            >>> reducer.reduce("A*01:01:01:01")
            "A*01:01g"
            >>> reducer.reduce("B*07:02:01")
            "B*07:02g"
        """
        # First perform LGX reduction
        lgx_strategy = LGXReducer(self.ard)
        redux_allele = lgx_strategy.reduce(allele)

        # Add appropriate suffix
        return self._add_lg_suffix(redux_allele)

    def _add_lg_suffix(self, redux_allele: str) -> str:
        """
        Add the LG suffix ('g' or 'ARS') to a reduced allele.

        This method handles both single alleles and allele lists (separated by '/').
        The suffix used depends on the ARD configuration setting 'ARS_as_lg'.

        Args:
            redux_allele (str): The reduced allele or allele list to add suffix to

        Returns:
            str: The allele(s) with appropriate LG suffix added

        Examples:
            >>> reducer._add_lg_suffix("A*01:01")
            "A*01:01g"
            >>> reducer._add_lg_suffix("A*01:01/A*01:02")
            "A*01:01g/A*01:02g"
        """
        # Handle allele lists (multiple alleles separated by '/')
        if "/" in redux_allele:
            return "/".join(
                [self._add_lg_suffix(allele) for allele in redux_allele.split("/")]
            )

        # Add suffix based on configuration
        if self.ard._config["ARS_as_lg"]:
            return redux_allele + "ARS"
        return redux_allele + "g"
