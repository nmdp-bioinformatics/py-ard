# -*- coding: utf-8 -*-

from .base_strategy import ReductionStrategy


class WStrategy(ReductionStrategy):
    """Strategy for W (WHO) reduction"""

    def reduce(self, allele: str) -> str:
        if self.ard._is_who_allele(allele):
            return allele
        if allele in self.ard.code_mappings.who_group:
            return self.ard.redux(
                "/".join(self.ard.code_mappings.who_group[allele]), "W"
            )
        else:
            return allele
