# -*- coding: utf-8 -*-

import pytest
from unittest.mock import Mock, patch

from pyard.handlers.serology_handler import SerologyHandler
from pyard.exceptions import InvalidAlleleError


class TestSerologyHandler:
    """Test cases for SerologyHandler class"""

    @pytest.fixture
    def mock_ard(self):
        """Create mock ARD instance"""
        ard = Mock()
        ard.db_connection = Mock()
        ard.valid_serology_set = {"A1", "A2", "B27", "DR4"}
        ard.serology_mapping = Mock()
        ard._is_allele_in_db.return_value = True
        return ard

    @pytest.fixture
    def serology_handler(self, mock_ard):
        """Create SerologyHandler instance"""
        return SerologyHandler(mock_ard)

    def test_init(self, mock_ard):
        """Test SerologyHandler initialization"""
        handler = SerologyHandler(mock_ard)
        assert handler.ard == mock_ard

    def test_is_serology_valid_serology(self, serology_handler):
        """Test is_serology with valid serology"""
        result = serology_handler.is_serology("A1")
        assert result is True

    def test_is_serology_invalid_serology(self, serology_handler):
        """Test is_serology with invalid serology"""
        result = serology_handler.is_serology("INVALID")
        assert result is False

    def test_is_serology_with_asterisk(self, serology_handler):
        """Test is_serology with molecular format (contains *)"""
        result = serology_handler.is_serology("A*01:01")
        assert result is False

    def test_is_serology_with_colon(self, serology_handler):
        """Test is_serology with molecular format (contains :)"""
        result = serology_handler.is_serology("A*01:01")
        assert result is False

    @patch("pyard.handlers.serology_handler.db.serology_to_alleles")
    def test_get_alleles_from_serology(
        self, mock_serology_to_alleles, serology_handler
    ):
        """Test get_alleles_from_serology"""
        mock_serology_to_alleles.return_value = ["A*01:01", "A*01:02", "A*01:03"]

        result = serology_handler.get_alleles_from_serology("A1")
        expected = {"A*01:01", "A*01:02", "A*01:03"}
        assert result == expected
        mock_serology_to_alleles.assert_called_once_with(
            serology_handler.ard.db_connection, "A1"
        )

    @patch("pyard.handlers.serology_handler.db.serology_to_alleles")
    def test_get_alleles_from_serology_filtered(
        self, mock_serology_to_alleles, serology_handler
    ):
        """Test get_alleles_from_serology with database filtering"""
        mock_serology_to_alleles.return_value = ["A*01:01", "A*01:02", "A*01:03"]
        serology_handler.ard._is_allele_in_db.side_effect = lambda x: x != "A*01:02"

        result = serology_handler.get_alleles_from_serology("A1")
        expected = {"A*01:01", "A*01:03"}
        assert result == expected

    def test_find_broad_splits(self, serology_handler):
        """Test find_broad_splits delegates to serology_mapping"""
        serology_handler.ard.serology_mapping.find_splits.return_value = (
            "A9",
            ["A23", "A24"],
        )

        result = serology_handler.find_broad_splits("A23")
        assert result == ("A9", ["A23", "A24"])
        serology_handler.ard.serology_mapping.find_splits.assert_called_once_with("A23")

    def test_find_associated_antigen(self, serology_handler):
        """Test find_associated_antigen delegates to serology_mapping"""
        serology_handler.ard.serology_mapping.find_associated_antigen.return_value = (
            "A1"
        )

        result = serology_handler.find_associated_antigen("A1")
        assert result == "A1"
        serology_handler.ard.serology_mapping.find_associated_antigen.assert_called_once_with(
            "A1"
        )

    @patch("pyard.handlers.serology_handler.db.find_xx_for_serology")
    def test_find_xx_from_serology_valid(self, mock_find_xx, serology_handler):
        """Test find_xx_from_serology with valid serology"""
        mock_find_xx.return_value = "A*01:XX"

        result = serology_handler.find_xx_from_serology("A1")
        assert result == "A*01:XX"
        mock_find_xx.assert_called_once_with(serology_handler.ard.db_connection, "A1")

    def test_find_xx_from_serology_invalid(self, serology_handler):
        """Test find_xx_from_serology with invalid serology"""
        with patch.object(serology_handler, "is_serology", return_value=False):
            with pytest.raises(InvalidAlleleError):
                serology_handler.find_xx_from_serology("INVALID")

    @pytest.mark.parametrize(
        "serology,expected",
        [
            ("A1", True),
            ("A2", True),
            ("B27", True),
            ("DR4", True),
            ("INVALID", False),
            ("A*01:01", False),
            ("A1:01", False),
        ],
    )
    def test_is_serology_various_inputs(self, serology_handler, serology, expected):
        """Test is_serology with various input formats"""
        result = serology_handler.is_serology(serology)
        assert result == expected
