# -*- coding: utf-8 -*-

import pytest
from unittest.mock import Mock, patch

from pyard import ARDConfig
from pyard.handlers.v2_handler import V2Handler


class TestV2Handler:
    """Test cases for V2Handler class"""

    @pytest.fixture
    def mock_ard(self):
        """Create mock ARD instance"""
        ard = Mock()
        ard.config = ARDConfig.from_dict({"reduce_v2": True})
        ard.db_connection = Mock()
        ard.is_mac.return_value = False
        ard._is_allele_in_db.return_value = True
        return ard

    @pytest.fixture
    def v2_handler(self, mock_ard):
        """Create V2Handler instance"""
        return V2Handler(mock_ard)

    def test_init(self, mock_ard):
        """Test V2Handler initialization"""
        handler = V2Handler(mock_ard)
        assert handler.ard == mock_ard

    @patch("pyard.handlers.v2_handler.db.v2_to_v3_allele")
    def test_is_v2_valid_v2_format(self, mock_v2_to_v3, v2_handler):
        """Test is_v2 with valid V2 format allele"""
        mock_v2_to_v3.return_value = "A*01:01"

        result = v2_handler.is_v2("A*0101")
        assert result is True

    def test_is_v2_config_disabled(self, mock_ard):
        """Test is_v2 with V2 reduction disabled"""
        mock_ard.config = ARDConfig.from_dict({"reduce_v2": False})
        handler = V2Handler(mock_ard)

        result = handler.is_v2("A*0101")
        assert result is False

    def test_is_v2_no_asterisk(self, v2_handler):
        """Test is_v2 with allele without asterisk"""
        result = v2_handler.is_v2("A0101")
        assert result is False

    def test_is_v2_has_colon(self, v2_handler):
        """Test is_v2 with allele containing colon (V3 format)"""
        result = v2_handler.is_v2("A*01:01")
        assert result is False

    @pytest.mark.parametrize("locus", ["MICA", "MICB", "HFE"])
    def test_is_v2_excluded_loci(self, v2_handler, locus):
        """Test is_v2 with excluded loci"""
        result = v2_handler.is_v2(f"{locus}*001")
        assert result is False

    @patch("pyard.handlers.v2_handler.db.v2_to_v3_allele")
    def test_is_v2_no_conversion_available(self, mock_v2_to_v3, v2_handler):
        """Test is_v2 when no V3 conversion is available"""
        mock_v2_to_v3.return_value = "A*0101"  # Same as input, no conversion

        result = v2_handler.is_v2("A*0101")
        assert result is False

    @patch("pyard.handlers.v2_handler.db.v2_to_v3_allele")
    def test_is_v2_mac_code_result(self, mock_v2_to_v3, v2_handler):
        """Test is_v2 when conversion results in MAC code"""
        mock_v2_to_v3.return_value = "A*01:AB"
        v2_handler.ard.is_mac.return_value = True

        result = v2_handler.is_v2("A*0101")
        assert result is True

    @patch("pyard.handlers.v2_handler.db.v2_to_v3_allele")
    def test_map_v2_to_v3_database_mapping(self, mock_v2_to_v3, v2_handler):
        """Test map_v2_to_v3 with database mapping available"""
        mock_v2_to_v3.return_value = "A*01:01"

        result = v2_handler.map_v2_to_v3("A*0101")
        assert result == "A*01:01"
        mock_v2_to_v3.assert_called_once_with(v2_handler.ard.db_connection, "A*0101")

    @patch("pyard.handlers.v2_handler.db.v2_to_v3_allele")
    def test_map_v2_to_v3_heuristic_fallback(self, mock_v2_to_v3, v2_handler):
        """Test map_v2_to_v3 falls back to heuristic when no database mapping"""
        mock_v2_to_v3.return_value = None

        with patch.object(
            v2_handler, "_predict_v3", return_value="A*01:01"
        ) as mock_predict:
            result = v2_handler.map_v2_to_v3("A*0101")
            assert result == "A*01:01"
            mock_predict.assert_called_once_with("A*0101")

    def test_predict_v3_single_digit(self, v2_handler):
        """Test _predict_v3 with single digit allele (should return unchanged)"""
        result = v2_handler._predict_v3("A*1")
        assert result == "A*1"

    def test_predict_v3_two_digits(self, v2_handler):
        """Test _predict_v3 with two digits"""
        result = v2_handler._predict_v3("A*01")
        assert result == "A*01"

    def test_predict_v3_two_digits_with_suffix(self, v2_handler):
        """Test _predict_v3 with two digits and non-digit suffix"""
        result = v2_handler._predict_v3("A*01N")
        assert result == "A*01:N"

    def test_predict_v3_four_digits_even(self, v2_handler):
        """Test _predict_v3 with four digits (even number)"""
        result = v2_handler._predict_v3("A*0101")
        assert result == "A*01:01"

    def test_predict_v3_five_digits_odd(self, v2_handler):
        """Test _predict_v3 with five digits (odd number)"""
        result = v2_handler._predict_v3("A*01011")
        assert result == "A*01:011"

    def test_predict_v3_dp_locus_five_digits(self, v2_handler):
        """Test _predict_v3 with DP locus and five digits (special case)"""
        result = v2_handler._predict_v3("DPA1*01011")
        assert result == "DPA1*010:11"

    def test_predict_v3_six_digits_even(self, v2_handler):
        """Test _predict_v3 with six digits (even number)"""
        result = v2_handler._predict_v3("A*010101")
        assert result == "A*01:01:01"

    def test_predict_v3_with_suffix(self, v2_handler):
        """Test _predict_v3 with digits and suffix"""
        result = v2_handler._predict_v3("A*0101N")
        assert result == "A*01:01N"

    def test_predict_v3_no_digits(self, v2_handler):
        """Test _predict_v3 with no digit pattern (should return unchanged)"""
        result = v2_handler._predict_v3("A*ABC")
        assert result == "A*ABC"

    def test_combine_with_colon_four_digits(self, v2_handler):
        """Test _combine_with_colon with four digits"""
        result = v2_handler._combine_with_colon("0101")
        assert result == "01:01"

    def test_combine_with_colon_six_digits(self, v2_handler):
        """Test _combine_with_colon with six digits"""
        result = v2_handler._combine_with_colon("010101")
        assert result == "01:01:01"

    def test_combine_with_colon_eight_digits(self, v2_handler):
        """Test _combine_with_colon with eight digits"""
        result = v2_handler._combine_with_colon("01010101")
        assert result == "01:01:01:01"

    @pytest.mark.parametrize(
        "v2_allele,expected_v3",
        [
            ("A*01", "A*01"),
            ("A*0101", "A*01:01"),
            ("A*010101", "A*01:01:01"),
            ("A*01010101", "A*01:01:01:01"),
            ("A*0101N", "A*01:01N"),
            ("A*01011", "A*01:011"),
            ("DPA1*01011", "DPA1*010:11"),
            ("A*1", "A*1"),
        ],
    )
    def test_predict_v3_various_patterns(self, v2_handler, v2_allele, expected_v3):
        """Test _predict_v3 with various V2 patterns"""
        result = v2_handler._predict_v3(v2_allele)
        assert result == expected_v3
