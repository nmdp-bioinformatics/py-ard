# -*- coding: utf-8 -*-

from abc import ABC, abstractmethod
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from ..ard import ARD


class ReductionStrategy(ABC):
    """Base class for all reduction strategies"""

    def __init__(self, ard_instance: "ARD"):
        self.ard = ard_instance

    @abstractmethod
    def reduce(self, allele: str) -> str:
        """Reduce allele according to this strategy"""
        pass
