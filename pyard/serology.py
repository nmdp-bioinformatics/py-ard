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
import re

from pyard.constants import HLA_regex

#
# HLA Antigens
# List of all recognised serological collected from:
# https://hla.alleles.org/antigens/recognised_serology.html
#


# -#
# Broad, Splits and Associated Antigens
# http://hla.alleles.org/antigens/broads_splits.html
#
#
# Mapping Generated from `dna_relshp.csv` file
#
broad_splits_dna_mapping = {
    "A*09": ["A*23", "A*24"],
    "A*10": ["A*25", "A*26", "A*34", "A*66"],
    "A*19": ["A*29", "A*30", "A*31", "A*32", "A*33", "A*74"],
    "A*28": ["A*68", "A*69"],
    "B*05": ["B*51", "B*52"],
    "B*12": ["B*44", "B*45"],
    "B*16": ["B*38", "B*39"],
    "B*17": ["B*57", "B*58"],
    "B*21": ["B*49", "B*50"],
    "B*22": ["B*54", "B*55", "B*56"],
    "C*10": ["C*03", "C*04"],
    "DQB1*01": ["DQB1*05", "DQB1*06"],
    "DRB1*02": ["DRB1*15", "DRB1*16"],
    "DRB1*06": ["DRB1*13", "DRB1*14"],
}

serology_xx_exception_mapping = {
    # Locus B
    # Broad B40
    "B60": "B*40:XX",
    "B61": "B*40:XX",
    # Broad B14
    "B64": "B*14:XX",
    "B65": "B*14:XX",
    # Broad B15
    "B62": "B*15:XX",
    "B63": "B*15:XX",
    "B70": "B*15:XX",
    "B75": "B*15:XX",
    "B76": "B*15:XX",
    "B77": "B*15:XX",
    # Broad B70
    "B71": "B*15:XX",
    "B72": "B*15:XX",
    "DR17": "DRB1*03:XX",
    "DR18": "DRB1*03:XX",
    # Locus DQB1
    # Broad DQ3
    "DQ7": "DQB1*03:XX",
    "DQ8": "DQB1*03:XX",
    "DQ9": "DQB1*03:XX",
}

sero_antigen_regex = re.compile(r"(\D+)(\d+)")


class SerologyMapping:
    valid_serology_map = {
        "A": [
            "A1",
            "A2",
            "A203",
            "A210",
            "A3",
            "A9",
            "A10",
            "A11",
            "A19",
            "A23",
            "A24",
            "A2403",
            "A25",
            "A26",
            "A28",
            "A29",
            "A30",
            "A31",
            "A32",
            "A33",
            "A34",
            "A36",
            "A43",
            "A66",
            "A68",
            "A69",
            "A74",
            "A80",
        ],
        "B": [
            "B5",
            "B7",
            "B703",
            "B8",
            "B12",
            "B13",
            "B14",
            "B15",
            "B16",
            "B17",
            "B18",
            "B21",
            "B22",
            "B27",
            "B2708",
            "B35",
            "B37",
            "B38",
            "B39",
            "B3901",
            "B3902",
            "B40",
            "B4005",
            "B41",
            "B42",
            "B44",
            "B45",
            "B46",
            "B47",
            "B48",
            "B49",
            "B50",
            "B51",
            "B5102",
            "B5103",
            "B52",
            "B53",
            "B54",
            "B55",
            "B56",
            "B57",
            "B58",
            "B59",
            "B60",
            "B61",
            "B62",
            "B63",
            "B64",
            "B65",
            "B67",
            "B70",
            "B71",
            "B72",
            "B73",
            "B75",
            "B76",
            "B77",
            "B78",
            "B81",
            "B82",
            "Bw4",
            "Bw6",
        ],
        "C": ["Cw1", "Cw2", "Cw3", "Cw4", "Cw5", "Cw6", "Cw7", "Cw8", "Cw9", "Cw10"],
        "D": [
            "Dw1",
            "Dw2",
            "Dw3",
            "Dw4",
            "Dw5",
            "Dw6",
            "Dw7",
            "Dw8",
            "Dw9",
            "Dw10",
            "Dw11",
            "Dw12",
            "Dw13",
            "Dw14",
            "Dw15",
            "Dw16",
            "Dw17",
            "Dw18",
            "Dw19",
            "Dw20",
            "Dw21",
            "Dw22",
            "Dw23",
            "Dw24",
            "Dw25",
            "Dw26",
        ],
        "DRB1": [
            "DR1",
            "DR103",
            "DR2",
            "DR3",
            "DR4",
            "DR5",
            "DR6",
            "DR7",
            "DR8",
            "DR9",
            "DR10",
            "DR11",
            "DR12",
            "DR13",
            "DR14",
            "DR1403",
            "DR1404",
            "DR15",
            "DR16",
            "DR17",
            "DR18",
            "DR51",
            "DR52",
            "DR53",
        ],
        "DQB1": ["DQ1", "DQ2", "DQ3", "DQ4", "DQ5", "DQ6", "DQ7", "DQ8", "DQ9"],
        "DPB1": ["DPw1", "DPw2", "DPw3", "DPw4", "DPw5", "DPw6"],
    }

    def __init__(self, broad_splits_mapping, associated_mapping):
        self.broad_splits_map = broad_splits_mapping
        self.serology_associated_map = associated_mapping

    def find_splits(self, allele: str) -> tuple:
        if HLA_regex.search(allele):
            prefix = True
            allele_name = allele.split("-")[1]
        else:
            prefix = False
            allele_name = allele

        if "*" in allele_name:
            mapping = broad_splits_dna_mapping
        else:
            mapping = self.broad_splits_map

        if allele_name in mapping:
            return self._get_mapping(allele_name, mapping, prefix)

        for broad in mapping:
            if allele_name in mapping[broad]:
                return self._get_mapping(broad, mapping, prefix)

    def find_associated_antigen(self, serology):
        return self.serology_associated_map.get(serology, serology)

    def get_xx_mappings(self):
        all_xx_mappings = {}
        for locus, serologies in SerologyMapping.valid_serology_map.items():
            xx_mapping = {
                serology: self._map_serology_to_xx(locus, serology)
                for serology in serologies
            }
            all_xx_mappings.update(xx_mapping)
        return all_xx_mappings

    @classmethod
    def get_valid_serology_names(cls):
        all_serology_names = {x for v in cls.valid_serology_map.values() for x in v}
        return all_serology_names

    def _map_serology_to_xx(self, locus, serology):
        if serology in serology_xx_exception_mapping.keys():
            return serology_xx_exception_mapping[serology]

        # Use the associated serology for XX version
        serology = self.find_associated_antigen(serology)

        # Extract just the digits
        antigen_group = sero_antigen_regex.match(serology).group(2)
        # Pad numbers with 0 for single digit numbers
        antigen_group_num = int(antigen_group)
        if antigen_group_num < 10:
            antigen_group = f"{antigen_group_num:02}"

        # Build the XX allele
        return f"{locus}*{antigen_group}:XX"

    @classmethod
    def _get_mapping(cls, broad, mapping, prefix):
        if prefix:
            return "HLA-" + broad, list(map(lambda x: "HLA-" + x, mapping[broad]))
        else:
            return broad, mapping[broad]
