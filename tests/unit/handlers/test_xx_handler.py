# -*- coding: utf-8 -*-

import pytest
from unittest.mock import Mock

from pyard.handlers.xx_handler import XXHandler


class TestXXHandler:
    """Test cases for XXHandler class"""

    @pytest.fixture
    def mock_ard(self):
        """Create mock ARD instance"""
        ard = Mock()
        ard.code_mappings = Mock()
        ard.code_mappings.xx_codes = {"A*01", "A*02", "B*27", "B*15"}
        return ard

    @pytest.fixture
    def xx_handler(self, mock_ard):
        """Create XXHandler instance"""
        return XXHandler(mock_ard)

    def test_init(self, mock_ard):
        """Test XXHandler initialization"""
        handler = XXHandler(mock_ard)
        assert handler.ard == mock_ard

    def test_is_xx_valid_xx_code(self, xx_handler):
        """Test is_xx with valid XX code"""
        result = xx_handler.is_xx("A*01:XX")
        assert result is True

    def test_is_xx_invalid_code_suffix(self, xx_handler):
        """Test is_xx with invalid code suffix (not XX)"""
        result = xx_handler.is_xx("A*01:AB")
        assert result is False

    def test_is_xx_invalid_locus_antigen(self, xx_handler):
        """Test is_xx with locus*antigen not in mappings"""
        result = xx_handler.is_xx("C*03:XX")
        assert result is False

    def test_is_xx_no_colon(self, xx_handler):
        """Test is_xx with string without colon"""
        result = xx_handler.is_xx("A01XX")
        assert result is False

    def test_is_xx_with_provided_components(self, xx_handler):
        """Test is_xx with pre-parsed components"""
        result = xx_handler.is_xx("", loc_antigen="A*01", code="XX")
        assert result is True

    def test_is_xx_with_provided_components_invalid_code(self, xx_handler):
        """Test is_xx with pre-parsed components but invalid code"""
        result = xx_handler.is_xx("", loc_antigen="A*01", code="AB")
        assert result is False

    def test_is_xx_with_provided_components_invalid_locus(self, xx_handler):
        """Test is_xx with pre-parsed components but invalid locus*antigen"""
        result = xx_handler.is_xx("", loc_antigen="C*03", code="XX")
        assert result is False

    def test_is_xx_malformed_string_too_many_colons(self, xx_handler):
        """Test is_xx with malformed string (too many colons)"""
        result = xx_handler.is_xx("A*01:02:XX")
        assert result is False

    def test_is_xx_empty_string(self, xx_handler):
        """Test is_xx with empty string"""
        result = xx_handler.is_xx("")
        assert result is False

    @pytest.mark.parametrize(
        "glstring,expected",
        [
            ("A*01:XX", True),
            ("A*02:XX", True),
            ("B*27:XX", True),
            ("B*15:XX", True),
            ("A*01:AB", False),
            ("A*01:01", False),
            ("C*03:XX", False),
            ("A01XX", False),
            ("A*01XX", False),
            ("", False),
        ],
    )
    def test_is_xx_various_inputs(self, xx_handler, glstring, expected):
        """Test is_xx with various input formats"""
        result = xx_handler.is_xx(glstring)
        assert result == expected

    def test_is_xx_case_sensitivity(self, xx_handler):
        """Test is_xx is case sensitive for XX code"""
        result_upper = xx_handler.is_xx("A*01:XX")
        result_lower = xx_handler.is_xx("A*01:xx")

        assert result_upper is True
        assert result_lower is False

    def test_is_xx_with_partial_components_none_loc_antigen(self, xx_handler):
        """Test is_xx with None loc_antigen but valid code"""
        result = xx_handler.is_xx("A*01:XX", loc_antigen=None, code="XX")
        assert result is True

    def test_is_xx_with_partial_components_none_code(self, xx_handler):
        """Test is_xx with valid loc_antigen but None code"""
        result = xx_handler.is_xx("A*01:XX", loc_antigen="A*01", code=None)
        assert result is True
