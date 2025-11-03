# -*- coding: utf-8 -*-

import pytest
from unittest.mock import Mock, patch
import sqlite3

from pyard.handlers.mac_handler import MACHandler
from pyard.exceptions import InvalidMACError


class TestMACHandler:
    """Test cases for MACHandler class"""

    @pytest.fixture
    def mock_ard(self):
        """Create mock ARD instance"""
        ard = Mock()
        ard.db_connection = Mock()
        ard.smart_sort_comparator.return_value = 0
        ard._is_allele_in_db.return_value = True
        return ard

    @pytest.fixture
    def mac_handler(self, mock_ard):
        """Create MACHandler instance"""
        return MACHandler(mock_ard)

    def test_init(self, mock_ard):
        """Test MACHandler initialization"""
        handler = MACHandler(mock_ard)
        assert handler.ard == mock_ard

    @patch("pyard.handlers.mac_handler.db.mac_code_to_alleles")
    def test_is_mac_valid_alphabetic_code(self, mock_mac_to_alleles, mac_handler):
        """Test is_mac with valid alphabetic MAC code"""
        mock_mac_to_alleles.return_value = ["01:01", "01:02"]

        result = mac_handler.is_mac("A*01:AB")
        assert result is True
        mock_mac_to_alleles.assert_called_once_with(mac_handler.ard.db_connection, "AB")

    @patch("pyard.handlers.mac_handler.db.mac_code_to_alleles")
    def test_is_mac_valid_with_antigen_validation(
        self, mock_mac_to_alleles, mac_handler
    ):
        """Test is_mac with antigen group validation"""
        mock_mac_to_alleles.return_value = ["01:01", "01:02", "02:01"]

        result = mac_handler.is_mac("A*01:AB")
        assert result is True

    def test_is_mac_no_colon(self, mac_handler):
        """Test is_mac with string without colon"""
        result = mac_handler.is_mac("A01AB")
        assert result is False

    def test_is_mac_numeric_code(self, mac_handler):
        """Test is_mac with numeric code (not alphabetic)"""
        result = mac_handler.is_mac("A*01:01")
        assert result is False

    @patch("pyard.handlers.mac_handler.db.mac_code_to_alleles")
    def test_is_mac_database_error(self, mock_mac_to_alleles, mac_handler):
        """Test is_mac with database error"""
        mock_mac_to_alleles.side_effect = sqlite3.OperationalError("DB Error")

        result = mac_handler.is_mac("A*01:AB")
        assert result is False

    @patch("pyard.handlers.mac_handler.db.mac_code_to_alleles")
    def test_is_mac_no_alleles_found(self, mock_mac_to_alleles, mac_handler):
        """Test is_mac when no alleles found for code"""
        mock_mac_to_alleles.return_value = []

        result = mac_handler.is_mac("A*01:AB")
        assert result is False

    def test_expand_mac_valid_standard_format(self, mac_handler):
        """Test expand_mac with valid standard format MAC"""
        with patch.object(mac_handler, "is_mac", return_value=True), patch.object(
            mac_handler, "get_alleles", return_value=["A*01:01", "A*01:02"]
        ):
            result = mac_handler.expand_mac("A*01:AB")
            assert result == "A*01:01/A*01:02"

    def test_expand_mac_valid_hla_prefixed(self, mac_handler):
        """Test expand_mac with HLA-prefixed format"""
        with patch.object(mac_handler, "is_mac", return_value=True), patch.object(
            mac_handler, "get_alleles", return_value=["A*01:01", "A*01:02"]
        ):
            result = mac_handler.expand_mac("HLA-A*01:AB")
            assert result == "HLA-A*01:01/HLA-A*01:02"

    def test_expand_mac_invalid(self, mac_handler):
        """Test expand_mac with invalid MAC code"""
        with patch.object(mac_handler, "is_mac", return_value=False):
            with pytest.raises(InvalidMACError):
                mac_handler.expand_mac("INVALID")

    @patch("pyard.handlers.mac_handler.db.alleles_to_mac_code")
    def test_lookup_mac_single_antigen_group(self, mock_alleles_to_mac, mac_handler):
        """Test lookup_mac with single antigen group optimization"""
        mock_alleles_to_mac.return_value = "AB"

        result = mac_handler.lookup_mac("A*01:01/A*01:02")
        assert result == "A*01:AB"
        mock_alleles_to_mac.assert_called_once_with(
            mac_handler.ard.db_connection, "01/02"
        )

    @patch("pyard.handlers.mac_handler.db.alleles_to_mac_code")
    def test_lookup_mac_given_order(self, mock_alleles_to_mac, mac_handler):
        """Test lookup_mac trying given order"""
        mock_alleles_to_mac.side_effect = [
            None,
            "AB",
        ]  # First call fails, second succeeds

        result = mac_handler.lookup_mac("A*01:01/A*02:01")
        assert result == "A*01:AB"

    @patch("pyard.handlers.mac_handler.db.alleles_to_mac_code")
    def test_lookup_mac_sorted_order(self, mock_alleles_to_mac, mac_handler):
        """Test lookup_mac trying sorted order"""
        # Mock the smart_sort_comparator to return consistent sorting
        mac_handler.ard.smart_sort_comparator.return_value = -1  # First arg comes first
        # For different antigen groups, skip single antigen optimization
        mock_alleles_to_mac.side_effect = [None, "AB"]  # First fails, second succeeds

        result = mac_handler.lookup_mac("A*02:01/A*01:01")
        assert result == "A*01:AB"  # Uses sorted antigen groups, first one is 01

    @patch("pyard.handlers.mac_handler.db.alleles_to_mac_code")
    def test_lookup_mac_no_mac_found(self, mock_alleles_to_mac, mac_handler):
        """Test lookup_mac when no MAC code is found"""
        mock_alleles_to_mac.return_value = None

        with pytest.raises(InvalidMACError):
            mac_handler.lookup_mac("A*01:01/A*01:02")

    @patch("pyard.handlers.mac_handler.db.mac_code_to_alleles")
    def test_get_alleles_full_allele_expansion(self, mock_mac_to_alleles, mac_handler):
        """Test get_alleles with full allele expansion format"""
        mock_mac_to_alleles.return_value = ["01:01", "01:02"]

        result = mac_handler.get_alleles("AB", "A*01")
        expected = ["A*01:01", "A*01:02"]
        assert list(result) == expected

    @patch("pyard.handlers.mac_handler.db.mac_code_to_alleles")
    def test_get_alleles_field_suffix_expansion(self, mock_mac_to_alleles, mac_handler):
        """Test get_alleles with field suffix expansion format"""
        mock_mac_to_alleles.return_value = ["01", "02"]

        result = mac_handler.get_alleles("AB", "A*01")
        expected = ["A*01:01", "A*01:02"]
        assert list(result) == expected

    @patch("pyard.handlers.mac_handler.db.mac_code_to_alleles")
    def test_get_alleles_filtered_by_database(self, mock_mac_to_alleles, mac_handler):
        """Test get_alleles filters results by database presence"""
        mock_mac_to_alleles.return_value = ["01:01", "01:02"]
        mac_handler.ard._is_allele_in_db.side_effect = lambda x: x == "A*01:01"

        result = mac_handler.get_alleles("AB", "A*01")
        assert list(result) == ["A*01:01"]

    def test_is_mac_cache_behavior(self, mac_handler):
        """Test that is_mac uses caching"""
        with patch(
            "pyard.handlers.mac_handler.db.mac_code_to_alleles"
        ) as mock_mac_to_alleles:
            mock_mac_to_alleles.return_value = ["01:01"]

            # Call twice with same input
            mac_handler.is_mac("A*01:AB")
            mac_handler.is_mac("A*01:AB")

            # Should only call database once due to caching
            assert mock_mac_to_alleles.call_count == 1
