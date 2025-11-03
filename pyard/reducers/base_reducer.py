# -*- coding: utf-8 -*-
"""
Abstract Base Class for HLA Allele Reduction Strategies.

This module defines the Reducer abstract base class that serves as the foundation
for all HLA allele reduction strategies in py-ard. It implements the Strategy
design pattern to allow interchangeable reduction algorithms.
"""

from abc import ABC, abstractmethod

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from ..ard import ARD


class Reducer(ABC):
    """
    Abstract base class for all HLA allele reduction strategies.

    This class implements the Strategy design pattern, providing a common
    interface for all reduction strategies while allowing each strategy to
    implement its own specific reduction logic. All concrete reduction
    strategies must inherit from this class and implement the reduce method.

    The Reducer class serves as the foundation for various HLA reduction types:
    - G Group reduction (GGroupReducer)
    - P Group reduction (PGroupReducer)
    - LG/LGX reduction (LGReducer, LGXReducer)
    - WHO reduction (WReducer)
    - Serology reduction (SReducer)
    - U2 reduction (U2Reducer)
    - Exon reduction (ExonReducer)
    - Default validation (DefaultReducer)

    Design Pattern:
        This class implements the Strategy pattern, allowing the ARD system
        to switch between different reduction algorithms at runtime based
        on the requested reduction type.

    Attributes:
        ard (ARD): The ARD instance containing all mapping data, database
                   connections, and utility methods needed for reduction.

    Example:
        >>> class CustomReducer(Reducer):
        ...     def reduce(self, allele: str) -> str:
        ...         # Custom reduction logic here
        ...         return processed_allele
        ...
        >>> reducer = CustomReducer(ard_instance)
        >>> result = reducer.reduce("A*01:01:01:01")
    """

    def __init__(self, ard_instance: "ARD"):
        """
        Initialize the reducer with an ARD instance.

        Args:
            ard_instance (ARD): The ARD instance containing mapping data,
                               database connections, and utility methods
                               required for allele reduction operations.

        Note:
            The ARD instance provides access to:
            - ARS mappings (G groups, P groups, LGX groups, etc.)
            - Code mappings (WHO groups, MAC codes, etc.)
            - Database connections for serology and other lookups
            - Utility methods for validation and processing
        """
        self.ard = ard_instance

    @abstractmethod
    def reduce(self, allele: str) -> str:
        """
        Reduce an HLA allele according to this strategy's specific logic.

        This is the core method that must be implemented by all concrete
        reduction strategies. Each implementation should define how to
        transform the input allele according to its specific reduction rules.

        Args:
            allele (str): The HLA allele to reduce (e.g., "A*01:01:01:01")

        Returns:
            str: The reduced allele according to this strategy's rules
                 (e.g., "A*01:01:01G" for G group reduction)

        Raises:
            NotImplementedError: If called on the abstract base class directly
            InvalidAlleleError: May be raised by concrete implementations
                               for invalid input alleles

        Examples:
            This method's behavior depends on the concrete implementation:

            >>> g_reducer = GGroupReducer(ard)
            >>> g_reducer.reduce("A*01:01:01:01")
            "A*01:01:01G"

            >>> lg_reducer = LGReducer(ard)
            >>> lg_reducer.reduce("A*01:01:01:01")
            "A*01:01g"

            >>> s_reducer = SReducer(ard)
            >>> s_reducer.reduce("A*01:01:01:01")
            "A1"

        Note:
            Concrete implementations should handle edge cases appropriately
            and may use the ARD instance's methods and data for processing.
        """
        pass
