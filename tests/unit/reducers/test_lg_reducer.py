# -*- coding: utf-8 -*-

import pytest
from unittest.mock import Mock
from pyard.reducers.lg_reducer import LGXReducer, LGReducer


@pytest.fixture
def mock_ard():
    """Create mock ARD instance"""
    ard = Mock()
    ard.ars_mappings = Mock()
    ard.ars_mappings.lgx_group = {"A*01:01:01": "A*01:01"}
    ard._config = {"ARS_as_lg": False}
    return ard


class TestLGXReducer:
    def test_reduce_allele_in_lgx_group(self, mock_ard):
        """Test reduction of allele in LGX group mapping"""
        reducer = LGXReducer(mock_ard)
        result = reducer.reduce("A*01:01:01")

        assert result == "A*01:01"

    def test_reduce_allele_not_in_lgx_group(self, mock_ard):
        """Test reduction of allele not in LGX group returns first 2 fields"""
        reducer = LGXReducer(mock_ard)
        result = reducer.reduce("B*07:02:01:03")

        assert result == "B*07:02"

    def test_reduce_two_field_allele(self, mock_ard):
        """Test reduction of already 2-field allele"""
        reducer = LGXReducer(mock_ard)
        result = reducer.reduce("C*01:02")

        assert result == "C*01:02"


class TestLGReducer:
    def test_reduce_single_allele_with_g_suffix(self, mock_ard):
        """Test reduction adds 'g' suffix to single allele"""
        reducer = LGReducer(mock_ard)
        result = reducer.reduce("A*01:01:01")

        assert result == "A*01:01g"

    def test_reduce_single_allele_with_ars_suffix(self, mock_ard):
        """Test reduction adds 'ARS' suffix when configured"""
        mock_ard._config = {"ARS_as_lg": True}
        reducer = LGReducer(mock_ard)
        result = reducer.reduce("A*01:01:01")

        assert result == "A*01:01ARS"

    def test_reduce_multiple_alleles_with_g_suffix(self, mock_ard):
        """Test reduction adds 'g' suffix to multiple alleles"""
        mock_ard.ars_mappings.lgx_group = {"A*01:01:01": "A*01:01/A*01:02"}
        reducer = LGReducer(mock_ard)
        result = reducer.reduce("A*01:01:01")

        assert result == "A*01:01g/A*01:02g"
