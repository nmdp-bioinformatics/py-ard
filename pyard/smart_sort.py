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

# Regular expressions for parsing HLA nomenclature components
expr_regex = re.compile(
    "[PNQLSGg]"
)  # Expression characters (P/G groups, null alleles, etc.)
glstring_chars = re.compile("[/|+^~]")  # GL string delimiter characters
serology_splitter = re.compile(
    r"(\D+)(\d+)"
)  # Separates locus letters from numbers in serology


@functools.lru_cache(maxsize=constants.DEFAULT_CACHE_SIZE)
def smart_sort_comparator(a1, a2, ignore_suffixes=()):
    """
    Natural sort 2 given alleles using HLA nomenclature rules.

    Python's default lexicographic sorting doesn't work correctly for HLA alleles
    because it treats field values as strings rather than numbers. This function
    implements proper numerical sorting for each field in HLA nomenclature.

    Sorting hierarchy:
    1. Handle identical alleles
    2. Handle GL string delimiters (lexicographic fallback)
    3. Handle ignored suffixes (push to end)
    4. Handle serological designations (numeric comparison)
    5. Handle molecular alleles (field-by-field numeric comparison)

    :param a1: first allele to compare
    :param a2: second allele to compare
    :param ignore_suffixes: tuple of allele suffixes to sort last
    :return: -1 if a1 < a2, 0 if equal, 1 if a1 > a2
    """

    # Quick equality check - identical alleles are equal
    if a1 == a2:
        return 0

    # Handle GL string delimiters - fall back to lexicographic sorting
    # GL strings with delimiters (/|+^~) are complex and sorted lexicographically
    if re.search(glstring_chars, a1) or re.search(glstring_chars, a2):
        if a1 > a2:
            return 1
        else:
            return -1

    # Handle ignored suffixes - push alleles with these suffixes to the end
    # This allows certain allele types to be sorted last (e.g., expression variants)
    if ignore_suffixes and "*" in a1:
        _, fields = a1.split("*")
        if fields in ignore_suffixes:
            return 1  # a1 comes after a2

    if ignore_suffixes and "*" in a2:
        _, fields = a2.split("*")
        if fields in ignore_suffixes:
            return -1  # a2 comes after a1

    # Remove expression characters (P, N, Q, L, S, G, g) for comparison
    # This normalizes alleles like 'A*01:01N' to 'A*01:01' for sorting
    a1 = re.sub(expr_regex, "", a1)
    a2 = re.sub(expr_regex, "", a2)

    # Check equality again after removing expression characters
    if a1 == a2:
        return 0

    # Handle serological designations (no colon separator)
    # Compare numeric parts of serology (e.g., '27' in 'B27')
    if ":" not in a1:
        serology1_match = serology_splitter.match(a1)
        serology1_num = int(serology1_match.group(2))  # Extract numeric part
        serology2_match = serology_splitter.match(a2)
        serology2_num = int(serology2_match.group(2))  # Extract numeric part
        return 1 if serology1_num > serology2_num else -1

    # Compare first field (allele group) numerically
    # Extract numbers between '*' and first ':' (e.g., '01' from 'A*01:01')
    a1_f1 = int(a1[a1.find("*") + 1 : a1.find(":")])
    a2_f1 = int(a2[a2.find("*") + 1 : a2.find(":")])

    if a1_f1 < a2_f1:
        return -1
    if a1_f1 > a2_f1:
        return 1

    # Split alleles into fields for detailed comparison
    a1_fields = a1.split(":")
    a2_fields = a2.split(":")

    # Compare second field (protein variation) numerically
    a1_f2 = int(a1_fields[1])
    a2_f2 = int(a2_fields[1])

    if a1_f2 < a2_f2:
        return -1
    if a1_f2 > a2_f2:
        return 1

    # Compare third field (synonymous DNA variation) numerically
    # Handle missing fields or non-numeric values gracefully
    if len(a1_fields) > 2:
        try:
            a1_f3 = int(a1_fields[2])
        except ValueError:
            a1_f3 = 0  # Non-numeric third field treated as 0
    else:
        a1_f3 = 0  # Missing third field treated as 0

    if len(a2_fields) > 2:
        try:
            a2_f3 = int(a2_fields[2])
        except ValueError:
            a2_f3 = 0  # Non-numeric third field treated as 0
    else:
        a2_f3 = 0  # Missing third field treated as 0

    if a1_f3 < a2_f3:
        return -1
    if a1_f3 > a2_f3:
        return 1

    # Compare fourth field (non-coding variation) numerically
    # Handle missing fields or non-numeric values gracefully
    if len(a1_fields) > 3:
        try:
            a1_f4 = int(a1_fields[3])
        except ValueError:
            a1_f4 = 0  # Non-numeric fourth field treated as 0
    else:
        a1_f4 = 0  # Missing fourth field treated as 0

    if len(a2_fields) > 3:
        try:
            a2_f4 = int(a2_fields[3])
        except ValueError:
            a2_f4 = 0  # Non-numeric fourth field treated as 0
    else:
        a2_f4 = 0  # Missing fourth field treated as 0

    if a1_f4 < a2_f4:
        return -1
    if a1_f4 > a2_f4:
        return 1

    # All compared fields are equal - alleles are considered equivalent for sorting
    return 0
