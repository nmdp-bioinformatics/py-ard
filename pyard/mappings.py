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
from collections import namedtuple

ars_mapping_tables = [
    "dup_g",
    "dup_lgx",
    "g_group",
    "p_group",
    "lgx_group",
    "exon_group",
    "p_not_g",
]

code_mapping_tables = [
    "xx_codes",
    "who_group",
]

allele_tables = [
    "alleles",
    "exp_alleles",
    "who_alleles",
]

ARSMapping = namedtuple("ARSMapping", ars_mapping_tables)
CodeMappings = namedtuple("CodeMappings", code_mapping_tables)
AlleleGroups = namedtuple("AlleleGroups", allele_tables)
