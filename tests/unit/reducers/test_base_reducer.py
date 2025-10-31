# -*- coding: utf-8 -*-

import pytest
from unittest.mock import Mock
from pyard.reducers.base_reducer import Reducer


class ConcreteReducer(Reducer):
    """Concrete implementation for testing abstract base class"""

    def reduce(self, allele: str) -> str:
        return f"reduced_{allele}"


def test_reducer_initialization():
    """Test that Reducer can be initialized with ARD instance"""
    mock_ard = Mock()
    reducer = ConcreteReducer(mock_ard)
    assert reducer.ard == mock_ard


def test_reducer_abstract_method():
    """Test that reduce method is implemented in concrete class"""
    mock_ard = Mock()
    reducer = ConcreteReducer(mock_ard)
    result = reducer.reduce("A*01:01")
    assert result == "reduced_A*01:01"


def test_reducer_cannot_be_instantiated():
    """Test that abstract Reducer class cannot be instantiated directly"""
    mock_ard = Mock()
    with pytest.raises(TypeError):
        Reducer(mock_ard)
