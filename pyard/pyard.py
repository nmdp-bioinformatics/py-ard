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
import functools
import logging
import os
import pathlib
import pickle
import re
from functools import partial
from operator import is_not
from typing import Dict

import pandas as pd

from .broad_splits import broad_splits_mapping
from .smart_sort import smart_sort_comparator

# The GitHub URL where IMGT HLA files are downloaded.
IMGT_HLA_URL = 'https://raw.githubusercontent.com/ANHIG/IMGTHLA/'


def is_mac(x):
    return True if re.search(r":\D+", x) else False


HLA_regex = re.compile("^HLA-")

# List of expression characters
expression_chars = ['N', 'Q', 'L', 'S']


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


class ARD(object):
    """ ARD reduction for HLA """

    def __init__(self, dbversion: str = 'Latest',
                 load_mac_file: bool = True,
                 verbose: bool = False,
                 remove_invalid: bool = True,
                 data_dir: str = None):

        self.mac = {}
        self._verbose = verbose
        self._dbversion = dbversion
        self._load_mac_file = load_mac_file
        self._remove_invalid = remove_invalid

        # Set data directory where all the downloaded files will go
        if data_dir is None:
            data_dir = pathlib.Path.home() / ".pyard"

        data_dir = f'{data_dir}/{dbversion}'
        pathlib.Path(data_dir).mkdir(parents=True, exist_ok=True)

        # Load MAC codes
        if load_mac_file:
            self.generate_mac_codes(data_dir)
        # Load Alleles and XX Codes
        self.generate_alleles_and_xxcodes(dbversion, data_dir)
        # Load ARS mappings
        self.generate_ars_mapping(data_dir)

    def generate_ars_mapping(self, data_dir):

        mapping_file = f'{data_dir}/ars_mapping.pickle'
        if os.path.isfile(mapping_file):
            with open(mapping_file, 'rb') as load_file:
                ars_mapping = pickle.load(load_file)
                self._G, self._lg, self._lgx, self.dup_g = ars_mapping
                return

        ars_url = f'{IMGT_HLA_URL}{self._dbversion}/wmda/hla_nom_g.txt'
        df = pd.read_csv(ars_url, skiprows=6, names=["Locus", "A", "G"], sep=";").dropna()

        df['A'] = df['A'].apply(lambda a: a.split('/'))
        df = df.explode('A')
        df['A'] = df['Locus'] + df['A']
        df['G'] = df['Locus'] + df['G']

        df['2d'] = df['A'].apply(get_2field_allele)
        df['3d'] = df['A'].apply(get_3field_allele)

        mg = df.drop_duplicates(['2d', 'G'])['2d'].value_counts()
        multiple_g_list = mg[mg > 1].reset_index()['index'].to_list()

        self.dup_g = df[df['2d'].isin(multiple_g_list)][['G', '2d']] \
            .drop_duplicates() \
            .groupby('2d', as_index=True).agg("/".join) \
            .to_dict()['G']

        df['lg'] = df['G'].apply(lambda a: ":".join(a.split(":")[0:2]) + "g")
        df['lgx'] = df['G'].apply(lambda a: ":".join(a.split(":")[0:2]))

        # Creating dictionaries with allele->ARS group mapping
        df_G = pd.concat([
            df[['2d', 'G']].rename(columns={'2d': 'A'}),
            df[['3d', 'G']].rename(columns={'3d': 'A'}),
            df[['A', 'G']]
        ], ignore_index=True)
        self._G = df_G.set_index('A')['G'].to_dict()

        df_lg = pd.concat([
            df[['2d', 'lg']].rename(columns={'2d': 'A'}),
            df[['3d', 'lg']].rename(columns={'3d': 'A'}),
            df[['A', 'lg']]
        ])
        self._lg = df_lg.set_index('A')['lg'].to_dict()

        df_lgx = pd.concat([
            df[['2d', 'lgx']].rename(columns={'2d': 'A'}),
            df[['3d', 'lgx']].rename(columns={'3d': 'A'}),
            df[['A', 'lgx']]
        ])
        self._lgx = df_lgx.set_index('A')['lgx'].to_dict()

        ars_mapping = (self._G, self._lg, self._lgx, self.dup_g)
        with open(mapping_file, 'wb') as save_file:
            pickle.dump(ars_mapping, save_file, protocol=pickle.HIGHEST_PROTOCOL)

    def generate_mac_codes(self, data_dir):
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

        :param data_dir:
        :return:
        """

        mac_pickle = f'{data_dir}/mac.pickle'

        if not os.path.isfile(mac_pickle):
            if self.verbose:
                logging.info("Downloading MAC file")
            # Load the MAC file to a DataFrame
            mac_url = 'https://hml.nmdp.org/mac/files/numer.v3.zip'
            df_mac = pd.read_csv(mac_url, sep='\t', compression='zip', skiprows=3, names=['Code', 'Alleles'])
            self.mac = df_mac.set_index("Code")["Alleles"].to_dict()

            # Writing dict to pickle file
            with open(mac_pickle, 'wb') as save_file:
                pickle.dump(self.mac, save_file, protocol=pickle.HIGHEST_PROTOCOL)
        else:
            if self.verbose:
                logging.info("Loading MAC file")
            with open(mac_pickle, 'rb') as load_file:
                self.mac = pickle.load(load_file)

    def generate_alleles_and_xxcodes(self, dbversion: str, data_dir: str) -> None:
        """
        Checks to see if there's already an allele list file for the `dbversion`
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

        :param dbversion: IMGT database version
        :param data_dir: Data Directory to save the resulting files
        :return: None, updates self
        """

        allele_file = f'{data_dir}/AlleleList.{dbversion}.pickle'
        xx_codes_file = f'{data_dir}/XX_Codes.{dbversion}.pickle'

        # If the pickled files already exist for the particular db version
        # then reload the files without re-downloading
        if pathlib.Path(allele_file).exists() and \
                pathlib.Path(xx_codes_file).exists():
            with open(allele_file, 'rb') as load_file:
                self.valid_alleles = pickle.load(load_file)
            with open(xx_codes_file, 'rb') as load_file:
                self.xxcodes = pickle.load(load_file)
            return

        # Create a Pandas DataFrame from the allele list file
        # Skip the header (first 6 lines) and use only the Allele
        if dbversion == "Latest":
            allele_list_url = f'{IMGT_HLA_URL}Latest/Allelelist.txt'
        else:
            allele_list_url = f'{IMGT_HLA_URL}Latest/Allelelist.{dbversion}.txt'
        allele_df = pd.read_csv(allele_list_url, header=6, usecols=['Allele'])

        # Create a set of valid alleles
        # All 2-field, 3-field and the original Alleles are considered valid alleles
        allele_df['2d'] = allele_df['Allele'].apply(get_2field_allele)
        allele_df['3d'] = allele_df['Allele'].apply(get_3field_allele)
        self.valid_alleles = set(allele_df['Allele']). \
            union(set(allele_df['2d'])). \
            union(set(allele_df['3d']))

        # Create xxcodes mapping from the unique alleles in 2-field column
        xx_df = pd.DataFrame(allele_df['2d'].unique(), columns=['Allele'])
        # Also create a first-field column
        xx_df['1d'] = xx_df['Allele'].apply(lambda x: x.split(":")[0])
        # xxcodes maps a first field name to its 2 field expansion
        self.xxcodes = xx_df.groupby(['1d']) \
            .apply(lambda x: list(x['Allele'])) \
            .to_dict()

        # Update xx codes with broads and splits
        for broad, splits in broad_splits_mapping.items():
            for split in splits:
                if broad in self.xxcodes:
                    self.xxcodes[broad].extend(self.xxcodes[split])
                else:
                    self.xxcodes[broad] = self.xxcodes[split]

        # Save this version of the valid alleles and xx codes
        # Save alleles to pickle file
        with open(allele_file, 'wb') as save_file:
            pickle.dump(self.valid_alleles, save_file, protocol=pickle.HIGHEST_PROTOCOL)
        # Save xx codes to pickle file
        with open(xx_codes_file, 'wb') as save_file:
            pickle.dump(self.xxcodes, save_file, protocol=pickle.HIGHEST_PROTOCOL)

    @property
    def dbversion(self) -> str:
        """
        Gets the dbversion of this ARS.

        :return: The dbversion of this ARS.
        :rtype: str
        """
        return self._dbversion

    @property
    def verbose(self) -> bool:
        """
        Gets the verbose of this ARS.

        :return: The verbose of this ARS.
        :rtype: bool
        """
        return self._verbose

    @property
    def load_mac_file(self) -> bool:
        """
        Gets the load_mac_file of this ARS.

        :return: The load_mac_file of this ARS.
        :rtype: bool
        """
        return self._load_mac_file

    @property
    def remove_invalid(self) -> bool:
        """
        Gets the remove_invalid of this ARS.

        :return: The remove_invalid of this ARS.
        :rtype: bool
        """
        return self._remove_invalid

    @property
    def G(self):
        """
        Gets the G of this ARS.

        :return: The G of this ARS.
        :rtype: Dict
        """
        return self._G

    @property
    def lg(self):
        """
        Gets the lg of this ARS.

        :return: The lg of this ARS.
        :rtype: Dict
        """
        return self._lg

    @property
    def lgx(self):
        """
        Gets the lgx of this ARS.

        :return: The lgx of this ARS.
        :rtype: Dict
        """
        return self._lgx

    @functools.lru_cache(maxsize=1000)
    def redux(self, allele: str, ars_type: str) -> str:
        """
        Does ARS reduction with allele and ARS type

        :param allele: An HLA allele.
        :type: str
        :param ars_type: The ARS ars_type.
        :type: str
        :return: ARS reduced allele
        :rtype: str
        """

        # deal with leading 'HLA-'
        if HLA_regex.search(allele):
            hla, allele_name = allele.split("-")
            redux_allele = self.redux(allele_name, ars_type)
            if redux_allele:
                return "HLA-" + redux_allele
            else:
                return redux_allele

        # Alleles ending with P or G are valid_alleles
        if allele.endswith(('P', 'G')):
            allele = allele[:-1]

        if ars_type == "G" and allele in self._G:
            if allele in self.dup_g:
                return self.dup_g[allele]
            else:
                return self.G[allele]
        elif ars_type == "lg":
            if allele in self._lg:
                return self.lg[allele]
            else:
                # for 'lg' when allele is not in G group,
                # return allele with only first 2 field
                return ':'.join(allele.split(':')[0:2]) + 'g'
        elif ars_type == "lgx":
            if allele in self._lgx:
                return self.lgx[allele]
            else:
                # for 'lgx' when allele is not in G group,
                # return allele with only first 2 field
                return ':'.join(allele.split(':')[0:2])
        else:
            if self.remove_invalid:
                if self._is_valid_allele(allele):
                    return allele
                else:
                    return ''
            else:
                return allele

    @functools.lru_cache(maxsize=1000)
    def redux_gl(self, glstring: str, redux_type: str) -> str:
        """
        Does ARS reduction with gl string and ARS type

        :param glstring: A GL String
        :type: str
        :param redux_type: The ARS ars_type.
        :type: str
        :return: ARS reduced allele
        :rtype: str
        """

        if not self.isvalid_gl(glstring):
            return ""

        if re.search(r"\^", glstring):
            return "^".join(sorted(set([self.redux_gl(a, redux_type) for a in glstring.split("^")]),
                                   key=functools.cmp_to_key(smart_sort_comparator)))

        if re.search(r"\|", glstring):
            return "|".join(sorted(set([self.redux_gl(a, redux_type) for a in glstring.split("|")]),
                                   key=functools.cmp_to_key(smart_sort_comparator)))

        if re.search(r"\+", glstring):
            return "+".join(sorted([self.redux_gl(a, redux_type) for a in glstring.split("+")],
                                   key=functools.cmp_to_key(smart_sort_comparator)))

        if re.search("~", glstring):
            return "~".join([self.redux_gl(a, redux_type) for a in glstring.split("~")])

        if re.search("/", glstring):
            return "/".join(sorted(set([self.redux_gl(a, redux_type) for a in glstring.split("/")]),
                                   key=functools.cmp_to_key(smart_sort_comparator)))

        loc_allele = glstring.split(":")
        loc_name, code = loc_allele[0], loc_allele[1]

        # handle XX codes
        # test that they are valid_alleles
        if (is_mac(glstring) and glstring.split(":")[1] == "XX") and loc_name in self.xxcodes:
            return self.redux_gl(
                "/".join(sorted(self.xxcodes[loc_name], key=functools.cmp_to_key(smart_sort_comparator))), redux_type)

        if is_mac(glstring) and code in self.mac:
            if HLA_regex.search(glstring):
                hla, allele_name = glstring.split("-")
                loc_name, code = allele_name.split(":")
                alleles = self._get_alleles(code, loc_name)
                return self.redux_gl(
                    "/".join(sorted(["HLA-" + a for a in alleles], key=functools.cmp_to_key(smart_sort_comparator))),
                    redux_type)
            else:
                alleles = self._get_alleles(code, loc_name)
                return self.redux_gl("/".join(sorted(alleles, key=functools.cmp_to_key(smart_sort_comparator))),
                                     redux_type)
        return self.redux(glstring, redux_type)

    def _is_valid_allele(self, allele):
        return allele in self.valid_alleles

    def _get_alleles(self, code, loc_name):
        return filter(self._is_valid_allele, [f'{loc_name}:{a}' for a in self.mac[code].split('/')])

    def isvalid(self, allele: str) -> bool:
        """
        Determines validity of an allele

        :param allele: An HLA allele.
        :type: str
        :return: allele or empty
        :rtype: bool
        """
        if not is_mac(allele):
            # PERFORMANCE: use hash instead of allele in "list"
            # return allele in self.valid_alleles
            # Alleles ending with P or G are valid_alleles
            if allele.endswith(('P', 'G')):
                # remove the last character
                allele = allele[:-1]
            # validate allele without the 'HLA-' prefix
            if HLA_regex.search(allele):
                # remove 'HLA-' prefix
                allele = allele[4:]
            return self._is_valid_allele(allele)
        return True

    def isvalid_gl(self, glstring: str) -> bool:
        """
        Determines validity of glstring

        :param glstring
        :type: str
        :return: result
        :rtype: bool
        """

        if re.search(r"\^", glstring):
            return all(map(self.isvalid_gl, glstring.split("^")))
        if re.search(r"\|", glstring):
            return all(map(self.isvalid_gl, glstring.split("|")))
        if re.search(r"\+", glstring):
            return all(map(self.isvalid_gl, glstring.split("+")))
        if re.search("~", glstring):
            return all(map(self.isvalid_gl, glstring.split("~")))
        if re.search("/", glstring):
            return all(map(self.isvalid_gl, glstring.split("/")))

        # what falls through here is an allele
        return self.isvalid(glstring)

    def mac_toG(self, allele: str) -> str:
        """
        Does ARS reduction with allele and ARS type

        :param allele: An HLA allele.
        :type: str
        :return: ARS reduced allele
        :rtype: str
        """
        loc_name, code = allele.split(":")
        if code in self.mac:
            alleles = self._get_alleles(code, loc_name)
            group = list(filter(partial(is_not, None),
                                set([self.toG(allele=a)
                                     for a in alleles])))
            if "X" in group:
                return ''
            else:
                return "/".join(group)

        else:
            return ''

    def toG(self, allele: str) -> str:
        """
        Does ARS reduction to the G group level

        :param allele: An HLA allele.
        :type: str
        :return: ARS G reduced allele
        :rtype: str
        """
        if allele in self.G:
            if allele in self.dup_g:
                return self.dup_g[allele]
            else:
                return self.G[allele]
        else:
            return "X"

    def expand_mac(self, allele: str):
        """
        Expands mac codes

        :param allele: An HLA allele.
        :type: str
        :return: List
        :rtype: List
        """
        loc_name, code = allele.split(":")
        loc, n = loc_name.split("*")
        if len(loc.split("-")) == 2:
            loc_name = loc_name.split("-")[1]

        if code in self.mac:
            return self._get_alleles(code, loc_name)
        else:
            return ''
