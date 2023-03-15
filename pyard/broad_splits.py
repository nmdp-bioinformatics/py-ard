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

#
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

# Loaded at runtime
broad_splits_ser_mapping = None

HLA_regex = re.compile("^HLA-")


def find_splits(allele: str) -> tuple:
    if HLA_regex.search(allele):
        prefix = True
        allele_name = allele.split("-")[1]
    else:
        prefix = False
        allele_name = allele

    if "*" in allele_name:
        mapping = broad_splits_dna_mapping
    else:
        mapping = broad_splits_ser_mapping

    if allele_name in mapping:
        return _get_mapping(allele_name, mapping, prefix)

    for broad in mapping:
        if allele_name in mapping[broad]:
            return _get_mapping(broad, mapping, prefix)


def _get_mapping(broad, mapping, prefix):
    if prefix:
        return "HLA-" + broad, list(map(lambda x: "HLA-" + x, mapping[broad]))
    else:
        return broad, mapping[broad]
