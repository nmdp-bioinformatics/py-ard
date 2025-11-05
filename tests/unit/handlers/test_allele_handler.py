# -*- coding: utf-8 -*-

import pytest
from unittest.mock import Mock, MagicMock

from pyard import ARDConfig
from pyard.handlers.allele_handler import AlleleHandler


class TestAlleleHandler:
    """Test cases for AlleleHandler class"""

    @pytest.fixture
    def mock_ard(self):
        """Create mock ARD instance"""
        ard = Mock()
        ard.config = ARDConfig.from_dict({"ARS_as_lg": False})
        return ard

    @pytest.fixture
    def mock_strategy_factory(self):
        """Create mock strategy factory"""
        factory = Mock()
        mock_strategy = Mock()
        mock_strategy.reduce.return_value = "A*01:01G"
        factory.get_strategy.return_value = mock_strategy
        return factory

    @pytest.fixture
    def allele_handler(self, mock_ard, mock_strategy_factory):
        """Create AlleleHandler instance with mocked dependencies"""
        handler = AlleleHandler(mock_ard)
        handler.strategy_factory = mock_strategy_factory
        return handler

    def test_init(self, mock_ard):
        """Test AlleleHandler initialization"""
        handler = AlleleHandler(mock_ard)
        assert handler.ard == mock_ard
        assert handler.strategy_factory is not None

    def test_reduce_allele(self, allele_handler, mock_strategy_factory):
        """Test reduce_allele method"""
        result = allele_handler.reduce_allele("A*01:01:01", "G")

        mock_strategy_factory.get_strategy.assert_called_once_with("G")
        mock_strategy_factory.get_strategy.return_value.reduce.assert_called_once_with(
            "A*01:01:01"
        )
        assert result == "A*01:01G"

    def test_add_lg_suffix_single_allele_default(self, allele_handler):
        """Test add_lg_suffix with single allele using default 'g' suffix"""
        result = allele_handler.add_lg_suffix("A*01:01")
        assert result == "A*01:01g"

    def test_add_lg_suffix_single_allele_ars(self, mock_ard):
        """Test add_lg_suffix with single allele using ARS suffix"""
        mock_ard.config = ARDConfig.from_dict({"ARS_as_lg": True})
        handler = AlleleHandler(mock_ard)
        result = handler.add_lg_suffix("A*01:01")
        assert result == "A*01:01ARS"

    def test_add_lg_suffix_multiple_alleles(self, allele_handler):
        """Test add_lg_suffix with multiple alleles separated by '/'"""
        result = allele_handler.add_lg_suffix("A*01:01/A*01:02")
        assert result == "A*01:01g/A*01:02g"

    def test_add_lg_suffix_multiple_alleles_ars(self, mock_ard):
        """Test add_lg_suffix with multiple alleles using ARS suffix"""
        mock_ard.config = ARDConfig.from_dict({"ARS_as_lg": True})
        handler = AlleleHandler(mock_ard)
        result = handler.add_lg_suffix("A*01:01/A*01:02")
        assert result == "A*01:01ARS/A*01:02ARS"
