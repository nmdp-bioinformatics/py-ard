import pytest
from unittest.mock import patch
from urllib.error import URLError
from pyard.loader.serology import load_serology_mappings
from pyard.simple_table import Table


def test_load_serology_mappings_success():
    mock_data = """
# file: rel_dna_ser.txt
# date: 2025-07-14
# version: IPD-IMGT/HLA 3.61.0
# origin: http://hla.alleles.org/wmda/rel_dna_ser.txt
# repository: https://raw.githubusercontent.com/ANHIG/IMGTHLA/Latest/wmda/rel_dna_ser.txt
# author: WHO, Steven G. E. Marsh (steven.marsh@ucl.ac.uk)
A*;01:01:01:01;1;;;
A*;01:01:01:02N;0;;;
A*;01:01:01:03;1;;;
A*;01:01:01:04;1;;;
A*;02:1068Q;;;0/2;
B*;01:01:01:05;1;;;
    """.strip()
    with patch("pyard.loader.serology.urlopen") as mock_urlopen:
        mock_urlopen.return_value = mock_data.encode().split(b"\n")

        result = load_serology_mappings("3290")

        assert isinstance(result, Table)
        loci = result["Locus"]
        alleles = result["Allele"]
        usa = result["USA"]
        assert len(loci) == 6
        assert loci[0] == "A*"
        assert alleles[0] == "01:01:01:01"
        assert usa[0] == "1"
        assert loci[5] == "B*"
        assert alleles[4] == "02:1068Q"


def test_load_serology_mappings_with_HATS_success():
    mock_data = """
# file: rel_dna_ser.txt
# date: 2026-04-16
# version: IPD-IMGT/HLA 3.64.0
# origin: http://hla.alleles.org/wmda/rel_dna_ser.txt
# repository: https://raw.githubusercontent.com/ANHIG/IMGTHLA/Latest/wmda/rel_dna_ser.txt
# author: IPD Team (ipdsubs@anthonynolan.org)
A*;01:01:01:01;1;;;;1
A*;01:01:01:02N;0;;;;
A*;01:01:01:03;1;;;;1
A*;01:01:01:04;1;;;;1
A*;02:04:02;2;;;;0201
A*;02:03:18;0203;;;;0203
B*;07:03;0703;;;;0703
    """.strip()
    with patch("pyard.loader.serology.urlopen") as mock_urlopen:
        mock_urlopen.return_value = mock_data.encode().split(b"\n")

        result = load_serology_mappings("3640")

        assert isinstance(result, Table)
        loci = result["Locus"]
        alleles = result["Allele"]
        usa = result["USA"]
        hats = result["HATS"]
        assert len(loci) == 7
        assert loci[0] == "A*"
        assert alleles[0] == "01:01:01:01"
        assert usa[0] == "1"
        assert loci[4] == "A*"
        assert alleles[4] == "02:04:02"
        assert hats[4] == "0201"
        assert loci[5] == "A*"
        assert alleles[5] == "02:03:18"
        assert hats[5] == "0203"
        assert loci[6] == "B*"
        assert alleles[6] == "07:03"
        assert hats[6] == "0703"


def test_load_serology_mappings_empty_lines():
    mock_data = """
# header line 1
# header line 2
# header line 3
# header line 4
# header line 5
# header line 6
A*;01:01:01:01;A1;A1;;

B*;07:02:01;B7;B7;;
    """.strip()

    with patch("pyard.loader.serology.urlopen") as mock_urlopen:
        mock_urlopen.return_value = mock_data.encode().split(b"\n")

        result = load_serology_mappings("3290")

        assert len(result["Locus"]) == 2


def test_load_serology_mappings_url_error():
    with patch("pyard.loader.serology.urlopen", side_effect=URLError("Network error")):
        with pytest.raises(SystemExit):
            load_serology_mappings("3290")
