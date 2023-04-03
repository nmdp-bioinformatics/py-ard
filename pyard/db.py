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
import pathlib
import sqlite3
from typing import Tuple, Dict, Set, List

from .mappings import ARSMapping, CodeMappings, AlleleGroups
from .misc import get_imgt_db_versions, get_default_db_directory


def create_db_connection(data_dir, imgt_version, ro=False):
    """
    Create a  connection to a sqlite database in read-only mode
    or read-write mode (default)

    :param data_dir: The directory where the db is/will be created
    :param imgt_version: IMGT db version
    :param ro: Read-only mode ?
    :return: db connection of type sqlite.Connection
    """
    # Set data directory where all the downloaded files will go
    if data_dir is None:
        data_dir = get_default_db_directory()

    db_filename = f"{data_dir}/pyard-{imgt_version}.sqlite3"

    if ro:
        # If in read-only mode, make sure the db file exists
        if not pathlib.Path(db_filename).exists():
            raise RuntimeError(f"Reference Database {db_filename}  not available.")
        # Open the database in read-only mode
        file_uri = f"file:{db_filename}?mode=ro"
        # Multiple threads can access the same connection since it's only ro
        return sqlite3.connect(file_uri, check_same_thread=False, uri=True), db_filename

    # Check the imgt_version is a valid IMGT DB Version
    # by querying the IMGT site
    if imgt_version != "Latest":
        if not pathlib.Path(db_filename).exists():
            all_imgt_versions = get_imgt_db_versions()
            if imgt_version not in all_imgt_versions:
                raise ValueError(
                    f"{imgt_version} is not a valid IMGT database version."
                )

    # Create the data directory if it doesn't exist
    if not pathlib.Path(data_dir).exists():
        pathlib.Path(data_dir).mkdir(parents=True, exist_ok=True)

    if not pathlib.Path(db_filename).exists():
        print(f"Creating {db_filename} as cache.")

    # Open the database for read/write
    file_uri = f"file:{db_filename}"
    return sqlite3.connect(file_uri, uri=True), db_filename


def table_exists(connection: sqlite3.Connection, table_name: str) -> bool:
    """
    Does the table exist in the database ?

    :param connection: db connection of type sqlite.Connection
    :param table_name: table in the sqlite db
    :return: bool indicating whether table_name exists as a table
    """
    query = """SELECT count(*) from sqlite_master where type = 'table' and name = ?"""
    cursor = connection.execute(query, (table_name,))
    result = cursor.fetchone()
    cursor.close()
    return result[0] > 0


def tables_exist(connection: sqlite3.Connection, table_names: List[str]):
    """
    Do all the given tables exist in the database ?

    :param connection: db connection of type sqlite.Connection
    :param table_names: names of tables in the sqlite db
    :return: bool indicating whether all table_names exists
    """
    return all([table_exists(connection, table_name) for table_name in table_names])


def count_rows(connection: sqlite3.Connection, table_name: str) -> int:
    """
    Count number of rows in the table.

    :param connection: db connection of type sqlite.Connection
    :param table_name: table in the sqlite db
    :return: bool indicating whether table_name exists as a table
    """
    query = f"SELECT count(*) from '{table_name}'"
    cursor = connection.execute(query)
    result = cursor.fetchone()
    cursor.close()
    return result[0]


def mac_code_to_alleles(connection: sqlite3.Connection, code: str) -> List[str]:
    """
    Look up the MAC code in the database and return corresponding list
    of alleles.
    :param connection: db connection of type sqlite.Connection
    :param code: MAC code
    :return: List of alleles
    """
    mac_query = "SELECT alleles from mac_codes where code = ?"
    cursor = connection.execute(mac_query, (code,))
    result = cursor.fetchone()
    cursor.close()
    if result:
        alleles = result[0].split("/")
    else:
        alleles = []
    return alleles


def alleles_to_mac_code(
    connection: sqlite3.Connection, code_expansion: str
) -> List[str]:
    """
    Look up the MAC code in the database and based on list of allele expansion
    :param connection: db connection of type sqlite.Connection
    :param code_expansion: expansion of MAC code
    :return: List of alleles
    """
    mac_query = "SELECT code from mac_codes where alleles = ?"
    cursor = connection.execute(mac_query, (code_expansion,))
    result = cursor.fetchone()
    cursor.close()
    if result:
        return result[0]
    return None


def is_valid_mac_code(connection: sqlite3.Connection, code: str) -> bool:
    """
    Check db if the MAC code exists.

    :param connection: db connection of type sqlite.Connection
    :param code: MAC code
    :return: code is MAC code ?
    """
    mac_query = "SELECT count(alleles) from mac_codes where code = ?"
    cursor = connection.execute(mac_query, (code,))
    result = cursor.fetchone()
    cursor.close()
    return result[0] > 0


def serology_to_alleles(connection: sqlite3.Connection, serology: str) -> List[str]:
    """
    Look up Serology in the database and return corresponding list of alleles.

    :param connection: db connection of type sqlite.Connection
    :param serology: Serology
    :return: List of alleles
    """
    serology_query = "SELECT allele_list from serology_mapping where serology = ?"
    cursor = connection.execute(serology_query, (serology,))
    result = cursor.fetchone()
    cursor.close()
    if result:
        alleles = result[0].split("/")
    else:
        alleles = []
    return alleles


def is_valid_serology(connection: sqlite3.Connection, serology: str) -> bool:
    """
    Check db if the serology exists

    :param connection: db connection of type sqlite.Connection
    :param serology: serology to test
    :return: is it serology ?
    """
    serology_query = (
        "SELECT count(allele_list) from serology_mapping where serology = ?"
    )
    cursor = connection.execute(serology_query, (serology,))
    result = cursor.fetchone()
    cursor.close()
    return result[0] > 0


def v2_to_v3_allele(connection: sqlite3.Connection, v2_allele: str) -> str:
    """
    Look up V3 version of the allele in the database.

    :param connection: db connection of type sqlite.Connection
    :param v2_allele: V2 allele
    :return: V3 allele
    """
    v2_query = "SELECT v3 from v2_mapping where v2 = ?"
    cursor = connection.execute(v2_query, (v2_allele,))
    result = cursor.fetchone()
    cursor.close()
    if result:
        return result[0]
    return None


def save_dict(
    connection: sqlite3.Connection,
    table_name: str,
    dictionary: Dict[str, str],
    columns: Tuple[str, str],
) -> bool:
    """
    Save the dictionary as a table with column names from columns Tuple.

    :param connection: db connection of type sqlite.Connection
    :param table_name: name of the table to create
    :param dictionary: the dictionary which to take the key and values from
    :param columns: column names in the table
    :return: success status
    """
    cursor = connection.cursor()

    # Drop the table first
    drop_table_sql = f"DROP TABLE IF EXISTS {table_name}"
    cursor.execute(drop_table_sql)

    # Create table
    create_table_sql = f"""CREATE TABLE {table_name} (
                            {columns[0]} TEXT PRIMARY KEY,
                            {columns[1]} TEXT NOT NULL
                    )"""
    cursor.execute(create_table_sql)

    # insert
    cursor.executemany(f"INSERT INTO {table_name} VALUES (?, ?)", dictionary.items())

    # commit transaction - writes to the db
    connection.commit()
    # close the cursor
    cursor.close()

    return True


def save_set(
    connection: sqlite3.Connection, table_name: str, rows: Set, column: str
) -> bool:
    """
    Save the set rows to the table table_name in the column

    :param connection: db connection of type sqlite.Connection
    :param table_name: name of the table to create
    :param rows: set which will become the the column in the table
    :param column: name of the column in the table
    :return: success status
    """
    cursor = connection.cursor()

    # Drop the table first
    drop_table_sql = f"DROP TABLE IF EXISTS {table_name}"
    cursor.execute(drop_table_sql)

    # Create table
    create_table_sql = f"""CREATE TABLE {table_name} (
                            {column} TEXT PRIMARY KEY
                    )"""
    cursor.execute(create_table_sql)

    # insert
    cursor.executemany(
        f"INSERT INTO {table_name} VALUES (?)",
        zip(
            rows,
        ),
    )

    # commit transaction - writes to the db
    connection.commit()
    # close the cursor
    cursor.close()

    return True


def load_set(connection: sqlite3.Connection, table_name: str, column: str) -> Set:
    """
    Retrieve the first column of the table as a set

    :param connection: db connection of type sqlite.Connection
    :param table_name: name of the table to query
    :param column: name of the column in the table to query
    :return: set containing values from the column
    """
    cursor = connection.cursor()
    select_all_query = f"SELECT {column} FROM {table_name}"
    cursor.execute(select_all_query)
    table_as_set = set(map(lambda t: t[0], cursor.fetchall()))
    cursor.close()
    return table_as_set


def load_cwd(connection: sqlite3.Connection, locus: str) -> Set:
    """
    Retrieve the CWD Version 2 alleles for a locus as a set

    :param connection: db connection of type sqlite.Connection
    :param locus: name of the column in the table to query
    :return: CWD allele set
    """
    cursor = connection.cursor()
    select_all_query = f"SELECT allele FROM cwd2 where locus='{locus}'"
    cursor.execute(select_all_query)
    table_as_set = set(map(lambda t: t[0], cursor.fetchall()))
    cursor.close()
    return table_as_set


def load_dict(
    connection: sqlite3.Connection, table_name: str, columns: Tuple[str, str]
) -> Dict[str, str]:
    """
    Retrieve the values in columns as a name, value pair and create a dict.

    :param connection: db connection of type sqlite.Connection
    :param table_name: name of the table to query
    :param columns: column names in the table
    :return: a dict containing key,value pairs from the columns
    """
    cursor = connection.cursor()
    select_all_query = f"SELECT {columns[0]}, {columns[1]} FROM {table_name}"
    cursor.execute(select_all_query)
    table_as_dict = {k: v for k, v in cursor.fetchall()}
    cursor.close()
    return table_as_dict


def similar_alleles(connection: sqlite3.Connection, allele_name: str) -> Set[str]:
    """
    Find similar alleles starting with the provided allele_name.

    :param connection: db connection of type sqlite.Connection
    :param allele_name: Allele name to use as a prefix to find similar alleles
    :return: list of similar alleles
    """
    query = "SELECT allele FROM alleles WHERE allele LIKE ?"
    cursor = connection.execute(query, (f"{allele_name}%",))
    result = cursor.fetchall()
    # fetchall() returns a list of tuples of results
    # e.g. [('C*04:09N',)]
    # Get out the first value of the tuple from the result list
    alleles = set(map(lambda t: t[0], result))
    return alleles


def get_user_version(connection: sqlite3.Connection) -> int:
    """
    Retrieve user_version from db

    :connection: sqlite3.Connection: SQLite DB Connection
    """
    query = "PRAGMA user_version"
    cursor = connection.execute(query)
    result = cursor.fetchone()
    version = result[0]
    cursor.close()

    if version:
        return version
    return None


def set_user_version(connection: sqlite3.Connection, version: int):
    """
    Save the version number as user_version in db

    :connection: sqlite3.Connection:
    :version: int: version number to store
    @return:
    """
    query = f"PRAGMA user_version={version}"
    cursor = connection.execute(query)
    # commit transaction - writes to the db
    connection.commit()
    # close the cursor
    cursor.close()


def load_ars_mappings(db_connection):
    dup_g = load_dict(db_connection, table_name="dup_g", columns=("allele", "g_group"))
    dup_lgx = load_dict(
        db_connection, table_name="dup_lgx", columns=("allele", "lgx_group")
    )
    g_group = load_dict(db_connection, table_name="g_group", columns=("allele", "g"))
    p_group = load_dict(db_connection, table_name="p_group", columns=("allele", "p"))
    lgx_group = load_dict(
        db_connection, table_name="lgx_group", columns=("allele", "lgx")
    )
    exon_group = load_dict(
        db_connection, table_name="exon_group", columns=("allele", "exon")
    )
    p_not_g = load_dict(db_connection, table_name="p_not_g", columns=("allele", "lgx"))
    return ARSMapping(
        dup_g=dup_g,
        dup_lgx=dup_lgx,
        g_group=g_group,
        p_group=p_group,
        lgx_group=lgx_group,
        exon_group=exon_group,
        p_not_g=p_not_g,
    )


def save_ars_mappings(db_connection: sqlite3.Connection, ars_mapping: ARSMapping):
    save_dict(
        db_connection,
        table_name="p_not_g",
        dictionary=ars_mapping.p_not_g,
        columns=("allele", "lgx"),
    )
    save_dict(
        db_connection,
        table_name="dup_g",
        dictionary=ars_mapping.dup_g,
        columns=("allele", "g_group"),
    )
    save_dict(
        db_connection,
        table_name="dup_lgx",
        dictionary=ars_mapping.dup_lgx,
        columns=("allele", "lgx_group"),
    )
    save_dict(
        db_connection,
        table_name="g_group",
        dictionary=ars_mapping.g_group,
        columns=("allele", "g"),
    )
    save_dict(
        db_connection,
        table_name="p_group",
        dictionary=ars_mapping.p_group,
        columns=("allele", "p"),
    )
    save_dict(
        db_connection,
        table_name="lgx_group",
        dictionary=ars_mapping.lgx_group,
        columns=("allele", "lgx"),
    )
    save_dict(
        db_connection,
        table_name="exon_group",
        dictionary=ars_mapping.exon_group,
        columns=("allele", "exon"),
    )


def save_code_mappings(
    db_connection,
    exp_alleles,
    flat_who_group,
    flat_xx_codes,
    valid_alleles,
    who_alleles,
):
    save_dict(db_connection, "exp_alleles", exp_alleles, ("exp_allele", "allele_list"))
    save_dict(db_connection, "xx_codes", flat_xx_codes, ("allele_1d", "allele_list"))
    # Save this version of the valid alleles
    save_set(db_connection, "alleles", valid_alleles, "allele")
    # Save this version of the WHO alleles
    save_set(db_connection, "who_alleles", who_alleles, "allele")
    save_dict(
        db_connection, "who_group", flat_who_group, columns=("who", "allele_list")
    )


def load_code_mappings(db_connection):
    valid_alleles = load_set(db_connection, "alleles", "allele")
    who_alleles = load_set(db_connection, "who_alleles", "allele")
    who_group = load_dict(db_connection, "who_group", ("who", "allele_list"))
    who_group = {k: v.split("/") for k, v in who_group.items()}
    xx_codes = load_dict(db_connection, "xx_codes", ("allele_1d", "allele_list"))
    xx_codes = {k: v.split("/") for k, v in xx_codes.items()}
    exp_alleles = load_dict(db_connection, "exp_alleles", ("exp_allele", "allele_list"))
    exp_alleles = {k: v.split("/") for k, v in exp_alleles.items()}
    return (
        CodeMappings(xx_codes=xx_codes, who_group=who_group),
        AlleleGroups(
            alleles=valid_alleles, who_alleles=who_alleles, exp_alleles=exp_alleles
        ),
    )


def load_shortnulls(db_connection):
    shortnulls = load_dict(db_connection, "shortnulls", ("shortnull", "allele_list"))
    shortnulls = {k: v.split("/") for k, v in shortnulls.items()}
    return shortnulls


def save_shortnulls(db_connection, shortnulls):
    save_dict(db_connection, "shortnulls", shortnulls, ("shortnull", "allele_list"))


def save_mac_codes(db_connection, mac, mac_table_name):
    # Save the mac dict to db
    save_dict(
        db_connection,
        table_name=mac_table_name,
        dictionary=mac,
        columns=("code", "alleles"),
    )


def save_serology_mappings(db_connection, sero_mapping):
    # Save the serology mapping to db
    save_dict(
        db_connection,
        table_name="serology_mapping",
        dictionary=sero_mapping,
        columns=("serology", "allele_list"),
    )


def load_v2_v3_mappings(db_connection):
    # TODO: Create mapping table using both the allele list history and
    #  deleted alleles as reference.
    # Temporary Example
    v2_to_v3_example = {
        "A*0104": "A*01:04:01:01N",
        "A*0105N": "A*01:04:01:01N",
        "A*0111": "A*01:11N",
        "A*01123": "A*01:123N",
        "A*0115": "A*01:15N",
        "A*0116": "A*01:16N",
        "A*01160": "A*01:160N",
        "A*01162": "A*01:162N",
        "A*01178": "A*01:178N",
        "A*01179": "A*01:179N",
        "DRB5*02ZB": "DRB5*02:UTV",
    }
    save_dict(
        db_connection,
        table_name="v2_mapping",
        dictionary=v2_to_v3_example,
        columns=("v2", "v3"),
    )


def load_serology_broad_split_mappings(db_connection):
    sero_mapping = load_dict(
        db_connection, "serology_broad_split_mapping", ("serology", "splits")
    )
    sero_splits = {k: v.split("/") for k, v in sero_mapping.items()}
    return sero_splits


def save_serology_broad_split_mappings(db_connection, sero_mapping):
    # Save the `splits` as a "/" delimited string to db
    sero_splits = {sero: "/".join(splits) for sero, splits in sero_mapping.items()}
    save_dict(
        db_connection,
        table_name="serology_broad_split_mapping",
        dictionary=sero_splits,
        columns=("serology", "splits"),
    )


def save_cwd2(db_connection: sqlite3.Connection, cwd2_map: dict):
    save_dict(
        db_connection,
        table_name="cwd2",
        dictionary=cwd2_map,
        columns=("allele", "locus"),
    )
