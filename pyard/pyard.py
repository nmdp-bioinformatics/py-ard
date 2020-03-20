# -*- coding: utf-8 -*-

#
#    pyard
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
import re
import os
import pickle
import urllib.request
import pandas as pd
import functools
from .smart_sort import smart_sort_comparator
from .util import pandas_explode
from .util import all_macs
from operator import is_not
import functools
from functools import partial
from typing import Dict
import logging

ismac = lambda x: True if re.search(":\D+", x) else False


# a module shouldn't decide the logging config; thats up to the calling programo

#logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', datefmt='%m/%d/%Y %I:%M:%S %p', level=logging.INFO)

import string

alpha = list(string.ascii_lowercase) + list(string.ascii_uppercase)


# Have GFE ARD be in pyARD because requiring
# pygfe would be a big download.
def getvalue(a):
    return int("".join(list(a)[0:len(list(a))-1])) if list(a)[len(list(a))-1] in alpha else int(a)


def loci_sort(a, b):
    la = a.split(":")
    lb = b.split(":")
    a1, a2 = int(la[0].split("*")[1]), getvalue(la[1])
    b1, b2 = int(lb[0].split("*")[1]), getvalue(lb[1])
    if a1 > b1:
        return 1
    elif a1 == b1:
        if a2 > b2:
            return 1
        elif a2 == b2:
            return 0
        else:
            return -1
    else:
        return -1


class ARD(object):
    '''
    classdocs
    '''
    def __init__(self, dbversion: str='Latest',
                 download_mac: bool=True,
                 verbose: bool=False,
                 remove_invalid: bool=True):
        """
        ARD -
        :param dbversion:
        :type dbversion: str
        """
        self.data_types = {
            'dbversion': str,
            'verbose': bool,
            'download_mac': bool,
            'remove_invalid': bool,
            'G': Dict,
            'lg': Dict,
            'lgx': Dict
        }
        self.attribute_map = {
            'dbversion': 'dbversion',
            'G': 'G',
            'lg': 'lg',
            'lgx': 'lgx',
            'verbose': 'verbose',
            'download_mac': 'download_mac',
            'remove_invalid': 'remove_invalid'
        }

        self.mac = {}
        self._verbose = verbose
        self._dbversion = dbversion
        self._download_mac = download_mac
        self._remove_invalid = remove_invalid

        self.HLA_regex = re.compile("^HLA-")

        # TODO: add check for valid ARD type
        # TODO: add check for valid db version

        # List of expression characters
        expre_chars = ['N', 'Q', 'L', 'S']
        data_dir = os.path.dirname(__file__)
        ars_url = 'https://raw.githubusercontent.com/ANHIG/IMGTHLA/' \
                  + dbversion + '/wmda/hla_nom_g.txt'
        ars_file = data_dir + '/hla_nom_g.' + str(dbversion) + ".txt"
        allele_file = data_dir + '/AlleleList.' + str(dbversion) + ".txt"
        mac_file = data_dir + "/mac.txt"
        mac_pickle = data_dir + "/mac.pickle"
        broad_file = data_dir + "/dna_relshp.csv"

        allele_url = "https://raw.githubusercontent.com/ANHIG/IMGTHLA/" \
                     + dbversion + "/Allelelist.txt"

        # Downloading ARS file
        if not os.path.isfile(ars_file):
            if verbose:
                logging.info("Downloading " + str(dbversion) + " ARD file")
            urllib.request.urlretrieve(ars_url, ars_file)

        # Downloading allele list file
        if not os.path.isfile(allele_file):
            if verbose:
                logging.info("Downloading " + str(dbversion) + " allele list")
            urllib.request.urlretrieve(allele_url, allele_file)

        # Downloading MAC file
        if download_mac:
            if not os.path.isfile(mac_pickle):
                if verbose:
                    logging.info("Downloading MAC file")
                self.mac = all_macs(mac_file)

                # Writing dict to pickle file
                with open(mac_pickle, 'wb') as handle:
                    pickle.dump(self.mac, handle, protocol=pickle.HIGHEST_PROTOCOL)
            else:
                if verbose:
                    logging.info("Loading MAC file")
                with open(mac_pickle, 'rb') as handle:
                    self.mac = pickle.load(handle)

        with open(allele_file) as f:
            first_line = f.readline()
            f.close()

        sep = "," if re.search("#", first_line) else " "
        allele_data = []
        with open(allele_file, 'r') as f:
            for line in f:
                line = line.rstrip()
                if not re.search("#", line):
                    allele_data.append(line.split(sep))
            f.close()

        allele_df = pd.DataFrame(allele_data)
        if allele_df[:1].values.tolist()[0][1] == 'Allele':
            allele_df.columns = allele_df[:1].values.tolist()[0]
            idname = allele_df[:1].values.tolist()[0][0]
            allele_df.drop(0, inplace=True)
            allele_df = allele_df.rename(index=str, columns={idname: "ID"})
        else:
            allele_df.columns = ["ID", "Allele"]

        allele_df['2d'] = allele_df['Allele'].apply(lambda a:
                                     ":".join(a.split(":")[0:2]) +
                                     list(a)[-1] if list(a)[-1]
                                     in expre_chars and
                                     len(a.split(":")) > 2
                                     else ":".join(a.split(":")[0:2]))

        dfxx = pd.DataFrame(pd.Series(allele_df['2d'].unique().tolist()),
                                      columns=['Allele'])
        dfxx['1d'] = dfxx['Allele'].apply(lambda x: x.split(":")[0])
    
        # xxcodes maps a first field name to its expansion
        self.xxcodes = dfxx.groupby(['1d'])\
                           .apply(lambda x: list(x['Allele']))\
                           .to_dict()

        # defined broad XX codes
        dfbroad = pd.read_csv(broad_file, skiprows=1, dtype=str,
                         names=["Locus", "Broad", "Fam"], sep=",").dropna()

        dictbroad = dfbroad.groupby(['Locus','Broad']).apply(lambda x: list(x['Fam'])).to_dict()

        for (locus,broad) in dictbroad.keys():
            locusbroad="*".join([locus,broad])  
            for split in dictbroad[(locus,broad)]:
                locussplit="*".join([locus,split])
                if locusbroad in self.xxcodes:
                    self.xxcodes[locusbroad].extend(self.xxcodes[locussplit])
                else:
                    self.xxcodes[locusbroad] = self.xxcodes[locussplit]

        allele_df['3d'] = allele_df['Allele'].apply(lambda a:
                                 ":".join(a.split(":")[0:3]) +
                                 list(a)[-1] if list(a)[-1]
                                 in expre_chars and
                                 len(a.split(":")) > 3
                                 else ":".join(a.split(":")[0:3]))

        # all alleles are valid and also shortening to 3 and 2 fields
        self.valid = list(set(allele_df['Allele'].tolist()
                              + allele_df['2d'].tolist()
                              + allele_df['3d'].tolist()))
        # use a dict
        self.valid_dict={}
        for i in self.valid:
            self.valid_dict[i]=True

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

        df['2d'] = df['A'].apply(lambda a:
                                 ":".join(a.split(":")[0:2]) +
                                 list(a)[-1] if list(a)[-1]
                                 in expre_chars and
                                 len(a.split(":")) > 2
                                 else ":".join(a.split(":")[0:2]))

        df['3d'] = df['A'].apply(lambda a:
                                 ":".join(a.split(":")[0:3]) +
                                 list(a)[-1] if list(a)[-1]
                                 in expre_chars and
                                 len(a.split(":")) > 3
                                 else ":".join(a.split(":")[0:3]))

        df_values = df.drop_duplicates(['2d', 'G'])['2d']\
                      .value_counts().reset_index()\
                      .sort_values(by='2d', ascending=False)
        multiple_Glist = df_values[df_values['2d'] > 1]['index'].tolist()
        self.dup_g = df[df['2d'].isin(multiple_Glist)][['G', '2d']]\
                                .drop_duplicates()\
                                .groupby('2d', as_index=True).agg("/".join)\
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
    def download_mac(self) -> bool:
        """
        Gets the download_mac of this ARS.

        :return: The download_mac of this ARS.
        :rtype: bool
        """
        return self._download_mac

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

    @functools.lru_cache(maxsize=None)
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

        # PERFORMANCE: precompiled regex
        # dealing with leading HLA-

        if self.HLA_regex.search(allele):
            hla, allele_name = allele.split("-")
            return "-".join(["HLA", self.redux(allele_name, ars_type)])

        if ars_type == "G" and allele in self._G:
            if allele in self.dup_g:
                return self.dup_g[allele]
            else:
                return self.G[allele]
        elif ars_type == "lg" and allele in self._lg:
            return self.lg[allele]
        elif ars_type == "lgx" and allele in self._lgx:
            return self.lgx[allele]
        else:
            if self.remove_invalid:
                if allele in self.valid:
                    return allele
                else:
                    return
            else:
                return allele

    @functools.lru_cache(maxsize=None)
    def redux_gl(self, glstring: str, redux_type: str) -> str:
        """
        Does ARS reduction with allele and ARS type

        :param allele: An HLA allele.
        :type: str
        :param ars_type: The ARS ars_type.
        :type: str
        :return: ARS reduced allele
        :rtype: str
        """
        
        if not self.isvalid_gl(glstring):
            return ""

        if re.search("\^", glstring):
            return "^".join(sorted(set([self.redux_gl(a, redux_type) for a in glstring.split("^")]), key=functools.cmp_to_key(smart_sort_comparator)))

        if re.search("\|", glstring):
            return "|".join(sorted(set([self.redux_gl(a, redux_type) for a in glstring.split("|")]), key=functools.cmp_to_key(smart_sort_comparator)))

        if re.search("\+", glstring):
            return "+".join(sorted([self.redux_gl(a, redux_type) for a in glstring.split("+")], key=functools.cmp_to_key(smart_sort_comparator)))

        if re.search("\~", glstring):
            return "~".join([self.redux_gl(a, redux_type) for a in glstring.split("~")])

        if re.search("/", glstring):
            return "/".join(sorted(set([self.redux_gl(a, redux_type) for a in glstring.split("/")]), key=functools.cmp_to_key(smart_sort_comparator)))

        loc_allele = glstring.split(":")
        loc_name, code = loc_allele[0], loc_allele[1]
       
        # handle XX codes
        # test that they are valid
        if(ismac(glstring) and glstring.split(":")[1] == "XX") and loc_name in self.xxcodes:
            loc, n = loc_name.split("*")
            return self.redux_gl("/".join(sorted(self.xxcodes[loc_name], key=functools.cmp_to_key(smart_sort_comparator))), redux_type)

        if ismac(glstring) and code in self.mac:
            if re.search("HLA-", glstring):
                hla, allele_name = glstring.split("-")
                loc_name, code = allele_name.split(":")
                loc, n = loc_name.split("*")
                alleles = list(filter(lambda a: a in self.valid,
                                      [loc_name + ":" + a if len(a) <= 3
                                       else loc + "*" + a
                                       for a in self.mac[code]['Alleles']]))
                return self.redux_gl("/".join(sorted(["HLA-" + a for a in alleles], key=functools.cmp_to_key(smart_sort_comparator))), redux_type)
            else:
                loc, n = loc_name.split("*")
                alleles = list(filter(lambda a: a in self.valid,
                                      [loc_name + ":" + a if len(a) <= 3
                                       else loc + "*" + a
                                       for a in self.mac[code]['Alleles']]))
                return self.redux_gl("/".join(sorted(alleles, key=functools.cmp_to_key(smart_sort_comparator))), redux_type)
        return self.redux(glstring, redux_type)

    def isvalid(self, allele: str) -> bool:
        """
        Determines validity of an allele

        :param allele: An HLA allele.
        :type: str
        :return: allele or empty
        :rtype: bool
        """
        if not ismac(allele):
            # PERFORMANCE: use hash instead of allele in "list"
            # return allele in self.valid
            return self.valid_dict.get(allele, False)
        return True

    def isvalid_gl(self, glstring: str) -> bool:
        """
        Determine validity of glstring

        :param glstring
        :type: str
        :return: result
        :rtype: bool
        """
        
        if re.search("\^", glstring):
            return(all(list(map(self.isvalid_gl,glstring.split("^")))))
        if re.search("\|", glstring):
            return(all(list(map(self.isvalid_gl,glstring.split("|")))))
        if re.search("\+", glstring):
            return(all(list(map(self.isvalid_gl,glstring.split("+")))))
        if re.search("\~", glstring):
            return(all(list(map(self.isvalid_gl,glstring.split("~")))))
        if re.search("/", glstring):
            return(all(list(map(self.isvalid_gl,glstring.split("/")))))

        # what falls through here is an allele
        return(self.isvalid(glstring))

    def mac_toG(self, allele: str) -> str:
        """
        Does ARS reduction with allele and ARS type

        :param allele: An HLA allele.
        :type: str
        :param ars_type: The ARS ars_type.
        :type: str
        :return: ARS reduced allele
        :rtype: str
        """
        loc_name, code = allele.split(":")
        loc, n = loc_name.split("*")
        if code in self.mac:
            alleles = list(filter(lambda a: a in self.valid,
                                  [loc_name + ":" + a if len(a) <= 3
                                   else loc + "*" + a
                                   for a in self.mac[code]['Alleles']]))
            group = list(filter(partial(is_not, None),
                         set([self.toG(allele=a)
                              for a in alleles])))
            if "X" in group:
                return None
            else:
                return "/".join(group)

        else:
            return None

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
            return list(filter(lambda a: a in self.valid,
                               [loc_name + ":" + a if len(a) <= 3
                                else loc + "*" + a
                                for a in self.mac[code]['Alleles']]))
        else:
            return ''

