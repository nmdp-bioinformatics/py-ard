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
from collections import namedtuple
import functools
import sqlite3

import pandas as pd

from pyard import db
from pyard.broad_splits import broad_splits_dna_mapping
from pyard.broad_splits import broad_splits_ser_mapping

# GitHub URL where IMGT HLA files are downloaded.
from pyard.smart_sort import smart_sort_comparator

IMGT_HLA_URL = 'https://raw.githubusercontent.com/ANHIG/IMGTHLA/'

# List of expression characters
expression_chars = ['N', 'Q', 'L', 'S']

ars_mapping_tables = ['dup_g', 'dup_lg', 'dup_lgx', 'g_group', 'lg_group', 'lgx_group']
ARSMapping = namedtuple("ARSMapping", ars_mapping_tables)


def get_n_field_allele(allele: str, n: int) -> str:
    """
    Given an HLA allele of >= n field, return n field allele.
    Preserve the expression character if it exists

    :param allele: Original allele
    :param n: n number of fields to reduce to
    :return: trimmed to n fields of the original allele
    """
    last_char = allele[-1]
    fields = allele.split(':')
    if last_char in expression_chars and len(fields) > n:
        return ':'.join(fields[0:n]) + last_char
    else:
        return ':'.join(fields[0:n])


def get_3field_allele(a: str) -> str:
    return get_n_field_allele(a, 3)


def get_2field_allele(a: str) -> str:
    return get_n_field_allele(a, 2)


def generate_ars_mapping(db_connection: sqlite3.Connection, imgt_version):
    if db.tables_exists(db_connection, ars_mapping_tables):
        dup_g = db.load_dict(db_connection, table_name='dup_g', columns=('allele', 'g_group'))
        dup_lg = db.load_dict(db_connection, table_name='dup_lg', columns=('allele', 'lg_group'))
        dup_lgx = db.load_dict(db_connection, table_name='dup_lgx', columns=('allele', 'lgx_group'))
        g_group = db.load_dict(db_connection, table_name='g_group', columns=('allele', 'g'))
        lg_group = db.load_dict(db_connection, table_name='lg_group', columns=('allele', 'lg'))
        lgx_group = db.load_dict(db_connection, table_name='lgx_group', columns=('allele', 'lgx'))
        return ARSMapping(dup_g=dup_g, dup_lg=dup_lg, dup_lgx=dup_lgx,
                          g_group=g_group, lg_group=lg_group, lgx_group=lgx_group)

    ars_url = f'{IMGT_HLA_URL}{imgt_version}/wmda/hla_nom_g.txt'
    df = pd.read_csv(ars_url, skiprows=6, names=["Locus", "A", "G"], sep=";").dropna()

    df['A'] = df['A'].apply(lambda a: a.split('/'))
    df = df.explode('A')
    df['A'] = df['Locus'] + df['A']
    df['G'] = df['Locus'] + df['G']

    df['2d'] = df['A'].apply(get_2field_allele)
    df['3d'] = df['A'].apply(get_3field_allele)
    df['lg'] = df['G'].apply(lambda a: ":".join(a.split(":")[0:2]) + "g")
    df['lgx'] = df['G'].apply(lambda a: ":".join(a.split(":")[0:2]))

    # multiple Gs
    mg = df.drop_duplicates(['2d', 'G'])['2d'].value_counts()
    multiple_g_list = mg[mg > 1].reset_index()['index'].to_list()

    # Keep only the alleles that have more than 1 mapping
    dup_g = df[df['2d'].isin(multiple_g_list)][['G', '2d']] \
        .drop_duplicates() \
        .groupby('2d', as_index=True).agg("/".join) \
        .to_dict()['G']

    # multiple lg
    mlg = df.drop_duplicates(['2d', 'lg'])['2d'].value_counts()
    multiple_lg_list = mlg[mlg > 1].reset_index()['index'].to_list()

    # Keep only the alleles that have more than 1 mapping
    dup_lg = df[df['2d'].isin(multiple_lg_list)][['lg', '2d']] \
        .drop_duplicates() \
        .groupby('2d', as_index=True).agg("/".join) \
        .to_dict()['lg']

    # multiple lgx
    mlgx = df.drop_duplicates(['2d', 'lgx'])['2d'].value_counts()
    multiple_lgx_list = mlgx[mlgx > 1].reset_index()['index'].to_list()

    # Keep only the alleles that have more than 1 mapping
    dup_lgx = df[df['2d'].isin(multiple_lgx_list)][['lgx', '2d']] \
        .drop_duplicates() \
        .groupby('2d', as_index=True).agg("/".join) \
        .to_dict()['lgx']

    # Creating dictionaries with mac_code->ARS group mapping
    df_g = pd.concat([
        df[['2d', 'G']].rename(columns={'2d': 'A'}),
        df[['3d', 'G']].rename(columns={'3d': 'A'}),
        df[['A', 'G']]
    ], ignore_index=True)
    g_group = df_g.set_index('A')['G'].to_dict()

    df_lg = pd.concat([
        df[['2d', 'lg']].rename(columns={'2d': 'A'}),
        df[['3d', 'lg']].rename(columns={'3d': 'A'}),
        df[['A', 'lg']]
    ])
    lg_group = df_lg.set_index('A')['lg'].to_dict()

    df_lgx = pd.concat([
        df[['2d', 'lgx']].rename(columns={'2d': 'A'}),
        df[['3d', 'lgx']].rename(columns={'3d': 'A'}),
        df[['A', 'lgx']]
    ])
    lgx_group = df_lgx.set_index('A')['lgx'].to_dict()

    db.save_dict(db_connection, table_name='dup_g', dictionary=dup_g, columns=('allele', 'g_group'))
    db.save_dict(db_connection, table_name='dup_lg', dictionary=dup_lg, columns=('allele', 'lg_group'))
    db.save_dict(db_connection, table_name='dup_lgx', dictionary=dup_lgx, columns=('allele', 'lgx_group'))
    db.save_dict(db_connection, table_name='g_group', dictionary=g_group, columns=('allele', 'g'))
    db.save_dict(db_connection, table_name='lg_group', dictionary=lg_group, columns=('allele', 'lg'))
    db.save_dict(db_connection, table_name='lgx_group', dictionary=lgx_group, columns=('allele', 'lgx'))

    return ARSMapping(dup_g=dup_g, dup_lg=dup_lg, dup_lgx=dup_lgx,
                      g_group=g_group, lg_group=lg_group, lgx_group=lgx_group)


def generate_alleles_and_xx_codes(db_connection: sqlite3.Connection, imgt_version):
    """
    Checks to see if there's already an allele list file for the `imgt_version`
    in the `data_dir` directory. If not, will download the file and create
    a valid allele set and corresponding xx codes.

    The format of the AlleleList file has a 6-line header with a header
    on the 7th line
    ```
    # file: Allelelist.3290.txt
    # date: 2017-07-10
    # version: IPD-IMGT/HLA 3.29.0
    # origin: https://github.com/ANHIG/IMGTHLA/Allelelist.3290.txt
    # repository: https://raw.githubusercontent.com/ANHIG/IMGTHLA/Latest/Allelelist.3290.txt
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
    :return: None, updates self
    """

    if db.table_exists(db_connection, 'alleles'):
        valid_alleles = db.load_set(db_connection, 'alleles')
        xx_codes = db.load_dict(db_connection, 'xx_codes',
                                ('allele_1d', 'allele_list'))
        xx_codes = {k: v.split('/') for k, v in xx_codes.items()}
        return valid_alleles, xx_codes

    # Create a Pandas DataFrame from the mac_code list file
    # Skip the header (first 6 lines) and use only the Allele column
    if imgt_version == "Latest":
        allele_list_url = f'{IMGT_HLA_URL}Latest/Allelelist.txt'
    else:
        allele_list_url = f'{IMGT_HLA_URL}Latest/Allelelist.{imgt_version}.txt'
    allele_df = pd.read_csv(allele_list_url, header=6, usecols=['Allele'])

    # Create a set of valid alleles
    # All 2-field, 3-field and the original Alleles are considered valid alleles
    allele_df['2d'] = allele_df['Allele'].apply(get_2field_allele)
    allele_df['3d'] = allele_df['Allele'].apply(get_3field_allele)
    valid_alleles = set(allele_df['Allele']). \
        union(set(allele_df['2d'])). \
        union(set(allele_df['3d']))

    # Create xx_codes mapping from the unique alleles in 2-field column
    xx_df = pd.DataFrame(allele_df['2d'].unique(), columns=['Allele'])
    # Also create a first-field column
    xx_df['1d'] = xx_df['Allele'].apply(lambda x: x.split(":")[0])
    # xx_codes maps a first field name to its 2 field expansion
    xx_codes = xx_df.groupby(['1d']) \
        .apply(lambda x: list(x['Allele'])) \
        .to_dict()

    # Update xx codes with broads and splits
    for broad, splits in broad_splits_dna_mapping.items():
        for split in splits:
            if broad in xx_codes:
                xx_codes[broad].extend(xx_codes[split])
            else:
                xx_codes[broad] = xx_codes[split]

    # Save this version of the valid alleles
    db.save_set(db_connection, 'alleles', valid_alleles, 'allele')
    # Save this version of xx codes
    flat_xx_codes = {k: '/'.join(sorted(v, key=functools.cmp_to_key(smart_sort_comparator)))
                     for k, v in xx_codes.items()}
    db.save_dict(db_connection, 'xx_codes', flat_xx_codes,
                 ('allele_1d', 'allele_list'))

    return valid_alleles, xx_codes


def generate_mac_codes(db_connection: sqlite3.Connection, refresh_mac: bool):
    """
    MAC files come in 2 different versions:

    Martin: when they’re printed, the first is better for encoding and the
    second is better for decoding. The entire list was maintained both as an
    excel spreadsheet and also as a sybase database table. The excel was the
    one that was printed and distributed.

        **==> numer.v3.txt <==**

        Sorted by the length and the the values in the list
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

    :param db_connection: Database connection to the sqlite database
    :param refresh_mac: Refresh the database with newer MAC data ?
    :return: None
    """
    mac_table_name = 'mac_codes'
    if refresh_mac or not db.table_exists(db_connection, mac_table_name):
        # Load the MAC file to a DataFrame
        mac_url = 'https://hml.nmdp.org/mac/files/numer.v3.zip'
        df_mac = pd.read_csv(mac_url, sep='\t', compression='zip',
                             skiprows=3, names=['Code', 'Alleles'])
        # Create a dict from code to alleles
        mac = df_mac.set_index("Code")["Alleles"].to_dict()
        # Save the mac dict to db
        db.save_dict(db_connection, table_name=mac_table_name,
                     dictionary=mac, columns=('code', 'alleles'))


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
    locus, sero_number = locus_name.split('*')
    sero_locus = locus[:2]
    sero_name = sero_locus + sero_number
    return sero_name


def generate_serology_mapping(db_connection: sqlite3.Connection, imgt_version):
    if not db.table_exists(db_connection, 'serology_mapping'):
        # Load WMDA serology mapping data
        rel_dna_ser_url = f'{IMGT_HLA_URL}{imgt_version}/wmda/rel_dna_ser.txt'
        df_sero = pd.read_csv(rel_dna_ser_url, sep=';', skiprows=6,
                              names=['Locus', 'Allele', 'USA', 'PSA', 'ASA'],
                              index_col=False)

        # Remove 0 and ?
        df_sero = df_sero[(df_sero != '0') & (df_sero != '?')]
        df_sero['Allele'] = df_sero['Locus'] + df_sero['Allele']

        usa = df_sero[['Locus', 'Allele', 'USA']].dropna()
        usa['Sero'] = usa['Locus'] + usa['USA']

        psa = df_sero[['Locus', 'Allele', 'PSA']].dropna()
        psa['PSA'] = psa['PSA'].apply(lambda row: row.split('/'))
        psa = psa.explode('PSA')
        psa = psa[(psa != '0') & (psa != '?')].dropna()
        psa['Sero'] = psa['Locus'] + psa['PSA']

        asa = df_sero[['Locus', 'Allele', 'ASA']].dropna()
        asa['ASA'] = asa['ASA'].apply(lambda x: x.split('/'))
        asa = asa.explode('ASA')
        asa = asa[(asa != '0') & (asa != '?')].dropna()
        asa['Sero'] = asa['Locus'] + asa['ASA']

        sero_mapping_combined = pd.concat([usa[['Sero', 'Allele']],
                                           psa[['Sero', 'Allele']],
                                           asa[['Sero', 'Allele']]])

        # Map to only valid serological antigen name
        sero_mapping_combined['Sero'] = sero_mapping_combined['Sero']. \
            apply(to_serological_name)

        sero_mapping = sero_mapping_combined.groupby('Sero'). \
            apply(lambda x: '/'.join(sorted(x['Allele']))). \
            to_dict()

        # map alleles for split serology to their corresponding broad
        # Update xx codes with broads and splits
        for broad, splits in broad_splits_ser_mapping.items():
            for split in splits:
                try:
                    sero_mapping[broad] = '/'.join([sero_mapping[broad], sero_mapping[split]])

                except KeyError:
                    sero_mapping[broad] = sero_mapping[split]

        # re-sort allele lists into smartsort order
        for sero in sero_mapping.keys():
            sero_mapping[sero] = '/'.join(
                sorted(sero_mapping[sero].split('/'), key=functools.cmp_to_key(smart_sort_comparator)))

        # Save the serology mapping to db
        db.save_dict(db_connection, table_name='serology_mapping',
                     dictionary=sero_mapping, columns=('serology', 'allele_list'))


def generate_v2_to_v3_mapping(db_connection: sqlite3.Connection, imgt_version):
    if not db.table_exists(db_connection, 'v2_mapping'):
        # TODO: Create mapping table using both the allele list history and
        #  deleted alleles as reference.
        # Temporary Example
        v2_to_v3_example = {
            "A*0104": "A*01:04N",
            "A*0105N": "A*01:04N",
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
        db.save_dict(db_connection, table_name='v2_mapping',
                     dictionary=v2_to_v3_example, columns=('v2', 'v3'))
