from typing import Dict, List

import pandas as pd

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
