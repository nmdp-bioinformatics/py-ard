# -*- coding: utf-8 -*-

from typing import Dict, TYPE_CHECKING

from .default_reducer import DefaultReducer
from .base_reducer import Reducer
from .exon_reducer import ExonReducer
from .g_reducer import GGroupReducer
from .lg_reducer import LGReducer, LGXReducer
from .p_reducer import PGroupReducer
from .s_reducer import SReducer
from .u2_reducer import U2Reducer
from .w_reducer import WReducer
from ..constants import VALID_REDUCTION_TYPE

if TYPE_CHECKING:
    from ..ard import ARD


class StrategyFactory:
    """Factory for creating reduction strategies"""

    def __init__(self, ard_instance: "ARD"):
        self.ard = ard_instance
        self._strategies: Dict[str, Reducer] = {}
        self._initialize_strategies()

    def _initialize_strategies(self):
        """Initialize all reduction strategies"""
        self._strategies = {
            "G": GGroupReducer(self.ard),
            "P": PGroupReducer(self.ard),
            "lg": LGReducer(self.ard),
            "lgx": LGXReducer(self.ard),
            "W": WReducer(self.ard),
            "exon": ExonReducer(self.ard),
            "U2": U2Reducer(self.ard),
            "S": SReducer(self.ard),
            "default": DefaultReducer(self.ard),
        }

    def get_strategy(self, redux_type: VALID_REDUCTION_TYPE) -> Reducer:
        """Get the appropriate strategy for the reduction type"""
        return self._strategies.get(redux_type, self._strategies["default"])
