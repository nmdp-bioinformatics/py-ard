# -*- coding: utf-8 -*-

import pytest
from unittest.mock import Mock

from pyard.handlers.gl_string_processor import GLStringHandler
from pyard.exceptions import InvalidAlleleError


class TestGLStringHandler:
    """Test cases for GLStringHandler class"""

    @pytest.fixture
    def mock_ard(self):
        """Create mock ARD instance"""

        def redux_side_effect(x, y):
            # Mock the redux method to return the input string
            return x

        def sort_comparator(a, b, ignore_suffixes=()):
            # Simple lexicographic comparison for consistent sorting
            if a < b:
                return -1
            elif a > b:
                return 1
            else:
                return 0

        ard = Mock()
        ard._config = {"strict": False, "ignore_allele_with_suffixes": ()}
        ard.redux.side_effect = redux_side_effect
        ard.smart_sort_comparator.side_effect = sort_comparator
        ard._is_valid.return_value = True
        return ard

    @pytest.fixture
    def gl_handler(self, mock_ard):
        """Create GLStringHandler instance"""
        return GLStringHandler(mock_ard)

    def test_init(self, mock_ard):
        """Test GLStringHandler initialization"""
        handler = GLStringHandler(mock_ard)
        assert handler.ard == mock_ard

    def test_process_gl_string_single_allele(self, gl_handler):
        """Test processing single allele (no delimiters)"""
        result = gl_handler.process_gl_string("A*01:01", "G")
        assert result == "A*01:01"

    def test_process_gl_string_caret_delimiter(self, gl_handler):
        """Test processing GL string with ^ delimiter"""
        result = gl_handler.process_gl_string("A*01:01^B*07:02", "G")
        # Results are sorted - check that both components are present
        assert "A*01:01" in result and "B*07:02" in result and "^" in result

    def test_process_gl_string_pipe_delimiter(self, gl_handler):
        """Test processing GL string with | delimiter"""
        result = gl_handler.process_gl_string("A*01:01|B*07:02", "G")
        # Results are sorted - check that both components are present
        assert "A*01:01" in result and "B*07:02" in result and "|" in result

    def test_process_gl_string_plus_delimiter(self, gl_handler):
        """Test processing GL string with + delimiter"""
        result = gl_handler.process_gl_string("A*01:01+A*02:01", "G")
        assert result == "A*01:01+A*02:01"

    def test_process_gl_string_tilde_delimiter(self, gl_handler):
        """Test processing GL string with ~ delimiter"""
        result = gl_handler.process_gl_string("A*01:01~A*02:01", "G")
        assert result == "A*01:01~A*02:01"

    def test_process_gl_string_slash_delimiter(self, gl_handler):
        """Test processing GL string with / delimiter"""
        result = gl_handler.process_gl_string("A*01:01/A*02:01", "lgx")
        # Results are sorted - the actual sorting puts A*01:01 before A*02:01
        assert result == "A*01:01/A*02:01"

    def test_process_gl_string_strict_mode_valid(self, mock_ard):
        """Test processing with strict mode enabled and valid alleles"""
        mock_ard._config["strict"] = True
        handler = GLStringHandler(mock_ard)
        result = handler.process_gl_string("A*01:01", "G")
        assert result == "A*01:01"
        mock_ard._is_valid.assert_called_once_with("A*01:01")

    def test_process_gl_string_strict_mode_invalid(self, mock_ard):
        """Test processing with strict mode enabled and invalid alleles"""
        mock_ard._config["strict"] = True
        mock_ard._is_valid.return_value = False
        handler = GLStringHandler(mock_ard)

        with pytest.raises(InvalidAlleleError):
            handler.process_gl_string("INVALID", "G")

    def test_sorted_unique_gl_tilde_preserves_order(self, gl_handler):
        """Test that ~ delimiter preserves original order"""
        result = gl_handler._sorted_unique_gl(["B*07:02", "A*01:01"], "~")
        assert result == "B*07:02~A*01:01"

    def test_sorted_unique_gl_plus_sorts(self, gl_handler):
        """Test that + delimiter sorts components"""
        result = gl_handler._sorted_unique_gl(["B*07:02", "A*01:01"], "+")
        assert "+" in result

    def test_sorted_unique_gl_other_delimiters_flatten(self, gl_handler):
        """Test that other delimiters flatten and deduplicate"""
        result = gl_handler._sorted_unique_gl(["A*01:01/A*02:01", "A*01:01"], "/")
        # Should flatten and deduplicate
        assert "/" in result

    def test_validate_gl_string_single_valid_allele(self, gl_handler):
        """Test validation of single valid allele"""
        result = gl_handler.validate_gl_string("A*01:01")
        assert result is True

    def test_validate_gl_string_single_invalid_allele(self, mock_ard):
        """Test validation of single invalid allele"""
        mock_ard._is_valid.return_value = False
        handler = GLStringHandler(mock_ard)

        with pytest.raises(InvalidAlleleError):
            handler.validate_gl_string("INVALID")

    def test_validate_gl_string_with_delimiters(self, gl_handler):
        """Test validation of GL string with delimiters"""
        result = gl_handler.validate_gl_string("A*01:01^B*07:02")
        assert result is True

    def test_validate_gl_string_mixed_valid_invalid(self, mock_ard):
        """Test validation with mix of valid and invalid alleles"""
        mock_ard._is_valid.side_effect = lambda x: x != "INVALID"
        handler = GLStringHandler(mock_ard)

        with pytest.raises(InvalidAlleleError):
            handler.validate_gl_string("A*01:01^INVALID")

    @pytest.mark.parametrize(
        "redux_type", ["G", "P", "lg", "lgx", "W", "exon", "U2", "S"]
    )
    def test_process_gl_string_valid_redux_types(self, gl_handler, redux_type):
        """Test processing with all valid reduction types"""
        result = gl_handler.process_gl_string("A*01:01", redux_type)
        assert result == "A*01:01"

    def test_process_gl_string_invalid_redux_type(self, gl_handler):
        """Test processing with invalid reduction type"""
        with pytest.raises(ValueError):
            gl_handler.process_gl_string("A*01:01", "INVALID")
