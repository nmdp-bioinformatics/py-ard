import sys
from typing import Tuple, List
from urllib.error import URLError
from urllib.request import urlopen

from ..simple_table import Table
from ..loader import IMGT_HLA_URL


def load_serology_mappings(imgt_version):
    """
    Read `rel_dna_ser.txt` file that contains alleles and their serological equivalents.
    The fields of the Alleles->Serological mapping file are:
    |--------|----------------------------------------------------------------------|
    | Field  | Description                                                          |
    |--------|----------------------------------------------------------------------|
    | Locus  | HLA Locus                                                            |
    | Allele | HLA Allele Name                                                      |
    | USA    | Unambiguous Serological Antigen associated with allele               |
    | PSA    | Possible Serological Antigen associated with allele                  |
    | ASA    | Assumed Serological Antigen associated with allele                   |
    | EAE    | Expert Assigned Exceptions in search determinants of some registries |
    | HATS   | Assigned specificity as calculated by HATS                           |
    |--------|----------------------------------------------------------------------|
    EAE is ignored when generating the serology map.
    HATS is ignored when generating the serology map.

    :param imgt_version: IMGT database version
    :return: Table object with serology mapping data
    """

    rel_dna_ser_url = f"{IMGT_HLA_URL}{imgt_version}/wmda/rel_dna_ser.txt"

    try:
        response = urlopen(rel_dna_ser_url)
        lines = [line.decode("utf-8").strip() for line in response]

        # Skip first 6 header lines
        data_lines = lines[6:]

        # Convert semicolon-separated data to list of tuples
        # Original format: "A;A*01:01:01:01;A1;A1;;"
        # Version >= IPD-IMGT/HLA 3.64.0: "A*;01:01:01:01;1;;;;1"
        data_tuples = []
        columns = []
        for line in data_lines:
            if not line:
                continue
            fields = line.split(";")
            # as of 3.64.0 rel_dna_ser.txt has 7 fields
            if len(fields) == 7:
                # Extract 7 fields as tuple, replace empty strings with None
                rel_dna_fields = tuple(field if field else None for field in fields)
                data_tuples.append(rel_dna_fields)
                if not columns:
                    columns = ["Locus", "Allele", "USA", "PSA", "ASA", "EAE", "HATS"]
            elif len(fields) == 6:
                # Extract 6 fields as tuple, replace empty strings with None
                rel_dna_fields = tuple(field if field else None for field in fields)
                data_tuples.append(rel_dna_fields)
                if not columns:
                    columns = ["Locus", "Allele", "USA", "PSA", "ASA", "EAE"]
        return Table(data_tuples, columns)
    except URLError as e:
        print(f"Error downloading {rel_dna_ser_url}", e, file=sys.stderr)
        sys.exit(1)


def load_serology_broad_split_mapping(imgt_version: str) -> Tuple[Table, Table]:
    """
    Load serology broad/split mapping from rel_ser_ser.txt file.

    :param imgt_version: IMGT database version
    :return: Tuple of (splits_table, associated_table) Table objects
             - splits_table: Table with 'broad' and 'splits' columns
             - associated_table: Table with 'split' and 'broad' columns
    """

    ser_ser_url = f"{IMGT_HLA_URL}{imgt_version}/wmda/rel_ser_ser.txt"
    try:
        response = urlopen(ser_ser_url)
        lines = [line.decode("utf-8").strip() for line in response]

        # Skip first 6 header lines
        data_lines = lines[6:]

        # Prepare data as lists of tuples
        splits_tuples = []
        associated_tuples = []

        for line in data_lines:
            if line:  # Skip empty lines
                fields = line.split(";")
                if len(fields) >= 4:
                    locus, a, splits, associated = (
                        fields[0],
                        fields[1],
                        fields[2],
                        fields[3],
                    )

                    # Process splits: broad antigen -> list of splits
                    if splits:
                        sero = locus + a  # e.g. "A" + "10" = "A10"
                        splits_list = add_locus_name(
                            locus, splits
                        )  # Add locus prefix to each split
                        splits_str = "/".join(splits_list)
                        splits_tuples.append((sero, splits_str))

                    # Process associated: create reverse mapping from split -> broad
                    if associated:
                        sero = locus + a
                        associated_list = add_locus_name(locus, associated)
                        for assoc in associated_list:
                            associated_tuples.append((assoc, sero))

        splits_table = Table(splits_tuples, ["broad", "splits"])
        associated_table = Table(associated_tuples, ["split", "broad"])

        return splits_table, associated_table
    except URLError as e:
        print(f"Error downloading {ser_ser_url}", e, file=sys.stderr)
        sys.exit(1)


def add_locus_name(locus: str, splits: str) -> List:
    split_list = map(lambda sero: locus + sero, splits.split("/"))
    return list(split_list)
