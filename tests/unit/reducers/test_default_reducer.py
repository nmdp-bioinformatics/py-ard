# -*- coding: utf-8 -*-

import pytest
from unittest.mock import Mock
from pyard.reducers.default_reducer import DefaultReducer
from pyard.exceptions import InvalidAlleleError


@pytest.fixture
def mock_ard():
    """Create mock ARD instance"""
    ard = Mock()
    ard.ars_mappings = Mock()
    ard.ars_mappings.p_group = Mock()
    ard.ars_mappings.g_group = Mock()
    ard.is_valid_allele = Mock()
    return ard


def test_reduce_p_group_allele(mock_ard):
    """Test reduction of P group allele"""
    mock_ard.ars_mappings.p_group.values.return_value = ["A*01:01P"]

    reducer = DefaultReducer(mock_ard)
    result = reducer.reduce("A*01:01P")

    assert result == "A*01:01P"


def test_reduce_g_group_allele(mock_ard):
    """Test reduction of G group allele"""
    mock_ard.ars_mappings.g_group.values.return_value = ["A*01:01G"]

    reducer = DefaultReducer(mock_ard)
    result = reducer.reduce("A*01:01G")

    assert result == "A*01:01G"


def test_reduce_valid_allele_in_db(mock_ard):
    """Test reduction of valid allele in database"""
    mock_ard.is_valid_allele.return_value = True

    reducer = DefaultReducer(mock_ard)
    result = reducer.reduce("A*01:01")

    assert result == "A*01:01"
    mock_ard.is_valid_allele.assert_called_once_with("A*01:01")


def test_reduce_invalid_allele_raises_error(mock_ard):
    """Test that invalid allele raises InvalidAlleleError"""
    mock_ard.ars_mappings.p_group.values.return_value = []
    mock_ard.ars_mappings.g_group.values.return_value = []
    mock_ard.is_valid_allele.return_value = False

    reducer = DefaultReducer(mock_ard)

    with pytest.raises(InvalidAlleleError, match="INVALID is an invalid allele"):
        reducer.reduce("INVALID")
