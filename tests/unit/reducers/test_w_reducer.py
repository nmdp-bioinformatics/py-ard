# -*- coding: utf-8 -*-

import pytest
from unittest.mock import Mock
from pyard.reducers.w_reducer import WReducer


@pytest.fixture
def mock_ard():
    """Create mock ARD instance"""
    ard = Mock()
    ard._is_who_allele = Mock()
    ard.code_mappings = Mock()
    ard.code_mappings.who_group = {"A*01:XX": ["A*01:01", "A*01:02"]}
    ard.redux = Mock()
    return ard


def test_reduce_who_allele_returns_unchanged(mock_ard):
    """Test that WHO allele is returned unchanged"""
    mock_ard._is_who_allele.return_value = True

    reducer = WReducer(mock_ard)
    result = reducer.reduce("A*01:01:01:01")

    assert result == "A*01:01:01:01"
    mock_ard._is_who_allele.assert_called_once_with("A*01:01:01:01")


def test_reduce_allele_in_who_group(mock_ard):
    """Test reduction of allele in WHO group mapping"""
    mock_ard._is_who_allele.return_value = False
    mock_ard.redux.return_value = "A*01:01/A*01:02"

    reducer = WReducer(mock_ard)
    result = reducer.reduce("A*01:XX")

    assert result == "A*01:01/A*01:02"
    mock_ard.redux.assert_called_once_with("A*01:01/A*01:02", "W")


def test_reduce_allele_not_in_who_group(mock_ard):
    """Test that allele not in WHO group is returned unchanged"""
    mock_ard._is_who_allele.return_value = False

    reducer = WReducer(mock_ard)
    result = reducer.reduce("B*07:02")

    assert result == "B*07:02"
