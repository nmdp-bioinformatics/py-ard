# -*- coding: utf-8 -*-

import pytest
from unittest.mock import Mock

from pyard.handlers.shortnull_handler import ShortNullHandler


class TestShortNullHandler:
    """Test cases for ShortNullHandler class"""

    @pytest.fixture
    def mock_ard(self):
        """Create mock ARD instance"""
        ard = Mock()
        ard._config = {"reduce_shortnull": True}
        ard.shortnulls = {"A*01:01N", "B*07:02N"}
        ard.is_mac.return_value = False
        return ard

    @pytest.fixture
    def shortnull_handler(self, mock_ard):
        """Create ShortNullHandler instance"""
        return ShortNullHandler(mock_ard)

    def test_init(self, mock_ard):
        """Test ShortNullHandler initialization"""
        handler = ShortNullHandler(mock_ard)
        assert handler.ard == mock_ard

    def test_is_shortnull_valid_with_config_enabled(self, shortnull_handler):
        """Test is_shortnull with valid short null and config enabled"""
        result = shortnull_handler.is_shortnull("A*01:01N")
        assert result is True

    def test_is_shortnull_valid_with_config_disabled(self, mock_ard):
        """Test is_shortnull with valid short null but config disabled"""
        mock_ard._config["reduce_shortnull"] = False
        handler = ShortNullHandler(mock_ard)

        result = handler.is_shortnull("A*01:01N")
        assert result is False

    def test_is_shortnull_invalid_allele(self, shortnull_handler):
        """Test is_shortnull with allele not in shortnulls set"""
        result = shortnull_handler.is_shortnull("A*02:01N")
        assert result is False

    def test_is_shortnull_non_null_allele(self, shortnull_handler):
        """Test is_shortnull with non-null allele"""
        result = shortnull_handler.is_shortnull("A*01:01")
        assert result is False

    def test_is_null_valid_null_allele(self, shortnull_handler):
        """Test is_null with valid null allele (ends with N)"""
        result = shortnull_handler.is_null("A*01:01N")
        assert result is True

    def test_is_null_non_null_allele(self, shortnull_handler):
        """Test is_null with non-null allele"""
        result = shortnull_handler.is_null("A*01:01")
        assert result is False

    def test_is_null_mac_code_ending_with_n(self, shortnull_handler):
        """Test is_null with MAC code ending with N (should return False)"""
        shortnull_handler.ard.is_mac.return_value = True

        result = shortnull_handler.is_null("A*01:AN")
        assert result is False

    def test_is_null_allele_ending_with_n_not_mac(self, shortnull_handler):
        """Test is_null with allele ending with N that is not a MAC code"""
        shortnull_handler.ard.is_mac.return_value = False

        result = shortnull_handler.is_null("A*01:01N")
        assert result is True

    @pytest.mark.parametrize(
        "allele,in_shortnulls,config_enabled,expected",
        [
            ("A*01:01N", True, True, True),
            ("A*01:01N", True, False, False),
            ("A*01:01N", False, True, False),
            ("A*01:01N", False, False, False),
            (
                "A*01:01",
                True,
                True,
                True,
            ),  # If allele is in shortnulls set and config enabled, returns True
            ("A*01:01", False, True, False),
        ],
    )
    def test_is_shortnull_combinations(
        self, mock_ard, allele, in_shortnulls, config_enabled, expected
    ):
        """Test is_shortnull with various combinations of conditions"""
        mock_ard._config["reduce_shortnull"] = config_enabled
        mock_ard.shortnulls = {allele} if in_shortnulls else set()
        handler = ShortNullHandler(mock_ard)

        result = handler.is_shortnull(allele)
        assert result == expected

    @pytest.mark.parametrize(
        "allele,ends_with_n,is_mac_code,expected",
        [
            ("A*01:01N", True, False, True),
            ("A*01:01N", True, True, False),
            ("A*01:01", False, False, False),
            ("A*01:01", False, True, False),
            ("A*01:AN", True, True, False),
            ("A*01:AN", True, False, True),
        ],
    )
    def test_is_null_combinations(
        self, mock_ard, allele, ends_with_n, is_mac_code, expected
    ):
        """Test is_null with various combinations of conditions"""
        mock_ard.is_mac.return_value = is_mac_code
        handler = ShortNullHandler(mock_ard)

        result = handler.is_null(allele)
        assert result == expected
