# -*- coding: utf-8 -*-
from typing_extensions import override

from .default_strategy import DefaultStrategy


class GGroupStrategy(DefaultStrategy):
    """Strategy for G group reduction"""

    @override
    def reduce(self, allele: str) -> str:
        if allele in self.ard.ars_mappings.g_group:
            if allele in self.ard.ars_mappings.dup_g:
                return self.ard.ars_mappings.dup_g[allele]
            else:
                return self.ard.ars_mappings.g_group[allele]

        return super().reduce(allele)
