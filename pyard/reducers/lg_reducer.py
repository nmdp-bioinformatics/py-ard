# -*- coding: utf-8 -*-
from .base_reducer import Reducer


class LGXReducer(Reducer):
    """Strategy for lgx reduction"""

    # @override
    def reduce(self, allele: str) -> str:
        if allele in self.ard.ars_mappings.lgx_group:
            return self.ard.ars_mappings.lgx_group[allele]
        else:
            # Return allele with only first 2 fields
            return ":".join(allele.split(":")[0:2])


class LGReducer(Reducer):
    """Strategy for lg reduction (lgx + g suffix)"""

    # @override
    def reduce(self, allele: str) -> str:
        lgx_strategy = LGXReducer(self.ard)
        redux_allele = lgx_strategy.reduce(allele)
        return self._add_lg_suffix(redux_allele)

    def _add_lg_suffix(self, redux_allele: str) -> str:
        """Add lg suffix to reduced allele"""
        if "/" in redux_allele:
            return "/".join(
                [self._add_lg_suffix(allele) for allele in redux_allele.split("/")]
            )
        if self.ard._config["ARS_as_lg"]:
            return redux_allele + "ARS"
        return redux_allele + "g"
