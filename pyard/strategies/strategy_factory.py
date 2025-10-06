# -*- coding: utf-8 -*-

from typing import Dict, TYPE_CHECKING

from .default_strategy import DefaultStrategy
from .base_strategy import ReductionStrategy
from .exon_strategy import ExonStrategy
from .g_strategy import GGroupStrategy
from .lg_strategy import LGStrategy, LGXStrategy
from .p_strategy import PGroupStrategy
from .s_strategy import SStrategy
from .u2_strategy import U2Strategy
from .w_strategy import WStrategy
from ..constants import VALID_REDUCTION_TYPE

if TYPE_CHECKING:
    from ..ard import ARD


class StrategyFactory:
    """Factory for creating reduction strategies"""

    def __init__(self, ard_instance: "ARD"):
        self.ard = ard_instance
        self._strategies: Dict[str, ReductionStrategy] = {}
        self._initialize_strategies()

    def _initialize_strategies(self):
        """Initialize all reduction strategies"""
        self._strategies = {
            "G": GGroupStrategy(self.ard),
            "P": PGroupStrategy(self.ard),
            "lg": LGStrategy(self.ard),
            "lgx": LGXStrategy(self.ard),
            "W": WStrategy(self.ard),
            "exon": ExonStrategy(self.ard),
            "U2": U2Strategy(self.ard),
            "S": SStrategy(self.ard),
            "default": DefaultStrategy(self.ard),
        }

    def get_strategy(self, redux_type: VALID_REDUCTION_TYPE) -> ReductionStrategy:
        """Get the appropriate strategy for the reduction type"""
        return self._strategies.get(redux_type, self._strategies["default"])
