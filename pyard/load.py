import sys
from typing import Dict, List
from urllib.error import HTTPError

import pandas as pd

from pyard.misc import get_G_name, get_2field_allele, get_3field_allele, get_P_name

# GitHub URL where IMGT HLA files are downloaded.
IMGT_HLA_URL = "https://raw.githubusercontent.com/ANHIG/IMGTHLA/"


def add_locus_name(locus: str, splits: str) -> List:
    split_list = map(lambda sero: locus + sero, splits.split("/"))
    return list(split_list)


#
# Derived from rel_ser_ser.txt
# https://raw.githubusercontent.com/ANHIG/IMGTHLA/Latest/wmda/rel_ser_ser.txt
#
def load_serology_broad_split_mapping(imgt_version: str) -> Dict:
    ser_ser_url = f"{IMGT_HLA_URL}{imgt_version}/wmda/rel_ser_ser.txt"
    df_p = pd.read_csv(
        ser_ser_url,
        skiprows=6,
        names=["Locus", "A", "Splits", "Associated"],
        usecols=[0, 1, 2],
        dtype="string",
        sep=";",
    ).dropna()

    df_p["Sero"] = df_p["Locus"] + df_p["A"]
    df_p["Splits"] = df_p[["Locus", "Splits"]].apply(
        lambda x: add_locus_name(x["Locus"], x["Splits"]), axis=1
    )

    sero_mapping = df_p[["Sero", "Splits"]].set_index("Sero")["Splits"].to_dict()
    return sero_mapping


def load_g_group(imgt_version):
    # load the hla_nom_g.txt
    ars_g_url = f"{IMGT_HLA_URL}{imgt_version}/wmda/hla_nom_g.txt"
    df = pd.read_csv(ars_g_url, skiprows=6, names=["Locus", "A", "G"], sep=";").dropna()
    # the G-group is named for its first allele
    df["G"] = df["A"].apply(get_G_name)
    # convert slash delimited string to a list
    df["A"] = df["A"].apply(lambda a: a.split("/"))
    # convert the list into separate rows for each element
    df = df.explode("A")
    #  A*   + 02:01   = A*02:01
    df["A"] = df["Locus"] + df["A"]
    df["G"] = df["Locus"] + df["G"]
    # Create 2,3 field versions of the alleles
    df["2d"] = df["A"].apply(get_2field_allele)
    df["3d"] = df["A"].apply(get_3field_allele)
    # lgx is 2 field version of the G group allele
    df["lgx"] = df["G"].apply(get_2field_allele)

    return df


def load_p_group(imgt_version):
    # load the hla_nom_p.txt
    ars_p_url = f"{IMGT_HLA_URL}{imgt_version}/wmda/hla_nom_p.txt"
    # example: C*;06:06:01:01/06:06:01:02/06:271;06:06P
    df_p = pd.read_csv(
        ars_p_url, skiprows=6, names=["Locus", "A", "P"], sep=";"
    ).dropna()
    # the P-group is named for its first allele
    df_p["P"] = df_p["A"].apply(get_P_name)
    # convert slash delimited string to a list
    df_p["A"] = df_p["A"].apply(lambda a: a.split("/"))
    df_p = df_p.explode("A")
    # C* 06:06:01:01/06:06:01:02/06:271 06:06P
    df_p["A"] = df_p["Locus"] + df_p["A"]
    df_p["P"] = df_p["Locus"] + df_p["P"]
    # C* 06:06:01:01 06:06P
    # C* 06:06:01:02 06:06P
    # C* 06:271 06:06P
    df_p["2d"] = df_p["A"].apply(get_2field_allele)
    # lgx has the P-group name without the P for comparison
    df_p["lgx"] = df_p["P"].apply(get_2field_allele)
    return df_p


def load_allele_list(imgt_version):
    """
    The format of the AlleleList file has a 6-line header with a header
    on the 7th line
    ```
    # file: Allelelist.3290.txt
    # date: 2017-07-10
    # version: IPD-IMGT/HLA 3.29.0
    # origin: https://github.com/ANHIG/IMGTHLA/Allelelist.3290.txt
    # repository: https://raw.githubusercontent.com/ANHIG/IMGTHLA/Latest/allelelist/Allelelist.3290.txt
    # author: WHO, Steven G. E. Marsh (steven.marsh@ucl.ac.uk)
    AlleleID,Allele
    HLA00001,A*01:01:01:01
    HLA02169,A*01:01:01:02N
    HLA14798,A*01:01:01:03
    HLA15760,A*01:01:01:04
    HLA16415,A*01:01:01:05
    HLA16417,A*01:01:01:06
    HLA16436,A*01:01:01:07
    ```

    :param db_connection: Database connection to the sqlite database
    :param imgt_version: IMGT database version
    :param ars_mappings: ARSMapping object to ARS mapping tables
    :return: None, updates self
    """
    # Create a Pandas DataFrame from the mac_code list file
    # Skip the header (first 6 lines) and use only the Allele column
    if imgt_version == "Latest":
        allele_list_url = f"{IMGT_HLA_URL}Latest/Allelelist.txt"
    else:
        if imgt_version == "3130":
            # 3130 was renamed to 3131 for Allelelist file only 🤷🏾‍
            imgt_version = "3131"
        allele_list_url = (
            f"{IMGT_HLA_URL}Latest/allelelist/Allelelist.{imgt_version}.txt"
        )
    try:
        allele_df = pd.read_csv(allele_list_url, header=6, usecols=["Allele"])
    except HTTPError as e:
        print(
            f"Failed importing alleles for version {imgt_version} from {allele_list_url}",
            file=sys.stderr,
        )
        sys.exit(1)
    return allele_df


def load_serology_mappings(imgt_version):
    """
    Read `rel_dna_ser.txt` file that contains alleles and their serological equivalents.

    The fields of the Alleles->Serological mapping file are:
       Locus - HLA Locus
       Allele - HLA Allele Name
       USA - Unambiguous Serological Antigen associated with allele
       PSA - Possible Serological Antigen associated with allele
       ASA - Assumed Serological Antigen associated with allele
       EAE - Expert Assigned Exceptions in search determinants of some registries

    EAE is ignored when generating the serology map.
    """
    rel_dna_ser_url = f"{IMGT_HLA_URL}{imgt_version}/wmda/rel_dna_ser.txt"
    # Load WMDA serology mapping data from URL
    df_sero = pd.read_csv(
        rel_dna_ser_url,
        sep=";",
        skiprows=6,
        names=["Locus", "Allele", "USA", "PSA", "ASA", "EAE"],
        index_col=False,
    )
    return df_sero


def load_mac_codes():
    """
    MAC files come in 2 different versions:

    Martin: when they’re printed, the first is better for encoding and the
    second is better for decoding. The entire list was maintained both as an
    Excel spreadsheet and also as a sybase database table. The Excel was the
    one that was printed and distributed.

        **==> numer.v3.txt <==**

        Sorted by the length and the values in the list
        ```
        "LAST UPDATED: 09/30/20"
        CODE	SUBTYPE

        AB	01/02
        AC	01/03
        AD	01/04
        AE	01/05
        AG	01/06
        AH	01/07
        AJ	01/08
        ```

        **==> alpha.v3.txt <==**

        Sorted by the code

        ```
        "LAST UPDATED: 10/01/20"
        *	CODE	SUBTYPE

            AA	01/02/03/05
            AB	01/02
            AC	01/03
            AD	01/04
            AE	01/05
            AF	01/09
            AG	01/06
        ```
    """
    # Load the MAC file to a DataFrame
    mac_url = "https://hml.nmdp.org/mac/files/numer.v3.zip"
    df_mac = pd.read_csv(
        mac_url,
        sep="\t",
        compression="zip",
        skiprows=3,
        names=["Code", "Alleles"],
        keep_default_na=False,
    )
    return df_mac


def load_latest_version():
    from urllib.request import urlopen

    response = urlopen(
        "https://raw.githubusercontent.com/ANHIG/IMGTHLA/Latest/release_version.txt"
    )
    version = 0
    for line in response:
        l = line.decode("utf-8")
        if l.find("version:") != -1:
            # Version line looks like
            # # version: IPD-IMGT/HLA 3.51.0
            version = l.split()[-1].replace(".", "")
    return version
