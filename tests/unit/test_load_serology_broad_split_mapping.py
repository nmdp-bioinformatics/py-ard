import pytest
from unittest.mock import patch
from urllib.error import URLError
from pyard.loader.serology import load_serology_broad_split_mapping
from pyard.simple_table import Table


def test_load_serology_broad_split_mapping_success():
    mock_data = """
# file: rel_ser_ser.txt
# date: 2025-07-14
# version: IPD-IMGT/HLA 3.61.0
# origin: http://hla.alleles.org/wmda/rel_ser_ser.txt
# repository: https://raw.githubusercontent.com/ANHIG/IMGTHLA/Latest/wmda/rel_ser_ser.txt
# author: WHO, Steven G. E. Marsh (steven.marsh@ucl.ac.uk)
A;10;25/26/34/66;25/26/34/66
B;14;64/65;64/65
""".strip()

    with patch("pyard.loader.serology.urlopen") as mock_urlopen:
        mock_urlopen.return_value = mock_data.encode().split(b"\n")

        splits_table, associated_table = load_serology_broad_split_mapping("3290")

        assert isinstance(splits_table, Table)
        assert isinstance(associated_table, Table)

        # Test splits table
        broad_col = splits_table["broad"]
        splits_col = splits_table["splits"]
        assert len(broad_col) == 2
        assert broad_col[0] == "A10"
        assert splits_col[0] == "A25/A26/A34/A66"
        assert len(splits_col[0].split("/")) == 4  # 4 A splits
        assert broad_col[1] == "B14"
        assert splits_col[1] == "B64/B65"
        assert len(splits_col[1].split("/")) == 2  # 2 B splits

        # Test associated table
        split_col = associated_table["split"]
        broad_assoc_col = associated_table["broad"]
        assert len(split_col) == 6  # 4 A associated + 2 B associated
        assert "A25" in split_col
        assert "A10" in broad_assoc_col


def test_load_serology_broad_split_mapping_empty_splits():
    mock_data = """
# header 1
# header 2
# header 3
# header 4
# header 5
# header 6
A;10;;;
B;14;64/65;64/65
""".strip()

    with patch("pyard.loader.serology.urlopen") as mock_urlopen:
        mock_urlopen.return_value = mock_data.encode().split(b"\n")

        splits_table, associated_table = load_serology_broad_split_mapping("3290")

        # Only B14 should have splits
        assert len(splits_table["broad"]) == 1
        assert splits_table["broad"][0] == "B14"


def test_load_serology_broad_split_mapping_url_error():
    with patch("pyard.loader.serology.urlopen", side_effect=URLError("Network error")):
        with pytest.raises(SystemExit):
            load_serology_broad_split_mapping("3290")
