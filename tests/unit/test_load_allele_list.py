import pytest
from unittest.mock import patch
from urllib.error import URLError
from pyard.loader.allele_list import load_allele_list
from pyard.simple_table import Table

# The pytest unit test covers:
# Success case - Tests parsing CSV data and returning correct dictionary
# Version 3130 handling - Verifies it gets renamed to 3131
# Latest version - Tests the "Latest" URL path
# Error handling - Tests URLError causes SystemExit
# Key test features:
# Uses unittest.mock.patch to mock urlopen
# Tests dictionary structure and content
# Verifies URL construction logic
# Tests error handling behavior
#
#
# fix patches urlopen at the module level where it's imported (pyard.load.load_new.urlopen) instead of at the global urllib.request.urlopen level. This ensures the mock intercepts the function call where it's actually used in the code.

mock_data = """# file: Allelelist.3290.txt
# date: 2017-07-10
# version: IPD-IMGT/HLA 3.29.0
# origin: https://github.com/ANHIG/IMGTHLA/Allelelist.3290.txt
# repository: https://raw.githubusercontent.com/ANHIG/IMGTHLA/Latest/allelelist/Allelelist.3290.txt
# author: WHO, Steven G. E. Marsh (steven.marsh@ucl.ac.uk)
AlleleID,Allele
HLA00001,A*01:01:01:01
HLA02169,A*01:01:01:02N
HLA14798,A*01:01:01:03"""


def test_load_allele_list_success():
    with patch("pyard.loader.allele_list.urlopen") as mock_urlopen:
        mock_urlopen.return_value = mock_data.encode().split(b"\n")

        result = load_allele_list("3290")

        assert isinstance(result, Table)
        allele_ids = result["AlleleID"]
        alleles = result["Allele"]
        assert allele_ids[0] == "HLA00001"
        assert alleles[0] == "A*01:01:01:01"
        assert allele_ids[1] == "HLA02169"
        assert alleles[1] == "A*01:01:01:02N"


def test_load_allele_list_version_3130():
    with patch("pyard.loader.allele_list.urlopen") as mock_urlopen:
        mock_urlopen.return_value = mock_data.encode().split(b"\n")

        load_allele_list("3130")

        expected_url = "https://raw.githubusercontent.com/ANHIG/IMGTHLA/Latest/allelelist/Allelelist.3131.txt"
        mock_urlopen.assert_called_once_with(expected_url)


def test_load_allele_list_latest():
    with patch("pyard.loader.allele_list.urlopen") as mock_urlopen:
        mock_urlopen.return_value = mock_data.encode().split(b"\n")

        load_allele_list("Latest")

        expected_url = (
            "https://raw.githubusercontent.com/ANHIG/IMGTHLA/Latest/Allelelist.txt"
        )
        mock_urlopen.assert_called_once_with(expected_url)


def test_load_allele_list_url_error():
    with patch(
        "pyard.loader.allele_list.urlopen", side_effect=URLError("Network error")
    ):
        with pytest.raises(SystemExit):
            load_allele_list("3290")
