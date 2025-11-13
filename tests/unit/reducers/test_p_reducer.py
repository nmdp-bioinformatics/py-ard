# -*- coding: utf-8 -*-

import pytest
from unittest.mock import Mock
from pyard.reducers.p_reducer import PGroupReducer


@pytest.fixture
def mock_ard():
    """Create mock ARD instance"""
    ard = Mock()
    ard.ars_mappings = Mock()
    ard.ars_mappings.p_group = {"A*01:01": "A*01:01P"}
    ard.is_valid_allele = Mock(return_value=True)
    return ard


def test_reduce_allele_in_p_group(mock_ard):
    """Test reduction of allele in P group mapping"""
    reducer = PGroupReducer(mock_ard)
    result = reducer.reduce("A*01:01")

    assert result == "A*01:01P"


def test_reduce_allele_not_in_p_group_calls_super(mock_ard):
    """Test that allele not in P group calls parent reduce method"""
    reducer = PGroupReducer(mock_ard)
    result = reducer.reduce("B*07:02")

    assert result == "B*07:02"
    mock_ard.is_valid_allele.assert_called_once_with("B*07:02")
