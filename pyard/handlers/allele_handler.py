# -*- coding: utf-8 -*-

from typing import TYPE_CHECKING

from ..constants import VALID_REDUCTION_TYPE
from ..reducers.reducer_factory import StrategyFactory

if TYPE_CHECKING:
    from ..ard import ARD


class AlleleHandler:
    """Handles core allele reduction logic using Strategy Pattern

    This class serves as the main handler for reducing HLA alleles to different
    resolution levels (G group, P group, lg, etc.). It uses the Strategy Pattern
    to delegate the actual reduction logic to specific strategy classes.
    """

    def __init__(self, ard_instance: "ARD"):
        """Initialize the AlleleReducer with an ARD instance

        Args:
            ard_instance: The main ARD object containing database connections
                         and configuration settings
        """
        self.ard = ard_instance
        # Factory that creates appropriate reduction strategy based on redux_type
        self.strategy_factory = StrategyFactory(ard_instance)

    def reduce_allele(
        self, allele: str, redux_type: VALID_REDUCTION_TYPE, re_ping=True
    ) -> str:
        """Core allele reduction logic using Strategy Pattern

        Reduces an HLA allele to the specified resolution level by delegating
        to the appropriate reduction strategy.

        Args:
            allele: HLA allele string to reduce (e.g., "A*01:01:01:01")
            redux_type: Type of reduction to perform (G, P, lg, lgx, W, exon, U2, S)
            re_ping: Whether to re-ping for P groups when G groups are unavailable

        Returns:
            Reduced allele string according to the specified redux_type
        """
        # Get the appropriate reduction strategy for the redux_type
        strategy = self.strategy_factory.get_strategy(redux_type)
        # Execute the reduction using the selected strategy
        return strategy.reduce(allele)

    def add_lg_suffix(self, redux_allele):
        """Add lg suffix to reduced allele - kept for backward compatibility

        Appends the appropriate suffix ('g' or 'ARS') to reduced alleles.
        Handles both single alleles and ambiguous allele lists separated by '/'.

        Args:
            redux_allele: Reduced allele string, may contain multiple alleles
                         separated by '/'

        Returns:
            Allele string with appropriate suffix added to each allele
        """
        # Handle ambiguous alleles (multiple alleles separated by '/')
        if "/" in redux_allele:
            return "/".join(
                [self.add_lg_suffix(allele) for allele in redux_allele.split("/")]
            )
        # Use 'ARS' suffix if configured, otherwise use 'g' suffix
        if self.ard.config.ars_as_lg_enabled:
            return redux_allele + "ARS"
        return redux_allele + "g"
