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
import itertools

import pyard.loader
import pyard.loader.cwd
import pyard.loader.mac_codes
import pyard.loader.serology
from pyard.smart_sort import smart_sort_comparator
from . import db
from .constants import expression_chars
from .loader.allele_list import load_allele_list
from .loader.serology import load_serology_mappings, load_serology_broad_split_mapping
from .loader.version import load_latest_version

from .loader.p_group import load_p_group
from .loader.g_group import load_g_group

from .simple_table import Table

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
from .serology import broad_splits_dna_mapping, SerologyMapping
from .smart_sort import smart_sort_comparator


def expression_reduce(exp_alleles_table):
    """
    For each group of expression alleles, check if __all__ of
    them have the same expression character. If so, the second field
    with the expression character is a valid allele.
    Rule:
        The general rule is that expression characters can propagate up to two
        field level if all three-field and/or four-field alleles have the same
        expression character.

    Given
    allele_groups = {
        'A*01:01': [
            {'AlleleID': 'HLA02169', 'Allele': 'A*01:01:01:02N', '2d': 'A*01:01', '3d': 'A*01:01:01',
             'Exp': 'A*01:01:01:02N'},
            {'AlleleID': 'HLA03587', 'Allele': 'A*01:01:38L', '2d': 'A*01:01', '3d': 'A*01:01:38L',
             'Exp': 'A*01:01:38L'}
        ],
        'A*01:04': [
            {'AlleleID': 'HLA00004', 'Allele': 'A*01:04:01:01N', '2d': 'A*01:04', '3d': 'A*01:04:01',
             'Exp': 'A*01:04:01:01N'},
            {'AlleleID': 'HLA18724', 'Allele': 'A*01:04:01:02N', '2d': 'A*01:04', '3d': 'A*01:04:01',
             'Exp': 'A*01:04:01:02N'}
        ], 'A*01:52': [
            {'AlleleID': 'HLA04761', 'Allele': 'A*01:52:01N', '2d': 'A*01:52', '3d': 'A*01:52:01N',
             'Exp': 'A*01:52:01N'},
            {'AlleleID': 'HLA14127', 'Allele': 'A*01:52:02N', '2d': 'A*01:52', '3d': 'A*01:52:02N',
             'Exp': 'A*01:52:02N'}]
    }


    """
    allele_groups = exp_alleles_table.group_by("2d")
    valid_2d_exp_alleles = dict()
    for allele_2d, allele_group in allele_groups.items():
        # Get the expression characters for the current allele_2d
        expression_chars = {allele["Exp"][-1] for allele in allele_group}

        # Check if all expression characters are the same
        if len(expression_chars) == 1:
            # If all expression characters are the same, return the 2d allele with the expression character
            valid_2d_exp_alleles[allele_2d] = allele_2d + expression_chars.pop()

    return valid_2d_exp_alleles


def join_allele_list(alleles: list):
    return "/".join(sorted(alleles, key=functools.cmp_to_key(smart_sort_comparator)))


def generate_ard_mapping(db_connection: sqlite3.Connection, imgt_version) -> ARSMapping:
    if db.tables_exist(db_connection, ars_mapping_tables):
        return db.load_ars_mappings(db_connection)

    df_g_group = load_g_group(imgt_version)
    df_p_group = load_p_group(imgt_version)

    # compare df_p_group["2d"] with df_g_group["2d"] to find 2-field alleles in the
    # P-group that aren't in the G-group
    p_not_in_g = set(df_p_group["2d"]) - set(df_g_group["2d"])

    # filter to find these 2-field alleles (2d) in the P-group data frame
    # dictionary which will define the table
    p_not_g = df_p_group.where_in("2d", p_not_in_g, ["A", "lgx"]).to_dict("A", "lgx")

    # multiple Gs
    # goal: identify 2-field alleles that are in multiple G-groups
    # group by 2d and G, and select the 2d column and count the columns
    multiple_g = df_g_group.unique(["2d", "G"]).value_counts("2d")
    # filter out the multiple_g with count > 1, leaving only duplicates
    multiple_g_list = multiple_g.where("count > 1")["2d"]

    # Keep only the alleles that have more than 1 mapping as allele list
    dup_g = (
        df_g_group.where_in("2d", multiple_g_list, ["G", "2d"])
        .unique(["G", "2d"])
        .agg("2d", "G", join_allele_list)
        .to_dict("2d", "agg")
    )

    # multiple lgx
    # goal: identify 2-field alleles that are in multiple lgx-groups
    # group by 2d and lgx, and select the 2d column and count the columns
    mlgx = df_g_group.unique(["2d", "lgx"]).value_counts("2d")
    # filter out the mlgx with count > 1, leaving only duplicates
    multiple_lgx_list = mlgx.where("count > 1")["2d"]

    # Keep only the alleles that have more than 1 mapping as allele list
    dup_lgx = (
        df_g_group.where_in("2d", multiple_lgx_list, ["lgx", "2d"])
        .unique(["lgx", "2d"])
        .agg("2d", "lgx", join_allele_list)
        .to_dict("2d", "agg")
    )

    # Extract G group mapping
    g_2d = df_g_group[["2d", "G"]].rename(column_mapping={"2d": "A"})
    g_3d = df_g_group[["3d", "G"]].rename(column_mapping={"3d": "A"})
    g_a = df_g_group[["A", "G"]]
    g_all = g_2d.union(g_3d).union(g_a)
    g_group = g_all.to_dict("A", "G")

    # Extract P group mapping
    p_2d = df_p_group[["2d", "P"]].rename(column_mapping={"2d": "A"})
    p_3d = df_p_group[["3d", "P"]].rename(column_mapping={"3d": "A"})
    p_a = df_p_group[["A", "P"]]
    p_all = p_2d.union(p_3d).union(p_a)
    p_group = p_all.to_dict("A", "P")

    # Extract lgx group mapping
    lgx_2d = df_g_group[["2d", "lgx"]].rename(column_mapping={"2d": "A"})
    lgx_3d = df_g_group[["3d", "lgx"]].rename(column_mapping={"3d": "A"})
    lgx_a = df_g_group[["A", "lgx"]]
    lgx_all = lgx_2d.union(lgx_3d).union(lgx_a)
    lgx_group = lgx_all.to_dict("A", "lgx")

    # Do not keep duplicate alleles for lgx. Issue #333
    # DPA1*02:02/DPA1*02:07 ==> DPA1*02:02
    #
    lowest_numbered_dup_lgx = {
        k: sorted(v.split("/"), key=functools.cmp_to_key(smart_sort_comparator))[0]
        for k, v in dup_lgx.items()
    }
    # Update the lgx_group with the allele with the lowest number
    lgx_group.update(lowest_numbered_dup_lgx)

    # Extract exon mapping
    exon_a = df_g_group[["A", "3d"]].rename(column_mapping={"3d": "exon"})
    exon_group = exon_a.to_dict("A", "exon")

    ars_mapping = ARSMapping(
        dup_g=dup_g,
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

    allele_df = load_allele_list(imgt_version)

    # Create columns of alleles of various fields
    allele_df["1d"] = allele_df["Allele"].apply(get_1field_allele)
    allele_df["2d"] = allele_df["Allele"].apply(get_2field_allele)
    allele_df["3d"] = allele_df["Allele"].apply(get_3field_allele)
    allele_df["Exp"] = allele_df["Allele"].apply(
        lambda a: a if a[-1] in expression_chars and number_of_fields(a) > 2 else None
    )
    exp_alleles_table = allele_df.where_not_null("Exp")
    exp_alleles = expression_reduce(exp_alleles_table)

    # Create valid set of alleles:
    # All full length alleles
    # All 3rd and 2nd field versions of longer alleles
    # All 2-field version of alleles with expression that can be reduced
    valid_alleles = (
        set(allele_df["Allele"])
        .union(set(allele_df["2d"]))
        .union(set(allele_df["3d"]))
        .union(set(exp_alleles.values()))
    )
    valid_alleles = sorted(valid_alleles)

    # unique_2d = allele_df.unique('2d')
    # xx_code_1d = unique_2d.apply(lambda x: x.split(":")[0])
    # xx_mapping = itertools.groupby(zip(xx_code_1d, unique_2d), key=lambda x: x[0])
    # xx_codes = {k: [x[1] for x in list(g)] for k, g in xx_mapping}
    #

    xx_codes = allele_df.agg("1d", "2d", list)

    # Update xx codes with broads and splits
    for broad, splits in broad_splits_dna_mapping.items():
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

    a1d = allele_df[["Allele", "1d"]].rename(column_mapping={"1d": "nd"})
    a2d = allele_df[["Allele", "2d"]].rename(column_mapping={"2d": "nd"})
    a3d = allele_df[["Allele", "3d"]].rename(column_mapping={"3d": "nd"})
    ag = Table(ars_mappings.g_group.items(), columns=["Allele", "nd"])
    ap = Table(ars_mappings.p_group.items(), columns=["Allele", "nd"])
    who_codes = a1d.union(a2d).union(a3d).union(ag).union(ap)

    # drop duplicates
    unique_who_codes = who_codes.unique(["Allele", "nd"])
    # remove valid alleles from who_codes to avoid recursion
    # who_codes1.remove('nd', who_alleles)
    # who_codes maps a first field name to its G field expansion
    who_group = unique_who_codes.agg("nd", "Allele", list)
    # dictionary
    # flat_who_group = who_group.to_dict()
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
                shortnulls[a_shortnull] = "/".join(
                    sorted(
                        expression_alleles[a_shortnull],
                        key=functools.cmp_to_key(smart_sort_comparator),
                    )
                )

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
            df_mac = pyard.loader.mac_codes.load_mac_codes()
            # Create a dict from code to alleles
            mac = df_mac.to_dict()
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


def generate_serology_mapping(
    db_connection: sqlite3.Connection,
    imgt_version: str,
    serology_mapping: SerologyMapping,
    redux_function,
):
    if not db.table_exists(db_connection, "serology_mapping"):
        df_sero = load_serology_mappings(imgt_version)

        df_sero["Locus*Allele"] = df_sero.concat_columns(["Locus", "Allele"])

        # Remove 0 and ? from USA
        usa = df_sero.where("USA is not null and USA not in ('0', '?')")
        usa["Sero"] = usa.concat_columns(["Locus", "USA"])

        psa = df_sero.where_not_null("PSA")
        psa = psa.explode("PSA", "/")
        psa = psa.where("PSA not in ('0', '?')")
        psa["Sero"] = psa.concat_columns(["Locus", "PSA"])

        asa = df_sero.where_not_null("ASA")
        asa = asa.explode("ASA", "/")
        asa = asa.where("ASA not in ('0', '?')")
        asa["Sero"] = asa.concat_columns(["Locus", "ASA"])

        sero_mapping_combined = (
            usa[["Sero", "Locus*Allele"]]
            .union(psa[["Sero", "Locus*Allele"]])
            .union(asa[["Sero", "Locus*Allele"]])
        )

        # Map to only valid serological antigen name
        sero_mapping_combined["Sero"] = sero_mapping_combined["Sero"].apply(
            to_serological_name
        )
        sero_mapping_combined["lgx"] = sero_mapping_combined["Locus*Allele"].apply(
            lambda allele: redux_function(allele, "lgx")
        )
        sero_allele_mapping = sero_mapping_combined.agg("Sero", "Locus*Allele", set)
        sero_lgx_mapping = sero_mapping_combined.agg("Sero", "lgx", set)
        sero_mapping = {
            k: (sero_allele_mapping[k], sero_lgx_mapping[k])
            for k in sero_allele_mapping.keys()
        }

        # map alleles for split serology to their corresponding broad
        # Update xx codes with broads and splits
        for broad, splits in serology_mapping.broad_splits_map.items():
            for split in splits:
                try:
                    sero_mapping[broad] = (
                        sero_mapping[broad][0].union(sero_mapping[split][0]),
                        sero_mapping[broad][1].union(sero_mapping[split][1]),
                    )
                except KeyError:
                    if split in sero_mapping:
                        sero_mapping[broad] = sero_mapping[split]

        # Create a mapping of serology to alleles, lgx_alleles and associated XX allele
        serology_xx_mapping = serology_mapping.get_xx_mappings()
        # re-sort allele lists into smart-sort order
        for sero in serology_xx_mapping:
            if sero in sero_mapping:
                sero_mapping[sero] = (
                    "/".join(
                        sorted(
                            sero_mapping[sero][0],
                            key=functools.cmp_to_key(smart_sort_comparator),
                        )
                    ),
                    "/".join(
                        sorted(
                            sero_mapping[sero][1],
                            key=functools.cmp_to_key(smart_sort_comparator),
                        ),
                    ),
                    serology_xx_mapping[sero],
                )
            else:
                sero_mapping[sero] = (None, None, serology_xx_mapping[sero])

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


def generate_broad_splits_mapping(db_connection: sqlite3.Connection, imgt_version):
    if not db.tables_exist(
        db_connection, ["serology_broad_split_mapping", "serology_associated_mappings"]
    ):
        sero_mapping, associated_mapping = load_serology_broad_split_mapping(
            imgt_version
        )

        # Save the `splits` as a "/" delimited string to db
        db.save_serology_broad_split_mappings(db_connection, sero_mapping.to_dict())
        db.save_serology_associated_mappings(
            db_connection, associated_mapping.to_dict()
        )

    sero_mapping = db.load_serology_broad_split_mappings(db_connection)
    associated_mapping = db.load_serology_associated_mappings(db_connection)

    return sero_mapping, associated_mapping


def generate_cwd_mapping(db_connection: sqlite3.Connection):
    if not db.table_exists(db_connection, "cwd2"):
        cwd2_map = pyard.loader.cwd.load_cwd2()
        db.save_cwd2(db_connection, cwd2_map)
