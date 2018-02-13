# -*- coding: utf-8 -*-

#
#    pyars pyARS.
#    Copyright (c) 2018 Be The Match operated by National Marrow Donor Program. All Rights Reserved.
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
import os
import urllib.request
import pandas as pd
from .base_model_ import Model
from .util import deserialize_model
from .util import pandas_explode
from typing import Dict


class ARD(Model):
    '''
    classdocs
    '''
    def __init__(self, dbversion: str='Latest'):
        """
        ARS -
        :param dbversion: The dbversion of this ReferenceData.
        :type dbversion: str
        """
        self.data_types = {
            'dbversion': str,
            'G': Dict,
            'lg': Dict,
            'lgx': Dict
        }
        self.attribute_map = {
            'dbversion': 'dbversion',
            'G': 'G',
            'lg': 'lg',
            'lgx': 'lgx'
        }

        self._dbversion = dbversion

        # List of expression characters
        expre_chars = ['N', 'Q', 'L', 'S']
        data_dir = os.path.dirname(__file__)
        ars_url = 'https://raw.githubusercontent.com/ANHIG/IMGTHLA/' \
                  + dbversion + '/wmda/hla_nom_g.txt'
        ars_file = data_dir + '/hla_nom_g.' + str(dbversion) + ".txt"
        
        # Downloading ARS file
        if not os.path.isfile(ars_file):
            urllib.request.urlretrieve(ars_url, ars_file)

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

    @classmethod
    def from_dict(cls, dikt) -> 'ARS':
        """
        Returns the dict as a model

        :param dikt: A dict.
        :type: dict
        :return: The ARS of this ARS.
        :rtype: ARS
        """
        return deserialize_model(dikt, cls)

    @property
    def dbversion(self) -> str:
        """
        Gets the dbversion of this ARS.

        :return: The dbversion of this ARS.
        :rtype: str
        """
        return self._dbversion

    @dbversion.setter
    def dbversion(self, dbversion: str):
        """
        Sets the dbversion of this ARS.

        :param dbversion: The dbversion of this ARS.
        :type dbversion: str
        """
        self._dbversion = dbversion

    @property
    def G(self) -> Dict:
        """
        Gets the G of this ARS.

        :return: The G of this ARS.
        :rtype: Dict
        """
        return self._G

    @property
    def lg(self) -> Dict:
        """
        Gets the lg of this ARS.

        :return: The lg of this ARS.
        :rtype: Dict
        """
        return self._lg

    @property
    def lgx(self) -> Dict:
        """
        Gets the lgx of this ARS.

        :return: The lgx of this ARS.
        :rtype: Dict
        """
        return self._lgx

    def redux(self, allele, ars_type):
        """
        Does ARS reduction with allele and ARS type

        :param allele: An HLA allele.
        :type: str
        :param ars_type: The ARS ars_type.
        :type: str
        :return: ARS reduced allele
        :rtype: str
        """
        if ars_type == "G" and allele in self.G:
            return self.G[allele]
        elif ars_type == "lg" and allele in self.lg:
            return self.lg[allele]
        elif ars_type == "lgx" and allele in self.lgx:
            return self.lgx[allele]
        else:
            return allele





