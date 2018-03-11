#!/usr/bin/env python
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

"""
test_pyars
----------------------------------

Tests for `pyars` module.
"""
import os
import sys
import json
import unittest

from pyard import ARD


class TestPyard(unittest.TestCase):

    def setUp(self):
        self.ard = ARD(verbose=True)
        self.data_dir = os.path.dirname(__file__)
        self.assertIsInstance(self.ard, ARD)
        expected_json = self.data_dir + "/expected.json"
        with open(expected_json) as json_data:
            self.expected = json.load(json_data)
        pass

    def test_000_nomac(self):
        self.ardnomac = ARD(download_mac=False)
        self.assertIsInstance(self.ardnomac, ARD)
        self.assertFalse(self.ardnomac.download_mac)
        self.assertTrue(len(self.ardnomac.mac.keys()) == 0)
        self.assertTrue(self.ardnomac.redux("A*01:01:01", 'G') == "A*01:01:01G")
        self.assertTrue(self.ardnomac.redux("A*01:01:01", 'lg') == "A*01:01g")
        self.assertTrue(self.ardnomac.redux("A*01:01:01", 'lgx') == "A*01:01")
        self.assertTrue(self.ardnomac.redux("HLA-A*01:01:01", 'G') == "HLA-A*01:01:01G")
        self.assertTrue(self.ardnomac.redux("HLA-A*01:01:01", 'lg') == "HLA-A*01:01g")
        self.assertTrue(self.ardnomac.redux("HLA-A*01:01:01", 'lgx') == "HLA-A*01:01")
        pass

    def test_001_dbversions(self):
        for db in ['3310', '3300', '3290', '3280']:
            self.arddb = ARD(dbversion=db, download_mac=False)
            self.assertIsInstance(self.arddb, ARD)
            self.assertFalse(self.arddb.download_mac)
            self.assertTrue(self.arddb.dbversion == db)
            self.assertTrue(self.arddb.redux("A*01:01:01", 'G') == "A*01:01:01G")
            self.assertTrue(self.arddb.redux("A*01:01:01", 'lg') == "A*01:01g")
            self.assertTrue(self.arddb.redux("A*01:01:01", 'lgx') == "A*01:01")
        pass

    def test_002_remove_invalid(self):
        self.assertTrue(self.ard.redux("A*01:01:01", 'G') == "A*01:01:01G")
        pass

    def test_003_mac(self):
        self.assertTrue(self.ard.redux_gl("A*01:AB", 'G') == "A*01:01:01G/A*01:02")
        self.assertTrue(self.ard.redux_gl("HLA-A*01:AB", 'G') == "HLA-A*01:01:01G/HLA-A*01:02")
        pass

    def test_004_redux_gl(self):
        for ex in self.expected['redux_gl']:
            glstring = ex['glstring']
            ard_type = ex['ard_type']
            expected_gl = ex['expected_gl']
            self.assertTrue(self.ard.redux_gl(glstring, ard_type) == expected_gl)
        pass

    def test_005_mac_G(self):
        self.assertTrue(self.ard.redux("A*01:01:01", 'G') == "A*01:01:01G")
        pass




