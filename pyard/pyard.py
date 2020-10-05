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
import urllib.request
from functools import partial
from operator import is_not
from typing import Dict

import pandas as pd

from .broad_splits import broad_splits_mapping
from .smart_sort import smart_sort_comparator
from .util import all_macs
from .util import pandas_explode

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
        """
        ARD -
        :param dbversion:
        :type dbversion: str
        """
        self.mac = {}
        self._verbose = verbose
        self._dbversion = dbversion
        self._load_mac_file = load_mac_file
        self._remove_invalid = remove_invalid


        # TODO: add check for valid_alleles ARD type
        # TODO: add check for valid_alleles db version

        # Set data directory where all the downloaded files will go
        if data_dir is None:
            data_dir = os.path.dirname(__file__)
        else:
            pathlib.Path(data_dir).mkdir(exist_ok=True)

        ars_url = IMGT_HLA_URL + dbversion + '/wmda/hla_nom_g.txt'

        ars_file = data_dir + '/hla_nom_g.' + str(dbversion) + ".txt"
        mac_file = data_dir + "/mac.txt"
        mac_pickle = data_dir + "/mac.pickle"

        # Downloading ARS file
        if not os.path.isfile(ars_file):
            if verbose:
                logging.info("Downloading " + str(dbversion) + " ARD file")
            urllib.request.urlretrieve(ars_url, ars_file)

        # Downloading MAC file
        if load_mac_file:
            if not os.path.isfile(mac_pickle):
                if verbose:
                    logging.info("Downloading MAC file")
                self.mac = all_macs(mac_file, data_dir=data_dir)

                # Writing dict to pickle file
                with open(mac_pickle, 'wb') as handle:
                    pickle.dump(self.mac, handle, protocol=pickle.HIGHEST_PROTOCOL)
            else:
                if verbose:
                    logging.info("Loading MAC file")
                with open(mac_pickle, 'rb') as handle:
                    self.mac = pickle.load(handle)

        self.generate_alleles_and_xxcodes(dbversion, data_dir)

        # Loading ARS file into pandas
        # TODO: Make skip dynamic in case the files are not consistent
        df = pd.read_csv(ars_file, skiprows=6,
                         names=["Locus", "A", "G"], sep=";").dropna()

        df['Locus'] = df['Locus'].apply(lambda l: l.split("*")[0])
        df['A'] = df[['Locus', 'A']].apply(lambda row: [row['Locus'] + "*" + a
                                                        for a in
                                                        row['A'].split("/")
                                                        ],
                                           axis=1)
        df['G'] = df[['Locus', 'G']].apply(lambda row: "*".join([row['Locus'],
                                                                 row['G']]),
                                           axis=1)

        df = pandas_explode(df, 'A')

        df['2d'] = df['A'].apply(get_2field_allele)
        df['3d'] = df['A'].apply(get_3field_allele)

        df_values = df.drop_duplicates(['2d', 'G'])['2d'] \
            .value_counts().reset_index() \
            .sort_values(by='2d', ascending=False)
        multiple_Glist = df_values[df_values['2d'] > 1]['index'].tolist()
        self.dup_g = df[df['2d'].isin(multiple_Glist)][['G', '2d']] \
            .drop_duplicates() \
            .groupby('2d', as_index=True).agg("/".join) \
            .to_dict()['G']

        df['lg'] = df['G'].apply(lambda a:
                                 ":".join(a.split(":")[0:2]) + "g")

        df['lgx'] = df['G'].apply(lambda a:
                                  ":".join(a.split(":")[0:2]))

        # Creating dictionaries with allele->ARS group mapping
        self._G = pd.concat([df.drop(['A', 'lg', 'lgx', '3d'], axis=1)
                            .rename(index=str,
                                    columns={"2d": "A"})[['A', 'G']],
                             df.drop(['A', 'lg', 'lgx', '2d'], axis=1)
                            .rename(index=str,
                                    columns={"3d": "A"})[['A', 'G']],
                             df[['A', 'G']]],
                            ignore_index=True).set_index('A').to_dict()['G']

        self._lg = pd.concat([df.drop(['A', 'G', 'lgx', '3d'], axis=1)
                             .rename(index=str,
                                     columns={"2d": "A"})[['A', 'lg']],
                              df.drop(['A', 'G', 'lgx', '2d'], axis=1)
                             .rename(index=str,
                                     columns={"3d": "A"})[['A', 'lg']],
                              df[['A', 'lg']]],
                             ignore_index=True).set_index('A').to_dict()['lg']

        self._lgx = pd.concat([df.drop(['A', 'lg', 'G', '3d'], axis=1)
                              .rename(index=str,
                                      columns={"2d": "A"})[['A', 'lgx']],
                               df.drop(['A', 'lg', 'G', '2d'], axis=1)
                              .rename(index=str,
                                      columns={"3d": "A"})[['A', 'lgx']],
                               df[['A', 'lgx']]],
                              ignore_index=True).set_index('A').to_dict()['lgx']

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
            print("Loading from file.")
            with open(allele_file, 'rb') as load_file:
                self.valid_alleles = pickle.load(load_file)
            with open(xx_codes_file, 'rb') as load_file:
                self.xxcodes = pickle.load(load_file)
            return

        # Create a Pandas DataFrame from the allele list file
        # Skip the header (first 6 lines) and use only the Allele
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
                if allele in self.valid_alleles:
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
            loc, n = loc_name.split("*")
            return self.redux_gl(
                "/".join(sorted(self.xxcodes[loc_name], key=functools.cmp_to_key(smart_sort_comparator))), redux_type)

        if is_mac(glstring) and code in self.mac:
            if HLA_regex.search(glstring):
                hla, allele_name = glstring.split("-")
                loc_name, code = allele_name.split(":")
                alleles = self.get_alleles(code, loc_name)
                return self.redux_gl(
                    "/".join(sorted(["HLA-" + a for a in alleles], key=functools.cmp_to_key(smart_sort_comparator))),
                    redux_type)
            else:
                alleles = self.get_alleles(code, loc_name)
                return self.redux_gl("/".join(sorted(alleles, key=functools.cmp_to_key(smart_sort_comparator))),
                                     redux_type)
        return self.redux(glstring, redux_type)

    def get_alleles(self, code, loc_name):
        loc, n = loc_name.split("*")
        alleles = list(filter(lambda a: a in self.valid_alleles,
                              [loc_name + ":" + a if len(a) <= 3
                               else loc + "*" + a
                               for a in self.mac[code]['Alleles']]))
        return alleles

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
            return allele in self.valid_alleles
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
        loc, n = loc_name.split("*")
        if code in self.mac:
            alleles = list(filter(lambda a: a in self.valid_alleles,
                                  [loc_name + ":" + a if len(a) <= 3
                                   else loc + "*" + a
                                   for a in self.mac[code]['Alleles']]))
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
        Exapnds mac codes

        :param allele: An HLA allele.
        :type: str
        :return: List
        :rtype: List
        """
        loc_name, code = allele.split(":")
        loc, n = loc_name.split("*")
        if len(loc.split("-")) == 2:
            loc = loc.split("-")[1]
            loc_name = loc_name.split("-")[1]

        if code in self.mac:
            return list(filter(lambda a: a in self.valid_alleles,
                               [loc_name + ":" + a if len(a) <= 3
                                else loc + "*" + a
                                for a in self.mac[code]['Alleles']]))
        else:
            return ''
