# -*- coding: utf-8 -*-
from typing import override

from .base_strategy import ReductionStrategy


class PGroupStrategy(ReductionStrategy):
    """Strategy for P group reduction"""

    @override
    def reduce(self, allele: str) -> str:
        if allele in self.ard.ars_mappings.p_group:
            return self.ard.ars_mappings.p_group[allele]

        return super().reduce(allele)
