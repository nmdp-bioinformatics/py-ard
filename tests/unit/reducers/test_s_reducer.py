# -*- coding: utf-8 -*-

import pytest
from unittest.mock import Mock, patch
from pyard.reducers.s_reducer import SReducer


@pytest.fixture
def mock_ard():
    """Create mock ARD instance"""
    ard = Mock()
    ard.db_connection = Mock()
    ard._redux_allele = Mock()
    ard.redux = Mock()
    ard.smart_sort_comparator = Mock()
    return ard


def test_reduce_two_field_allele(mock_ard):
    """Test reduction of 2-field allele"""
    mock_ard._redux_allele.return_value = "A*01:01"
    mock_ard.smart_sort_comparator.return_value = 0

    serology_mapping = {"A1": "A*01:01/A*01:02"}

    with patch("pyard.reducers.s_reducer.is_2_field_allele", return_value=True), patch(
        "pyard.reducers.s_reducer.db.find_serology_for_allele",
        return_value=serology_mapping,
    ), patch("functools.cmp_to_key"):
        reducer = SReducer(mock_ard)
        result = reducer.reduce("A*01:01")

    assert result == "A1"


def test_reduce_non_two_field_allele(mock_ard):
    """Test reduction of non-2-field allele"""
    mock_ard.smart_sort_comparator.return_value = 0

    serology_mapping = {"A1": "A*01:01:01/A*01:02:01"}

    with patch("pyard.reducers.s_reducer.is_2_field_allele", return_value=False), patch(
        "pyard.reducers.s_reducer.db.find_serology_for_allele",
        return_value=serology_mapping,
    ), patch("functools.cmp_to_key"):
        reducer = SReducer(mock_ard)
        result = reducer.reduce("A*01:01:01")

    assert result == "A1"


def test_reduce_multiple_serology_matches(mock_ard):
    """Test reduction with multiple serology matches"""
    mock_ard.smart_sort_comparator.return_value = 0

    serology_mapping = {"A1": "A*01:01/A*01:02", "A36": "A*01:01/A*36:01"}

    with patch("pyard.reducers.s_reducer.is_2_field_allele", return_value=False), patch(
        "pyard.reducers.s_reducer.db.find_serology_for_allele",
        return_value=serology_mapping,
    ), patch("functools.cmp_to_key", side_effect=lambda x: x):
        reducer = SReducer(mock_ard)
        result = reducer.reduce("A*01:01")

    # Should return sorted serology codes
    assert "A1" in result and "A36" in result
