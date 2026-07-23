# -*- coding: utf-8 -*-

import pytest
from unittest.mock import Mock, patch
from pyard.reducers.first_field_reducer import FirstFieldReducer


@pytest.fixture
def mock_ard():
    return Mock()


@pytest.mark.parametrize(
    "allele, expected",
    [
        ("A*01:01:01:01", "A*01"),
        ("B*07:02:01", "B*07"),
        ("DRB1*15:01:01", "DRB1*15"),
        ("A*01:01", "A*01"),
        ("A*01", "A*01"),
        ("C*07:02:01:03", "C*07"),
    ],
)
def test_reduce(mock_ard, allele, expected):
    assert FirstFieldReducer(mock_ard).reduce(allele) == expected


def test_reduce_calls_get_1field_allele(mock_ard):
    with patch(
        "pyard.reducers.first_field_reducer.get_1field_allele", return_value="A*01"
    ) as mock_fn:
        FirstFieldReducer(mock_ard).reduce("A*01:01:01:01")
        mock_fn.assert_called_once_with("A*01:01:01:01")
