# -*- coding: utf-8 -*-

import pytest
from unittest.mock import Mock
from pyard.reducers.g_reducer import GGroupReducer


@pytest.fixture
def mock_ard():
    """Create mock ARD instance"""
    ard = Mock()
    ard.ars_mappings = Mock()
    ard.ars_mappings.g_group = {"A*01:01": "A*01:01:01G", "A*02:01": "A*02:01:02G"}
    ard.ars_mappings.dup_g = {"A*02:01": "A*02:01:01G/A*02:01:02G"}
    ard.ars_mappings.p_group = Mock()
    ard.is_valid_allele = Mock(return_value=True)
    return ard


def test_reduce_allele_in_g_group(mock_ard):
    """Test reduction of allele in G group mapping"""
    reducer = GGroupReducer(mock_ard)
    result = reducer.reduce("A*01:01")

    assert result == "A*01:01:01G"


def test_reduce_allele_in_dup_g(mock_ard):
    """Test reduction of allele in duplicate G group mapping"""
    reducer = GGroupReducer(mock_ard)
    result = reducer.reduce("A*02:01")

    assert result == "A*02:01:01G/A*02:01:02G"


def test_reduce_allele_not_in_g_group_calls_super(mock_ard):
    """Test that allele not in G group calls parent reduce method"""
    reducer = GGroupReducer(mock_ard)
    result = reducer.reduce("B*07:02")

    assert result == "B*07:02"
    mock_ard.is_valid_allele.assert_called_once_with("B*07:02")
