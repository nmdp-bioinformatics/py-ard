# -*- coding: utf-8 -*-

import pytest
from unittest.mock import Mock, patch
from pyard.reducers.u2_reducer import U2Reducer


@pytest.fixture
def mock_ard():
    """Create mock ARD instance"""
    ard = Mock()
    ard._is_allele_in_db = Mock()
    ard._redux_allele = Mock()
    return ard


def test_reduce_two_field_allele_unchanged(mock_ard):
    """Test that 2-field allele is returned unchanged"""
    reducer = U2Reducer(mock_ard)
    result = reducer.reduce("A*01:01")

    assert result == "A*01:01"


def test_reduce_multi_field_allele_unambiguous(mock_ard):
    """Test reduction of multi-field allele that is unambiguous at 2-field level"""
    mock_ard._is_allele_in_db.return_value = True

    with patch("pyard.reducers.u2_reducer.get_n_field_allele", return_value="A*01:01"):
        reducer = U2Reducer(mock_ard)
        result = reducer.reduce("A*01:01:01:01")

    assert result == "A*01:01"
    mock_ard._is_allele_in_db.assert_called_once_with("A*01:01")


def test_reduce_multi_field_allele_ambiguous(mock_ard):
    """Test reduction of multi-field allele that is ambiguous at 2-field level"""
    mock_ard._is_allele_in_db.return_value = False
    mock_ard._redux_allele.return_value = "A*01:01"

    with patch("pyard.reducers.u2_reducer.get_n_field_allele", return_value="A*01:01"):
        reducer = U2Reducer(mock_ard)
        result = reducer.reduce("A*01:01:01:01")

    assert result == "A*01:01"
    mock_ard._redux_allele.assert_called_once_with("A*01:01:01:01", "lgx")
