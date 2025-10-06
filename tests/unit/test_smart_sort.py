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
from pyard.smart_sort import smart_sort_comparator


def test_same_comparator():
    allele = "HLA-A*01:01"
    assert smart_sort_comparator(allele, allele) == 0


def test_equal_comparator():
    allele1 = "HLA-A*01:01"
    allele2 = "HLA-A*01:01"
    assert smart_sort_comparator(allele1, allele2) == 0


def test_equal_comparator_G():
    # Should compare without G
    allele1 = "HLA-A*01:01G"
    allele2 = "HLA-A*01:01"
    assert smart_sort_comparator(allele1, allele2) == 0


def test_equal_comparator_NG():
    # Should compare without N and G
    allele1 = "HLA-A*01:01G"
    allele2 = "HLA-A*01:01N"
    assert smart_sort_comparator(allele1, allele2) == 0


def test_first_field_comparator_le():
    allele1 = "HLA-A*01:01"
    allele2 = "HLA-A*02:01"
    assert smart_sort_comparator(allele1, allele2) == -1


def test_first_field_comparator_ge():
    allele1 = "HLA-A*02:01"
    allele2 = "HLA-A*01:01"
    assert smart_sort_comparator(allele1, allele2) == 1


def test_second_field_comparator_le():
    allele1 = "HLA-A*01:01"
    allele2 = "HLA-A*01:02"
    assert smart_sort_comparator(allele1, allele2) == -1


def test_second_field_comparator_le_smart():
    allele1 = "HLA-A*01:29"
    allele2 = "HLA-A*01:100"
    assert smart_sort_comparator(allele1, allele2) == -1


def test_second_field_comparator_ge():
    allele1 = "HLA-A*01:02"
    allele2 = "HLA-A*01:01"
    assert smart_sort_comparator(allele1, allele2) == 1


def test_third_field_comparator_le():
    allele1 = "HLA-A*01:01:01"
    allele2 = "HLA-A*01:01:20"
    assert smart_sort_comparator(allele1, allele2) == -1


def test_third_field_comparator_le_smart():
    allele1 = "HLA-A*01:01:29"
    allele2 = "HLA-A*01:01:100"
    assert smart_sort_comparator(allele1, allele2) == -1


def test_third_field_comparator_ge():
    allele1 = "HLA-A*01:01:02"
    allele2 = "HLA-A*01:01:01"
    assert smart_sort_comparator(allele1, allele2) == 1


def test_fourth_field_comparator_le():
    allele1 = "HLA-A*01:01:01:01"
    allele2 = "HLA-A*01:01:01:20"
    assert smart_sort_comparator(allele1, allele2) == -1


def test_fourth_field_comparator_le_smart():
    allele1 = "HLA-A*01:01:01:39"
    allele2 = "HLA-A*01:01:01:200"
    assert smart_sort_comparator(allele1, allele2) == -1


def test_fourth_field_comparator_ge():
    allele1 = "HLA-A*01:01:01:30"
    allele2 = "HLA-A*01:01:01:09"
    assert smart_sort_comparator(allele1, allele2) == 1


def test_serology_ge():
    serology1 = "Cw10"
    serology2 = "Cw3"
    assert smart_sort_comparator(serology1, serology2) == 1


def test_serology_le():
    serology1 = "A10"
    serology2 = "A25"
    assert smart_sort_comparator(serology1, serology2) == -1


def test_serology_eq():
    serology1 = "B70"
    serology2 = "B70"
    assert smart_sort_comparator(serology1, serology2) == 0
