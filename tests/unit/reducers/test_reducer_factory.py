# -*- coding: utf-8 -*-

import pytest
from unittest.mock import Mock
from pyard.reducers.reducer_factory import StrategyFactory
from pyard.reducers.g_reducer import GGroupReducer
from pyard.reducers.p_reducer import PGroupReducer
from pyard.reducers.lg_reducer import LGReducer, LGXReducer
from pyard.reducers.w_reducer import WReducer
from pyard.reducers.exon_reducer import ExonReducer
from pyard.reducers.u2_reducer import U2Reducer
from pyard.reducers.s_reducer import SReducer
from pyard.reducers.default_reducer import DefaultReducer


@pytest.fixture
def mock_ard():
    """Create mock ARD instance"""
    return Mock()


def test_strategy_factory_initialization(mock_ard):
    """Test that StrategyFactory initializes with all strategies"""
    factory = StrategyFactory(mock_ard)

    assert factory.ard == mock_ard
    assert len(factory._strategies) == 9


def test_get_g_strategy(mock_ard):
    """Test getting G group strategy"""
    factory = StrategyFactory(mock_ard)
    strategy = factory.get_strategy("G")

    assert isinstance(strategy, GGroupReducer)


def test_get_p_strategy(mock_ard):
    """Test getting P group strategy"""
    factory = StrategyFactory(mock_ard)
    strategy = factory.get_strategy("P")

    assert isinstance(strategy, PGroupReducer)


def test_get_lg_strategy(mock_ard):
    """Test getting lg strategy"""
    factory = StrategyFactory(mock_ard)
    strategy = factory.get_strategy("lg")

    assert isinstance(strategy, LGReducer)


def test_get_lgx_strategy(mock_ard):
    """Test getting lgx strategy"""
    factory = StrategyFactory(mock_ard)
    strategy = factory.get_strategy("lgx")

    assert isinstance(strategy, LGXReducer)


def test_get_w_strategy(mock_ard):
    """Test getting W strategy"""
    factory = StrategyFactory(mock_ard)
    strategy = factory.get_strategy("W")

    assert isinstance(strategy, WReducer)


def test_get_exon_strategy(mock_ard):
    """Test getting exon strategy"""
    factory = StrategyFactory(mock_ard)
    strategy = factory.get_strategy("exon")

    assert isinstance(strategy, ExonReducer)


def test_get_u2_strategy(mock_ard):
    """Test getting U2 strategy"""
    factory = StrategyFactory(mock_ard)
    strategy = factory.get_strategy("U2")

    assert isinstance(strategy, U2Reducer)


def test_get_s_strategy(mock_ard):
    """Test getting S strategy"""
    factory = StrategyFactory(mock_ard)
    strategy = factory.get_strategy("S")

    assert isinstance(strategy, SReducer)


def test_get_default_strategy(mock_ard):
    """Test getting default strategy"""
    factory = StrategyFactory(mock_ard)
    strategy = factory.get_strategy("default")

    assert isinstance(strategy, DefaultReducer)


def test_get_unknown_strategy_returns_default(mock_ard):
    """Test that unknown strategy returns default strategy"""
    factory = StrategyFactory(mock_ard)
    strategy = factory.get_strategy("UNKNOWN")

    assert isinstance(strategy, DefaultReducer)
