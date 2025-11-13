# -*- coding: utf-8 -*-

import pytest
from unittest.mock import Mock, patch
from pyard.reducers.exon_reducer import ExonReducer


@pytest.fixture
def mock_ard():
    """Create mock ARD instance"""
    ard = Mock()
    ard.ars_mappings = Mock()
    ard.ars_mappings.exon_group = {"A*01:01:01": "A*01:01:01"}
    ard.is_shortnull = Mock()
    ard.redux = Mock()
    return ard


def test_reduce_allele_in_exon_group(mock_ard):
    """Test reduction of allele in exon group mapping"""
    reducer = ExonReducer(mock_ard)
    result = reducer.reduce("A*01:01:01")

    assert result == "A*01:01:01"


def test_reduce_allele_with_expression_char_shortnull(mock_ard):
    """Test reduction of allele with expression character that is shortnull"""
    mock_ard.ars_mappings.exon_group = {"A*01:01:01N": "A*01:01:01"}
    mock_ard.is_shortnull.return_value = True

    with patch("pyard.reducers.exon_reducer.expression_chars", "N"):
        reducer = ExonReducer(mock_ard)
        result = reducer.reduce("A*01:01:01N")

    assert result == "A*01:01:01N"
    mock_ard.is_shortnull.assert_called_once_with("A*01:01:01N")


def test_reduce_allele_with_expression_char_not_shortnull(mock_ard):
    """Test reduction of allele with expression character that is not shortnull"""
    mock_ard.ars_mappings.exon_group = {"A*01:01:01Q": "A*01:01:01"}
    mock_ard.is_shortnull.return_value = False

    with patch("pyard.reducers.exon_reducer.expression_chars", "Q"):
        reducer = ExonReducer(mock_ard)
        result = reducer.reduce("A*01:01:01Q")

    assert result == "A*01:01:01"


def test_reduce_allele_not_in_exon_group_w_redux_same(mock_ard):
    """Test reduction when W redux returns same allele"""
    mock_ard.redux.return_value = "B*07:02"

    reducer = ExonReducer(mock_ard)
    result = reducer.reduce("B*07:02")

    assert result == "B*07:02"
    mock_ard.redux.assert_called_once_with("B*07:02", "W")


def test_reduce_allele_not_in_exon_group_w_redux_two_field(mock_ard):
    """Test reduction when W redux returns 2-field allele"""
    mock_ard.redux.return_value = "B*07:02"

    reducer = ExonReducer(mock_ard)
    result = reducer.reduce("B*07:02:01")

    assert result == "B*07:02:01"


def test_reduce_allele_not_in_exon_group_recursive(mock_ard):
    """Test recursive reduction when W redux returns different allele"""
    mock_ard.redux.side_effect = ["B*07:02:01:01", "B*07:02:01"]

    reducer = ExonReducer(mock_ard)
    result = reducer.reduce("B*07:02:XX")

    assert result == "B*07:02:01"
    assert mock_ard.redux.call_count == 2
