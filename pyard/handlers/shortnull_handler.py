# -*- coding: utf-8 -*-

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from ..ard import ARD


class ShortNullHandler:
    """Handles short null allele operations

    Null alleles are HLA alleles that do not produce functional proteins
    due to mutations. Short null alleles are abbreviated representations
    of these null alleles. This class provides functionality to:
    - Identify short null alleles
    - Distinguish null alleles from other allele types
    """

    def __init__(self, ard_instance: "ARD"):
        """Initialize the ShortNullHandler with an ARD instance

        Args:
            ard_instance: The main ARD object containing configuration and data
        """
        self.ard = ard_instance

    def is_shortnull(self, allele: str) -> bool:
        """Check if allele is a valid short null

        Short null alleles are abbreviated forms of null alleles that are
        recognized by the system. The check depends on both the allele being
        in the short nulls database and the configuration allowing short null reduction.

        Args:
            allele: Allele string to check

        Returns:
            True if the allele is a valid short null and short null reduction
            is enabled in configuration, False otherwise
        """
        return allele in self.ard.shortnulls and self.ard._config["reduce_shortnull"]

    def is_null(self, allele: str) -> bool:
        """Check if allele is a null allele

        Null alleles are identified by the 'N' suffix in HLA nomenclature,
        indicating they do not produce functional proteins. This method
        distinguishes true null alleles from MAC codes that might also end with 'N'.

        Args:
            allele: Allele string to check

        Returns:
            True if the allele is a null allele (ends with 'N' but is not a MAC code),
            False otherwise
        """
        return allele.endswith("N") and not self.ard.is_mac(allele)
