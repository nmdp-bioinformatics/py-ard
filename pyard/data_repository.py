# -*- coding: utf-8 -*-
#
#    py-ard
#    Copyright (c) 2023 Be The Match operated by National Marrow Donor Program. All Rights Reserved.
#
#    This library is free software; you can redistribute it and/or modify it
#    under the terms of the GNU Lesser General Public License as published
#    by the Free Software Foundation; either version 3 of the License, or (at
#    your option) any later version.
#
#    This library is distributed in the hope that it will be useful, but WITHOUT
#    ANY WARRANTY; with out even the implied warranty of MERCHANTABILITY or
#    FITNESS FOR A PARTICULAR PURPOSE.  See the GNU Lesser General Public
#    License for more details.
#
#    You should have received a copy of the GNU Lesser General Public License
#    along with this library;  if not, write to the Free Software Foundation,
#    Inc., 59 Temple Place, Suite 330, Boston, MA 02111-1307  USA.
#
#    > http://www.fsf.org/licensing/licenses/lgpl.html
#    > http://www.opensource.org/licenses/lgpl-license.php
#
import copy
import functools
import sqlite3

import pyard.load
from pyard.smart_sort import smart_sort_comparator
from . import db, broad_splits
from .load import (
    load_g_group,
    load_p_group,
    load_allele_list,
    load_serology_mappings,
    load_latest_version,
)
from .constants import expression_chars
from .mappings import (
    ars_mapping_tables,
    ARSMapping,
    code_mapping_tables,
    AlleleGroups,
    CodeMappings,
    allele_tables,
)
from .misc import (
    get_2field_allele,
    get_3field_allele,
    number_of_fields,
    get_1field_allele,
)


def expression_reduce(df):
    """
    For each group of expression alleles, check if __all__ of
    them have the same expression character. If so, the second field
    with the expression character is a valid allele.
    Rule:
        The general rule is that expression characters can propagate up to two
        field level if all three-field and/or four-field alleles have the same
        expression character.

    :param df: dataframe with Allele column that is all expression characters
    :return: 2 field allele or None
    """
    for e in expression_chars:
        if df["Allele"].str.endswith(e).all():
            return df["2d"].iloc[0] + e
    return None


def generate_ard_mapping(db_connection: sqlite3.Connection, imgt_version) -> ARSMapping:
    if db.tables_exist(db_connection, ars_mapping_tables):
        return db.load_ars_mappings(db_connection)

    import pandas as pd

    df_g_group = load_g_group(imgt_version)
    df_p_group = load_p_group(imgt_version)

    # Extract p group mapping
    p_group = df_p_group.set_index("A")["P"].to_dict()

    # compare df_p_group["2d"] with df_g_group["2d"] to find 2-field alleles in the
    # P-group that aren't in the G-group
    p_not_in_g = set(df_p_group["2d"]) - set(df_g_group["2d"])

    # filter to find these 2-field alleles (2d) in the P-group data frame
    df_p_not_g = df_p_group[df_p_group["2d"].isin(p_not_in_g)]

    # dictionary which will define the table
    p_not_g = df_p_not_g.set_index("A")["lgx"].to_dict()

    # multiple Gs
    # goal: identify 2-field alleles that are in multiple G-groups

    # group by 2d and G, and select the 2d column and count the columns
    mg = df_g_group.drop_duplicates(["2d", "G"])["2d"].value_counts()
    # filter out the mg with count > 1, leaving only duplicates
    # take the index from the 2d version the data frame, make that a column
    # and turn that into a list
    multiple_g_list = mg[mg > 1].reset_index()["index"].to_list()

    # Keep only the alleles that have more than 1 mapping
    dup_g = (
        df_g_group[df_g_group["2d"].isin(multiple_g_list)][["G", "2d"]]
        .drop_duplicates()
        .groupby("2d", as_index=True)
        .agg("/".join)
        .to_dict()["G"]
    )

    # multiple lgx
    mlgx = df_g_group.drop_duplicates(["2d", "lgx"])["2d"].value_counts()
    multiple_lgx_list = mlgx[mlgx > 1].reset_index()["index"].to_list()

    # Keep only the alleles that have more than 1 mapping
    dup_lgx = (
        df_g_group[df_g_group["2d"].isin(multiple_lgx_list)][["lgx", "2d"]]
        .drop_duplicates()
        .groupby("2d", as_index=True)
        .agg("/".join)
        .to_dict()["lgx"]
    )

    # Creating dictionaries with mac_code->ARD group mapping
    df_g = pd.concat(
        [
            df_g_group[["2d", "G"]].rename(columns={"2d": "A"}),
            df_g_group[["3d", "G"]].rename(columns={"3d": "A"}),
            df_g_group[["A", "G"]],
        ],
        ignore_index=True,
    )
    g_group = df_g.set_index("A")["G"].to_dict()

    df_lgx = pd.concat(
        [
            df_g_group[["2d", "lgx"]].rename(columns={"2d": "A"}),
            df_g_group[["3d", "lgx"]].rename(columns={"3d": "A"}),
            df_g_group[["A", "lgx"]],
        ]
    )
    lgx_group = df_lgx.set_index("A")["lgx"].to_dict()

    # exon
    df_exon = pd.concat(
        [
            df_g_group[["A", "3d"]].rename(columns={"3d": "exon"}),
        ]
    )
    exon_group = df_exon.set_index("A")["exon"].to_dict()

    ars_mapping = ARSMapping(
        dup_g=dup_g,
        dup_lgx=dup_lgx,
        g_group=g_group,
        p_group=p_group,
        lgx_group=lgx_group,
        exon_group=exon_group,
        p_not_g=p_not_g,
    )
    db.save_ars_mappings(db_connection, ars_mapping)

    return ars_mapping


def generate_alleles_and_xx_codes_and_who(
    db_connection: sqlite3.Connection, imgt_version, ars_mappings
):
    if db.tables_exist(db_connection, code_mapping_tables + allele_tables):
        return db.load_code_mappings(db_connection)

    import pandas as pd

    allele_df = load_allele_list(imgt_version)

    # Create a set of valid alleles
    # All 2-field, 3-field and the original Alleles are considered valid alleles
    allele_df["2d"] = allele_df["Allele"].apply(get_2field_allele)
    allele_df["3d"] = allele_df["Allele"].apply(get_3field_allele)
    # For all Alleles with expression characters, find 2-field valid alleles
    exp_alleles = allele_df[
        allele_df["Allele"].apply(
            lambda a: a[-1] in expression_chars and number_of_fields(a) > 2
        )
    ]
    exp_alleles = exp_alleles.groupby("2d").apply(expression_reduce).dropna()

    # Create valid set of alleles:
    # All full length alleles
    # All 3rd and 2nd field versions of longer alleles
    # All 2-field version of alleles with expression that can be reduced
    valid_alleles = (
        set(allele_df["Allele"])
        .union(set(allele_df["2d"]))
        .union(set(allele_df["3d"]))
        .union(set(exp_alleles))
    )

    # Create xx_codes mapping from the unique alleles in 2-field column
    xx_df = pd.DataFrame(allele_df["2d"].unique(), columns=["Allele"])
    # Also create a first-field column
    xx_df["1d"] = xx_df["Allele"].apply(lambda x: x.split(":")[0])
    # xx_codes maps a first field name to its 2 field expansion
    xx_codes = xx_df.groupby(["1d"]).apply(lambda x: list(x["Allele"])).to_dict()

    # Update xx codes with broads and splits
    for broad, splits in broad_splits.broad_splits_dna_mapping.items():
        for split in splits:
            if broad in xx_codes:
                xx_codes[broad].extend(xx_codes[split])
            else:
                xx_codes[broad] = copy.deepcopy(xx_codes[split])

    # Save this version of xx codes
    flat_xx_codes = {
        k: "/".join(sorted(v, key=functools.cmp_to_key(smart_sort_comparator)))
        for k, v in xx_codes.items()
    }

    # W H O
    who_alleles = allele_df["Allele"].to_list()

    # Create WHO mapping from the unique alleles in the 1-field column
    allele_df["1d"] = allele_df["Allele"].apply(get_1field_allele)

    who_codes = pd.concat(
        [
            allele_df[["Allele", "1d"]].rename(columns={"1d": "nd"}),
            allele_df[["Allele", "2d"]].rename(columns={"2d": "nd"}),
            allele_df[["Allele", "3d"]].rename(columns={"3d": "nd"}),
            pd.DataFrame(ars_mappings.g_group.items(), columns=["Allele", "nd"]),
            pd.DataFrame(ars_mappings.p_group.items(), columns=["Allele", "nd"]),
        ],
        ignore_index=True,
    )

    # remove valid alleles from who_codes to avoid recursion
    for k in who_alleles:
        if k in who_codes["nd"]:
            who_codes.drop(labels=k, axis="index")

    # drop duplicates
    who_codes = who_codes.drop_duplicates()

    # who_codes maps a first field name to its 2 field expansion
    who_group = who_codes.groupby(["nd"]).apply(lambda x: list(x["Allele"])).to_dict()

    # dictionary
    flat_who_group = {
        k: "/".join(sorted(v, key=functools.cmp_to_key(smart_sort_comparator)))
        for k, v in who_group.items()
    }

    db.save_code_mappings(
        db_connection,
        exp_alleles,
        flat_who_group,
        flat_xx_codes,
        valid_alleles,
        who_alleles,
    )

    return (
        CodeMappings(xx_codes=xx_codes, who_group=who_group),
        AlleleGroups(
            alleles=valid_alleles, who_alleles=who_alleles, exp_alleles=exp_alleles
        ),
    )

    # return valid_alleles, who_alleles, xx_codes, who_group, exp_alleles


def generate_short_nulls(db_connection, who_group):
    if db.table_exists(db_connection, "shortnulls"):
        return db.load_shortnulls(db_connection)

    # shortnulls
    # scan WHO alleles for those with expression characters and make shortnull mappings
    # DRB4*01:03N | DRB4*01:03:01:02N/DRB4*01:03:01:13N
    # DRB5*01:08N | DRB5*01:08:01N/DRB5*01:08:02N
    shortnulls = dict()
    for who in who_group:
        # e.g. DRB4*01:03
        expression_alleles = dict()
        if who[-1] not in expression_chars and who[-1] not in ["G", "P"] and ":" in who:
            for an_allele in who_group[who]:
                # if an allele in a who_group has an expression character but the group allele doesnt,
                # add it to shortnulls
                last_char = an_allele[-1]
                if last_char in expression_chars:
                    # e.g. DRB4*01:03:01:02N
                    a_shortnull = who + last_char
                    if a_shortnull not in expression_alleles:
                        expression_alleles[a_shortnull] = []
                    expression_alleles[a_shortnull].append(an_allele)
            # only create a shortnull if there is one expression character in this who_group
            # there is nothing to be done for who_groups that have both Q and L for example
            for a_shortnull in expression_alleles:
                # e.g. DRB4*01:03N
                shortnulls[a_shortnull] = "/".join(expression_alleles[a_shortnull])

    db.save_shortnulls(db_connection, shortnulls)

    shortnulls = {k: v.split("/") for k, v in shortnulls.items()}
    return shortnulls


def generate_mac_codes(
    db_connection: sqlite3.Connection, refresh_mac: bool = False, load_mac: bool = True
):
    """
    :param db_connection: Database connection to the sqlite database
    :param refresh_mac: Refresh the database with newer MAC data ?
    :param load_mac: Should MAC be loaded at all
    :return: None
    """
    if load_mac:
        mac_table_name = "mac_codes"
        if refresh_mac or not db.table_exists(db_connection, mac_table_name):
            df_mac = pyard.load.load_mac_codes()
            # Create a dict from code to alleles
            mac = df_mac.set_index("Code")["Alleles"].to_dict()
            db.save_mac_codes(db_connection, mac, mac_table_name)


def to_serological_name(locus_name: str):
    """
    Map a DNA Allele name to Serological Equivalent.
    http://hla.alleles.org/antigens/recognised_serology.html
    Eg:
      A*1 -> A1
      ...
      DRB5*51 -> DR51
    :param locus_name: DNA Locus Name
    :return: Serological equivalent
    """
    locus, sero_number = locus_name.split("*")
    sero_locus = locus[:2]
    if sero_locus == "C":
        sero_locus = "Cw"
    sero_name = sero_locus + sero_number
    return sero_name


def generate_serology_mapping(db_connection: sqlite3.Connection, imgt_version):
    if not db.table_exists(db_connection, "serology_mapping"):
        df_sero = load_serology_mappings(imgt_version)

        import pandas as pd

        # Remove 0 and ? from USA
        df_sero = df_sero[(df_sero["USA"] != "0") & (df_sero["USA"] != "?")]
        df_sero["Allele"] = df_sero.loc[:, "Locus"] + df_sero.loc[:, "Allele"]

        usa = df_sero[["Locus", "Allele", "USA"]].dropna()
        usa["Sero"] = usa["Locus"] + usa["USA"]

        psa = df_sero[["Locus", "Allele", "PSA"]].dropna()
        psa["PSA"] = psa["PSA"].apply(lambda row: row.split("/"))
        psa = psa.explode("PSA")
        psa = psa[(psa["PSA"] != "0") & (psa["PSA"] != "?")].dropna()
        psa["Sero"] = psa["Locus"] + psa["PSA"]

        asa = df_sero[["Locus", "Allele", "ASA"]].dropna()
        asa["ASA"] = asa["ASA"].apply(lambda x: x.split("/"))
        asa = asa.explode("ASA")
        asa = asa[(asa["ASA"] != "0") & (asa["ASA"] != "?")].dropna()
        asa["Sero"] = asa["Locus"] + asa["ASA"]

        sero_mapping_combined = pd.concat(
            [usa[["Sero", "Allele"]], psa[["Sero", "Allele"]], asa[["Sero", "Allele"]]]
        )

        # Map to only valid serological antigen name
        sero_mapping_combined["Sero"] = sero_mapping_combined["Sero"].apply(
            to_serological_name
        )

        sero_mapping = (
            sero_mapping_combined.groupby("Sero")
            .apply(lambda x: "/".join(sorted(x["Allele"])))
            .to_dict()
        )

        # map alleles for split serology to their corresponding broad
        # Update xx codes with broads and splits
        for broad, splits in broad_splits.broad_splits_ser_mapping.items():
            for split in splits:
                try:
                    sero_mapping[broad] = "/".join(
                        [sero_mapping[broad], sero_mapping[split]]
                    )
                except KeyError:
                    if split in sero_mapping:
                        sero_mapping[broad] = sero_mapping[split]

        # re-sort allele lists into smartsort order
        for sero in sero_mapping.keys():
            sero_mapping[sero] = "/".join(
                sorted(
                    sero_mapping[sero].split("/"),
                    key=functools.cmp_to_key(smart_sort_comparator),
                )
            )

        db.save_serology_mappings(db_connection, sero_mapping)


def generate_v2_to_v3_mapping(db_connection: sqlite3.Connection, imgt_version):
    if not db.table_exists(db_connection, "v2_mapping"):
        db.load_v2_v3_mappings(db_connection)


def set_db_version(db_connection: sqlite3.Connection, imgt_version):
    """
    Set the IMGT database version number as a user_version string in
    the database itself.

    :param db_connection: Active SQLite Connection
    :param imgt_version: current imgt_version
    """
    # If version already exists, don't reset
    version = db.get_user_version(db_connection)
    if version:
        return version

    if imgt_version == "Latest":
        version = load_latest_version()
    else:
        version = imgt_version

    db.set_user_version(db_connection, int(version))
    print("Version:", version)
    return version


def get_db_version(db_connection: sqlite3.Connection):
    return db.get_user_version(db_connection)


def generate_serology_broad_split_mapping(
    db_connection: sqlite3.Connection, imgt_version
):
    if not db.table_exists(db_connection, "serology_broad_split_mapping"):
        sero_mapping = pyard.load.load_serology_broad_split_mapping(imgt_version)
        db.save_serology_broad_split_mappings(db_connection, sero_mapping)
        return sero_mapping

    return db.load_serology_broad_split_mappings(db_connection)


def generate_cwd_mapping(db_connection: sqlite3.Connection):
    if not db.table_exists(db_connection, "cwd2"):
        cwd2_map = pyard.load.load_cwd2()
        db.save_cwd2(db_connection, cwd2_map)
