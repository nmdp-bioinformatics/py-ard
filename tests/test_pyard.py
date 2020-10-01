#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#    py-ard pyARD.
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

"""
test_pyard
----------------------------------

Tests for `py-ard` module.
"""
import json
import os
import unittest

from pyard import ARD


class TestPyArd(unittest.TestCase):

    @classmethod
    def setUpClass(cls) -> None:
        cls.db_version = '3290'
        cls.ard = ARD(cls.db_version, data_dir='/tmp/3290')

    def setUp(self):
        self.assertIsInstance(self.ard, ARD)

    def test_no_mac(self):
        self.ard_no_mac = ARD(self.db_version, data_dir='/tmp/3290', load_mac_file=False)
        self.assertIsInstance(self.ard_no_mac, ARD)
        self.assertEqual(len(self.ard_no_mac.mac.keys()), 0)
        self.assertEqual(self.ard_no_mac.redux("A*01:01:01", 'G'), "A*01:01:01G")
        self.assertEqual(self.ard_no_mac.redux("A*01:01:01", 'lg'), "A*01:01g")
        self.assertEqual(self.ard_no_mac.redux("A*01:01:01", 'lgx'), "A*01:01")
        self.assertEqual(self.ard_no_mac.redux("HLA-A*01:01:01", 'G'), "HLA-A*01:01:01G")
        self.assertEqual(self.ard_no_mac.redux("HLA-A*01:01:01", 'lg'), "HLA-A*01:01g")
        self.assertEqual(self.ard_no_mac.redux("HLA-A*01:01:01", 'lgx'), "HLA-A*01:01")

    def test_remove_invalid(self):
        self.assertEqual(self.ard.redux("A*01:01:01", 'G'), "A*01:01:01G")

    def test_mac(self):
        self.assertEqual(self.ard.redux_gl("A*01:AB", 'G'), "A*01:01:01G/A*01:02")
        self.assertEqual(self.ard.redux_gl("HLA-A*01:AB", 'G'), "HLA-A*01:01:01G/HLA-A*01:02")

    def test_redux_gl(self):
        data_dir = os.path.dirname(__file__)
        expected_json = data_dir + "/expected.json"
        with open(expected_json) as json_data:
            expected = json.load(json_data)
        for ex in expected['redux_gl']:
            glstring = ex['glstring']
            ard_type = ex['ard_type']
            expected_gl = ex['expected_gl']
            self.assertEqual(self.ard.redux_gl(glstring, ard_type), expected_gl)

    def test_mac_G(self):
        self.assertEqual(self.ard.redux("A*01:01:01", 'G'), "A*01:01:01G")
        self.assertEqual(self.ard.redux_gl("HLA-A*01:AB", "G"), "HLA-A*01:01:01G/HLA-A*01:02")
        self.assertEqual(self.ard.redux("HLA-A*01:AB", "G"), "")
