# -*- coding: utf-8 -*-

from typing import TYPE_CHECKING

from ..constants import VALID_REDUCTION_TYPE
from ..reducers.reducer_factory import StrategyFactory

if TYPE_CHECKING:
    from ..ard import ARD


class AlleleReducer:
    """Handles core allele reduction logic using Strategy Pattern"""

    def __init__(self, ard_instance: "ARD"):
        self.ard = ard_instance
        self.strategy_factory = StrategyFactory(ard_instance)

    def reduce_allele(
        self, allele: str, redux_type: VALID_REDUCTION_TYPE, re_ping=True
    ) -> str:
        """Core allele reduction logic using Strategy Pattern"""
        strategy = self.strategy_factory.get_strategy(redux_type)
        return strategy.reduce(allele)

    def add_lg_suffix(self, redux_allele):
        """Add lg suffix to reduced allele - kept for backward compatibility"""
        if "/" in redux_allele:
            return "/".join(
                [self.add_lg_suffix(allele) for allele in redux_allele.split("/")]
            )
        if self.ard._config["ARS_as_lg"]:
            return redux_allele + "ARS"
        return redux_allele + "g"
