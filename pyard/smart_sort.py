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
import functools
import re

from pyard import constants

expr_regex = re.compile("[PNQLSGg]")
glstring_chars = re.compile("[/|+^~]")
serology_splitter = re.compile(r"(\D+)(\d+)")


@functools.lru_cache(maxsize=constants.DEFAULT_CACHE_SIZE)
def smart_sort_comparator(a1, a2, ignore_suffixes=()):
    """
    Natural sort 2 given alleles.

    Python sorts strings lexicographically but HLA alleles need
    to be sorted by numerical values in each field of the HLA nomenclature.

    If allele suffixes are in ignore_suffixes, comparison results in that
    appearing later.

    :param a1: first allele
    :param a2: second allele
    :param ignore_suffix: tuple of suffixes
    """

    # Check to see if they are the same alleles
    if a1 == a2:
        return 0

    # GL String matches
    if re.search(glstring_chars, a1) or re.search(glstring_chars, a2):
        if a1 > a2:
            return 1
        else:
            return -1

    if ignore_suffixes and "*" in a1:
        _, fields = a1.split("*")
        if fields in ignore_suffixes:
            return 1

    if ignore_suffixes and "*" in a2:
        _, fields = a2.split("*")
        if fields in ignore_suffixes:
            return -1

    # remove any non-numerics
    a1 = re.sub(expr_regex, "", a1)
    a2 = re.sub(expr_regex, "", a2)

    # Check to see if they are still the same alleles
    if a1 == a2:
        return 0

    # Handle serology
    if ":" not in a1:
        serology1_match = serology_splitter.match(a1)
        serology1_num = int(serology1_match.group(2))
        serology2_match = serology_splitter.match(a2)
        serology2_num = int(serology2_match.group(2))
        return 1 if serology1_num > serology2_num else -1

    # Extract and Compare 1st fields first
    a1_f1 = int(a1[a1.find("*") + 1 : a1.find(":")])
    a2_f1 = int(a2[a2.find("*") + 1 : a2.find(":")])

    if a1_f1 < a2_f1:
        return -1
    if a1_f1 > a2_f1:
        return 1

    a1_fields = a1.split(":")
    a2_fields = a2.split(":")

    # If the first fields are equal, try the 2nd fields
    a1_f2 = int(a1_fields[1])
    a2_f2 = int(a2_fields[1])

    if a1_f2 < a2_f2:
        return -1
    if a1_f2 > a2_f2:
        return 1

    # If the second fields are equal, try the 3rd fields
    if len(a1_fields) > 2:
        try:
            a1_f3 = int(a1_fields[2])
        except ValueError:
            a1_f3 = 0
    else:
        a1_f3 = 0
    if len(a2_fields) > 2:
        try:
            a2_f3 = int(a2_fields[2])
        except ValueError:
            a2_f3 = 0
    else:
        a2_f3 = 0

    if a1_f3 < a2_f3:
        return -1
    if a1_f3 > a2_f3:
        return 1

    # If the third fields are equal, try the 4th fields
    if len(a1_fields) > 3:
        try:
            a1_f4 = int(a1_fields[3])
        except ValueError:
            a1_f4 = 0
    else:
        a1_f4 = 0
    if len(a2_fields) > 3:
        try:
            a2_f4 = int(a2_fields[3])
        except ValueError:
            a2_f4 = 0
    else:
        a2_f4 = 0

    if a1_f4 < a2_f4:
        return -1
    if a1_f4 > a2_f4:
        return 1

    # All fields are considered equal after 4th field
    return 0
