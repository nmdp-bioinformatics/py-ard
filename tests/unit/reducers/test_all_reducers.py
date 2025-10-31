# -*- coding: utf-8 -*-

import pytest
from unittest.mock import Mock
from pyard.reducers import (
    Reducer,
    GGroupReducer,
    PGroupReducer,
    LGReducer,
    LGXReducer,
    WReducer,
    ExonReducer,
    U2Reducer,
    SReducer,
    DefaultReducer,
    StrategyFactory,
)


@pytest.fixture
def mock_ard():
    """Create comprehensive mock ARD instance"""
    ard = Mock()
    ard.ars_mappings = Mock()
    ard.ars_mappings.g_group = {"A*01:01": "A*01:01:01G"}
    ard.ars_mappings.p_group = {"A*01:01": "A*01:01P"}
    ard.ars_mappings.lgx_group = {"A*01:01:01": "A*01:01"}
    ard.ars_mappings.exon_group = {"A*01:01:01": "A*01:01:01"}
    ard.ars_mappings.dup_g = {}
    ard.code_mappings = Mock()
    ard.code_mappings.who_group = {}
    ard.db_connection = Mock()
    ard._config = {"ARS_as_lg": False}
    ard._is_allele_in_db = Mock(return_value=True)
    ard._is_who_allele = Mock(return_value=False)
    ard._redux_allele = Mock()
    ard.redux = Mock()
    ard.is_shortnull = Mock(return_value=False)
    ard.smart_sort_comparator = Mock()
    return ard


def test_all_reducers_inherit_from_base(mock_ard):
    """Test that all reducer classes inherit from Reducer base class"""
    reducers = [
        GGroupReducer(mock_ard),
        PGroupReducer(mock_ard),
        LGReducer(mock_ard),
        LGXReducer(mock_ard),
        WReducer(mock_ard),
        ExonReducer(mock_ard),
        U2Reducer(mock_ard),
        SReducer(mock_ard),
        DefaultReducer(mock_ard),
    ]

    for reducer in reducers:
        assert isinstance(reducer, Reducer)
        assert hasattr(reducer, "reduce")
        assert hasattr(reducer, "ard")


def test_strategy_factory_creates_all_reducers(mock_ard):
    """Test that StrategyFactory can create all reducer types"""
    factory = StrategyFactory(mock_ard)

    strategies = ["G", "P", "lg", "lgx", "W", "exon", "U2", "S", "default"]

    for strategy_type in strategies:
        strategy = factory.get_strategy(strategy_type)
        assert isinstance(strategy, Reducer)
        assert strategy.ard == mock_ard


def test_all_reducers_have_ard_instance(mock_ard):
    """Test that all reducers store ARD instance correctly"""
    reducers = [
        GGroupReducer(mock_ard),
        PGroupReducer(mock_ard),
        LGReducer(mock_ard),
        LGXReducer(mock_ard),
        WReducer(mock_ard),
        ExonReducer(mock_ard),
        U2Reducer(mock_ard),
        SReducer(mock_ard),
        DefaultReducer(mock_ard),
    ]

    for reducer in reducers:
        assert reducer.ard == mock_ard
