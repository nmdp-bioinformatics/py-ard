# -*- coding: utf-8 -*-

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from ..ard import ARD


class ShortNullHandler:
    """Handles short null allele operations"""

    def __init__(self, ard_instance: "ARD"):
        self.ard = ard_instance

    def is_shortnull(self, allele: str) -> bool:
        """Check if allele is a valid short null"""
        return allele in self.ard.shortnulls and self.ard._config["reduce_shortnull"]

    def is_null(self, allele: str) -> bool:
        """Check if allele is a null allele"""
        return allele.endswith("N") and not self.ard.is_mac(allele)
