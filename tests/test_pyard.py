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

import pyard.pyard
from pyard import ARD
from pyard.exceptions import InvalidAlleleError, InvalidMACError, InvalidTypingError


class TestPyArd(unittest.TestCase):

    @classmethod
    def setUpClass(cls) -> None:
        cls.db_version = '3440'
        cls.ard = ARD(cls.db_version, data_dir='/tmp/py-ard')

    def setUp(self):
        self.assertIsInstance(self.ard, ARD)

    def test_no_mac(self):
        self.assertEqual(self.ard.redux("A*01:01:01", 'G'), "A*01:01:01G")
        self.assertEqual(self.ard.redux("A*01:01:01", 'lg'), "A*01:01g")
        self.assertEqual(self.ard.redux("A*01:01:01", 'lgx'), "A*01:01")
        self.assertEqual(self.ard.redux("HLA-A*01:01:01", 'G'), "HLA-A*01:01:01G")
        self.assertEqual(self.ard.redux("HLA-A*01:01:01", 'lg'), "HLA-A*01:01g")
        self.assertEqual(self.ard.redux("HLA-A*01:01:01", 'lgx'), "HLA-A*01:01")

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

    def test_serology(self):
        data_dir = os.path.dirname(__file__)
        expected_json = data_dir + "/expected-serology.json"
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
        with self.assertRaises(InvalidAlleleError):
            self.ard.redux("HLA-A*01:AB", "G")

    def test_xx_code(self):
        expanded_string = """
        B*40:01:01G/B*40:01:03G/B*40:02:01G/B*40:03:01G/B*40:04:01G/B*40:05:01G/B*40:06:01G/B*40:07/B*40:08/B*40:09/B*40:10:01G/B*40:11:01G/B*40:12/B*40:13/B*40:14/B*40:15/B*40:16:01G/B*40:18/B*40:19/B*40:20:01G/B*40:21/B*40:22N/B*40:23/B*40:24/B*40:25/B*40:26/B*40:27/B*40:28/B*40:29/B*40:30/B*40:31/B*40:32/B*40:33/B*40:34/B*40:35/B*40:36/B*40:37/B*40:38/B*40:39/B*40:40:01G/B*40:42/B*40:43/B*40:44/B*40:45/B*40:46/B*40:47/B*40:48/B*40:49/B*40:50:01G/B*40:51/B*40:52/B*40:53/B*40:54/B*40:57/B*40:58/B*40:59/B*40:60/B*40:61/B*40:62/B*40:63/B*40:64:01G/B*40:65/B*40:66/B*40:67/B*40:68/B*40:69/B*40:70/B*40:71/B*40:72/B*40:73/B*40:74/B*40:75/B*40:76/B*40:77/B*40:78/B*40:79/B*40:80/B*40:81/B*40:82/B*40:83/B*40:84/B*40:85/B*40:86/B*40:87/B*40:88/B*40:89/B*40:90/B*40:91/B*40:92/B*40:93/B*40:94/B*40:95/B*40:96/B*40:98/B*40:99/B*40:100/B*40:101/B*40:102/B*40:103/B*40:104/B*40:105/B*40:106/B*40:107/B*40:108/B*40:109/B*40:110/B*40:111/B*40:112/B*40:113/B*40:114:01G/B*40:115/B*40:116/B*40:117/B*40:118N/B*40:119/B*40:120/B*40:121/B*40:122/B*40:123/B*40:124/B*40:125/B*40:126/B*40:127/B*40:128/B*40:129/B*40:130/B*40:131/B*40:132/B*40:133Q/B*40:134/B*40:135/B*40:136/B*40:137/B*40:138/B*40:139/B*40:140/B*40:142N/B*40:143/B*40:145/B*40:146/B*40:147/B*40:148/B*40:149/B*40:152/B*40:153/B*40:154/B*40:155:01G/B*40:156/B*40:157/B*40:158/B*40:159/B*40:160/B*40:161/B*40:162/B*40:163/B*40:164/B*40:165/B*40:166/B*40:167/B*40:168/B*40:169/B*40:170/B*40:171/B*40:172/B*40:173/B*40:174/B*40:175/B*40:177/B*40:178/B*40:180/B*40:181/B*40:182/B*40:183/B*40:184/B*40:185/B*40:186/B*40:187/B*40:188/B*40:189/B*40:190/B*40:191/B*40:192/B*40:193/B*40:194/B*40:195/B*40:196/B*40:197/B*40:198/B*40:199/B*40:200/B*40:201/B*40:202/B*40:203/B*40:204/B*40:205/B*40:206/B*40:207/B*40:208/B*40:209/B*40:210/B*40:211/B*40:212/B*40:213:01G/B*40:214/B*40:215/B*40:216N/B*40:217/B*40:218/B*40:219/B*40:220/B*40:222/B*40:223/B*40:224/B*40:225/B*40:226/B*40:227/B*40:228/B*40:230/B*40:231/B*40:232/B*40:233/B*40:234/B*40:235/B*40:237/B*40:238/B*40:239/B*40:240/B*40:242/B*40:243/B*40:244/B*40:245/B*40:246/B*40:248/B*40:249/B*40:250/B*40:251/B*40:252/B*40:253/B*40:254/B*40:255/B*40:256N/B*40:257/B*40:258/B*40:259/B*40:260/B*40:261/B*40:262/B*40:263N/B*40:265N/B*40:266/B*40:268/B*40:269/B*40:270/B*40:271/B*40:273/B*40:274/B*40:275/B*40:276/B*40:277/B*40:279/B*40:280/B*40:281/B*40:282/B*40:283/B*40:284/B*40:285/B*40:286N/B*40:287/B*40:288/B*40:289/B*40:290/B*40:291N/B*40:292/B*40:293/B*40:294/B*40:295/B*40:296/B*40:297/B*40:298/B*40:300/B*40:302/B*40:304/B*40:305/B*40:306/B*40:307/B*40:308/B*40:309/B*40:310/B*40:311/B*40:312/B*40:313/B*40:314/B*40:315/B*40:316/B*40:317/B*40:318/B*40:319/B*40:320/B*40:321/B*40:322/B*40:323/B*40:324/B*40:325/B*40:326/B*40:327/B*40:328/B*40:330/B*40:331/B*40:332/B*40:333/B*40:334/B*40:335/B*40:336/B*40:337N/B*40:339/B*40:340/B*40:341/B*40:342/B*40:343/B*40:344/B*40:345N/B*40:346/B*40:347/B*40:348/B*40:349/B*40:350/B*40:351/B*40:352/B*40:354/B*40:355/B*40:357/B*40:358/B*40:359/B*40:360/B*40:361N/B*40:362/B*40:363/B*40:364/B*40:365/B*40:366/B*40:367/B*40:368/B*40:369/B*40:370/B*40:371/B*40:372N/B*40:373/B*40:374/B*40:375/B*40:376/B*40:377/B*40:378/B*40:380/B*40:381/B*40:382/B*40:385/B*40:388/B*40:389/B*40:390/B*40:391/B*40:392/B*40:393/B*40:394/B*40:396/B*40:397/B*40:398/B*40:399N/B*40:400/B*40:401/B*40:402/B*40:403/B*40:404/B*40:407/B*40:408/B*40:409/B*40:410/B*40:411/B*40:412/B*40:413/B*40:414/B*40:415/B*40:420/B*40:421Q/B*40:422/B*40:423/B*40:424/B*40:426N/B*40:428N/B*40:429/B*40:430/B*40:432/B*40:433/B*40:434/B*40:436/B*40:437/B*40:438N/B*40:441/B*40:445/B*40:447/B*40:448/B*40:449/B*40:451/B*40:452/B*40:454/B*40:457/B*40:458/B*40:459/B*40:460/B*40:461/B*40:462/B*40:463/B*40:465/B*40:466/B*40:467/B*40:468/B*40:469/B*40:470/B*40:471/B*40:472/B*40:477/B*40:478/B*40:479/B*40:481N/B*40:482
        """.strip()
        gl = self.ard.redux_gl('B*40:XX', 'G')
        self.assertEqual(gl, expanded_string)

    def test_xx_code_with_prefix(self):
        expanded_string = """
        HLA-B*40:01:01G/HLA-B*40:01:03G/HLA-B*40:02:01G/HLA-B*40:03:01G/HLA-B*40:04:01G/HLA-B*40:05:01G/HLA-B*40:06:01G/HLA-B*40:07/HLA-B*40:08/HLA-B*40:09/HLA-B*40:10:01G/HLA-B*40:11:01G/HLA-B*40:12/HLA-B*40:13/HLA-B*40:14/HLA-B*40:15/HLA-B*40:16:01G/HLA-B*40:18/HLA-B*40:19/HLA-B*40:20:01G/HLA-B*40:21/HLA-B*40:22N/HLA-B*40:23/HLA-B*40:24/HLA-B*40:25/HLA-B*40:26/HLA-B*40:27/HLA-B*40:28/HLA-B*40:29/HLA-B*40:30/HLA-B*40:31/HLA-B*40:32/HLA-B*40:33/HLA-B*40:34/HLA-B*40:35/HLA-B*40:36/HLA-B*40:37/HLA-B*40:38/HLA-B*40:39/HLA-B*40:40:01G/HLA-B*40:42/HLA-B*40:43/HLA-B*40:44/HLA-B*40:45/HLA-B*40:46/HLA-B*40:47/HLA-B*40:48/HLA-B*40:49/HLA-B*40:50:01G/HLA-B*40:51/HLA-B*40:52/HLA-B*40:53/HLA-B*40:54/HLA-B*40:57/HLA-B*40:58/HLA-B*40:59/HLA-B*40:60/HLA-B*40:61/HLA-B*40:62/HLA-B*40:63/HLA-B*40:64:01G/HLA-B*40:65/HLA-B*40:66/HLA-B*40:67/HLA-B*40:68/HLA-B*40:69/HLA-B*40:70/HLA-B*40:71/HLA-B*40:72/HLA-B*40:73/HLA-B*40:74/HLA-B*40:75/HLA-B*40:76/HLA-B*40:77/HLA-B*40:78/HLA-B*40:79/HLA-B*40:80/HLA-B*40:81/HLA-B*40:82/HLA-B*40:83/HLA-B*40:84/HLA-B*40:85/HLA-B*40:86/HLA-B*40:87/HLA-B*40:88/HLA-B*40:89/HLA-B*40:90/HLA-B*40:91/HLA-B*40:92/HLA-B*40:93/HLA-B*40:94/HLA-B*40:95/HLA-B*40:96/HLA-B*40:98/HLA-B*40:99/HLA-B*40:100/HLA-B*40:101/HLA-B*40:102/HLA-B*40:103/HLA-B*40:104/HLA-B*40:105/HLA-B*40:106/HLA-B*40:107/HLA-B*40:108/HLA-B*40:109/HLA-B*40:110/HLA-B*40:111/HLA-B*40:112/HLA-B*40:113/HLA-B*40:114:01G/HLA-B*40:115/HLA-B*40:116/HLA-B*40:117/HLA-B*40:118N/HLA-B*40:119/HLA-B*40:120/HLA-B*40:121/HLA-B*40:122/HLA-B*40:123/HLA-B*40:124/HLA-B*40:125/HLA-B*40:126/HLA-B*40:127/HLA-B*40:128/HLA-B*40:129/HLA-B*40:130/HLA-B*40:131/HLA-B*40:132/HLA-B*40:133Q/HLA-B*40:134/HLA-B*40:135/HLA-B*40:136/HLA-B*40:137/HLA-B*40:138/HLA-B*40:139/HLA-B*40:140/HLA-B*40:142N/HLA-B*40:143/HLA-B*40:145/HLA-B*40:146/HLA-B*40:147/HLA-B*40:148/HLA-B*40:149/HLA-B*40:152/HLA-B*40:153/HLA-B*40:154/HLA-B*40:155:01G/HLA-B*40:156/HLA-B*40:157/HLA-B*40:158/HLA-B*40:159/HLA-B*40:160/HLA-B*40:161/HLA-B*40:162/HLA-B*40:163/HLA-B*40:164/HLA-B*40:165/HLA-B*40:166/HLA-B*40:167/HLA-B*40:168/HLA-B*40:169/HLA-B*40:170/HLA-B*40:171/HLA-B*40:172/HLA-B*40:173/HLA-B*40:174/HLA-B*40:175/HLA-B*40:177/HLA-B*40:178/HLA-B*40:180/HLA-B*40:181/HLA-B*40:182/HLA-B*40:183/HLA-B*40:184/HLA-B*40:185/HLA-B*40:186/HLA-B*40:187/HLA-B*40:188/HLA-B*40:189/HLA-B*40:190/HLA-B*40:191/HLA-B*40:192/HLA-B*40:193/HLA-B*40:194/HLA-B*40:195/HLA-B*40:196/HLA-B*40:197/HLA-B*40:198/HLA-B*40:199/HLA-B*40:200/HLA-B*40:201/HLA-B*40:202/HLA-B*40:203/HLA-B*40:204/HLA-B*40:205/HLA-B*40:206/HLA-B*40:207/HLA-B*40:208/HLA-B*40:209/HLA-B*40:210/HLA-B*40:211/HLA-B*40:212/HLA-B*40:213:01G/HLA-B*40:214/HLA-B*40:215/HLA-B*40:216N/HLA-B*40:217/HLA-B*40:218/HLA-B*40:219/HLA-B*40:220/HLA-B*40:222/HLA-B*40:223/HLA-B*40:224/HLA-B*40:225/HLA-B*40:226/HLA-B*40:227/HLA-B*40:228/HLA-B*40:230/HLA-B*40:231/HLA-B*40:232/HLA-B*40:233/HLA-B*40:234/HLA-B*40:235/HLA-B*40:237/HLA-B*40:238/HLA-B*40:239/HLA-B*40:240/HLA-B*40:242/HLA-B*40:243/HLA-B*40:244/HLA-B*40:245/HLA-B*40:246/HLA-B*40:248/HLA-B*40:249/HLA-B*40:250/HLA-B*40:251/HLA-B*40:252/HLA-B*40:253/HLA-B*40:254/HLA-B*40:255/HLA-B*40:256N/HLA-B*40:257/HLA-B*40:258/HLA-B*40:259/HLA-B*40:260/HLA-B*40:261/HLA-B*40:262/HLA-B*40:263N/HLA-B*40:265N/HLA-B*40:266/HLA-B*40:268/HLA-B*40:269/HLA-B*40:270/HLA-B*40:271/HLA-B*40:273/HLA-B*40:274/HLA-B*40:275/HLA-B*40:276/HLA-B*40:277/HLA-B*40:279/HLA-B*40:280/HLA-B*40:281/HLA-B*40:282/HLA-B*40:283/HLA-B*40:284/HLA-B*40:285/HLA-B*40:286N/HLA-B*40:287/HLA-B*40:288/HLA-B*40:289/HLA-B*40:290/HLA-B*40:291N/HLA-B*40:292/HLA-B*40:293/HLA-B*40:294/HLA-B*40:295/HLA-B*40:296/HLA-B*40:297/HLA-B*40:298/HLA-B*40:300/HLA-B*40:302/HLA-B*40:304/HLA-B*40:305/HLA-B*40:306/HLA-B*40:307/HLA-B*40:308/HLA-B*40:309/HLA-B*40:310/HLA-B*40:311/HLA-B*40:312/HLA-B*40:313/HLA-B*40:314/HLA-B*40:315/HLA-B*40:316/HLA-B*40:317/HLA-B*40:318/HLA-B*40:319/HLA-B*40:320/HLA-B*40:321/HLA-B*40:322/HLA-B*40:323/HLA-B*40:324/HLA-B*40:325/HLA-B*40:326/HLA-B*40:327/HLA-B*40:328/HLA-B*40:330/HLA-B*40:331/HLA-B*40:332/HLA-B*40:333/HLA-B*40:334/HLA-B*40:335/HLA-B*40:336/HLA-B*40:337N/HLA-B*40:339/HLA-B*40:340/HLA-B*40:341/HLA-B*40:342/HLA-B*40:343/HLA-B*40:344/HLA-B*40:345N/HLA-B*40:346/HLA-B*40:347/HLA-B*40:348/HLA-B*40:349/HLA-B*40:350/HLA-B*40:351/HLA-B*40:352/HLA-B*40:354/HLA-B*40:355/HLA-B*40:357/HLA-B*40:358/HLA-B*40:359/HLA-B*40:360/HLA-B*40:361N/HLA-B*40:362/HLA-B*40:363/HLA-B*40:364/HLA-B*40:365/HLA-B*40:366/HLA-B*40:367/HLA-B*40:368/HLA-B*40:369/HLA-B*40:370/HLA-B*40:371/HLA-B*40:372N/HLA-B*40:373/HLA-B*40:374/HLA-B*40:375/HLA-B*40:376/HLA-B*40:377/HLA-B*40:378/HLA-B*40:380/HLA-B*40:381/HLA-B*40:382/HLA-B*40:385/HLA-B*40:388/HLA-B*40:389/HLA-B*40:390/HLA-B*40:391/HLA-B*40:392/HLA-B*40:393/HLA-B*40:394/HLA-B*40:396/HLA-B*40:397/HLA-B*40:398/HLA-B*40:399N/HLA-B*40:400/HLA-B*40:401/HLA-B*40:402/HLA-B*40:403/HLA-B*40:404/HLA-B*40:407/HLA-B*40:408/HLA-B*40:409/HLA-B*40:410/HLA-B*40:411/HLA-B*40:412/HLA-B*40:413/HLA-B*40:414/HLA-B*40:415/HLA-B*40:420/HLA-B*40:421Q/HLA-B*40:422/HLA-B*40:423/HLA-B*40:424/HLA-B*40:426N/HLA-B*40:428N/HLA-B*40:429/HLA-B*40:430/HLA-B*40:432/HLA-B*40:433/HLA-B*40:434/HLA-B*40:436/HLA-B*40:437/HLA-B*40:438N/HLA-B*40:441/HLA-B*40:445/HLA-B*40:447/HLA-B*40:448/HLA-B*40:449/HLA-B*40:451/HLA-B*40:452/HLA-B*40:454/HLA-B*40:457/HLA-B*40:458/HLA-B*40:459/HLA-B*40:460/HLA-B*40:461/HLA-B*40:462/HLA-B*40:463/HLA-B*40:465/HLA-B*40:466/HLA-B*40:467/HLA-B*40:468/HLA-B*40:469/HLA-B*40:470/HLA-B*40:471/HLA-B*40:472/HLA-B*40:477/HLA-B*40:478/HLA-B*40:479/HLA-B*40:481N/HLA-B*40:482
        """.strip()
        gl = self.ard.redux_gl('HLA-B*40:XX', 'G')
        self.assertEqual(expanded_string, gl)

    def test_expand_mac(self):
        mac_ab_expanded = ['A*01:01', 'A*01:02']
        self.assertEqual(self.ard.expand_mac('A*01:AB'), mac_ab_expanded)

        mac_hla_ab_expanded = ['HLA-A*01:01', 'HLA-A*01:02']
        self.assertEqual(self.ard.expand_mac('HLA-A*01:AB'), mac_hla_ab_expanded)

        mac_ac_expanded = ['A*01:01', 'A*01:03']
        self.assertEqual(self.ard.expand_mac('A*01:AC'), mac_ac_expanded)

        mac_hla_ac_expanded = ['HLA-A*01:01', 'HLA-A*01:03']
        self.assertEqual(self.ard.expand_mac('HLA-A*01:AC'), mac_hla_ac_expanded)

    def test_mac_toG(self):
        g_alleles = 'A*01:01:01G/A*01:03:01G'
        self.assertEqual(self.ard.mac_toG('A*01:AC'), g_alleles)
        with self.assertRaises(InvalidMACError):
            self.ard.mac_toG('A*01:AB')

    def test_redux_types(self):
        self.assertIsNone(pyard.pyard.validate_reduction_type('G'))
        self.assertIsNone(pyard.pyard.validate_reduction_type('lg'))
        self.assertIsNone(pyard.pyard.validate_reduction_type('lgx'))
        self.assertIsNone(pyard.pyard.validate_reduction_type('W'))
        self.assertIsNone(pyard.pyard.validate_reduction_type('exon'))
        with self.assertRaises(ValueError):
            pyard.pyard.validate_reduction_type('XX')

    def test_empty_allele(self):
        with self.assertRaises(InvalidTypingError):
            self.ard.redux_gl('A*', 'lgx')

    def test_fp_allele(self):
        with self.assertRaises(InvalidTypingError):
            self.ard.redux_gl('A*0.123', 'lgx')

    def test_invalid_serology(self):
        # Test that A10 works and the first one is 'A*25:01'
        serology_a10 = self.ard.redux_gl('A10', 'lgx')
        self.assertEqual(serology_a10.split('/')[0], 'A*25:01')
        # And A100 isn't a valid typing
        with self.assertRaises(InvalidTypingError):
            self.ard.redux_gl('A100', 'lgx')

    def test_allele_duplicated(self):
        # Make sure the reduced alleles are unique
        # https://github.com/nmdp-bioinformatics/py-ard/issues/135
        allele_code = "C*02:ACMGS"
        allele_code_rx = self.ard.redux_gl(allele_code, 'lgx')
        self.assertEqual(allele_code_rx, 'C*02:02/C*02:10')
