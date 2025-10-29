# -*- coding: utf-8 -*-
from typing import override

from .default_reducer import DefaultReducer


class PGroupReducer(DefaultReducer):
    """Strategy for P group reduction"""

    # @override
    def reduce(self, allele: str) -> str:
        if allele in self.ard.ars_mappings.p_group:
            return self.ard.ars_mappings.p_group[allele]

        return super().reduce(allele)
