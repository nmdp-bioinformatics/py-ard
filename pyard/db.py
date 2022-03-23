# -*- coding: utf-8 -*-
#
#    py-ard
#    Copyright (c) 2020 Be The Match operated by National Marrow Donor Program. All Rights Reserved.
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


def get_pyard_db_install_directory():
    return pathlib.Path.home() / ".pyard"


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
        data_dir = get_pyard_db_install_directory()

    db_filename = f'{data_dir}/pyard-{imgt_version}.sqlite3'

    if ro:
        # If in read-only mode, make sure the db file exists
        if not pathlib.Path(db_filename).exists():
            raise RuntimeError(f'Reference Database {db_filename}  not available.')

    # Create the data directory if it doesn't exist
    if not pathlib.Path(data_dir).exists():
        pathlib.Path(data_dir).mkdir(parents=True, exist_ok=True)

    if ro:
        # Open the database in read-only mode
        file_uri = f'file:{db_filename}?mode=ro'
    else:
        # Open the database in read-only mode
        file_uri = f'file:{db_filename}'

    return sqlite3.connect(file_uri, uri=True)


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
        alleles = result[0].split('/')
    else:
        alleles = []
    return alleles


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
        alleles = result[0].split('/')
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
    serology_query = "SELECT count(allele_list) from serology_mapping where serology = ?"
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


def save_dict(connection: sqlite3.Connection, table_name: str,
              dictionary: Dict[str, str], columns=Tuple[str, str]) -> bool:
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


def save_set(connection: sqlite3.Connection, table_name: str, rows: Set, column: str) -> bool:
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
    cursor.executemany(f"INSERT INTO {table_name} VALUES (?)", zip(rows, ))

    # commit transaction - writes to the db
    connection.commit()
    # close the cursor
    cursor.close()

    return True


def load_set(connection: sqlite3.Connection, table_name: str) -> Set:
    """
    Retrieve the first column of the table as a set

    :param connection: db connection of type sqlite.Connection
    :param table_name: name of the table to query
    :return: set containing values from the column
    """
    cursor = connection.cursor()
    select_all_query = f"SELECT * FROM {table_name}"
    cursor.execute(select_all_query)
    table_as_set = set(map(lambda t: t[0], cursor.fetchall()))
    cursor.close()
    return table_as_set


def load_dict(connection: sqlite3.Connection, table_name: str, columns: Tuple[str, str]) -> Dict[str, str]:
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
    query = f"SELECT allele FROM alleles WHERE allele LIKE ?"
    cursor = connection.execute(query, (f"{allele_name}%",))
    result = cursor.fetchall()
    # fetchall() returns a list of tuples of results
    # e.g. [('C*04:09N',)]
    # Get out the first value of the tuple from the result list
    alleles = set(map(lambda t: t[0], result))
    return alleles
