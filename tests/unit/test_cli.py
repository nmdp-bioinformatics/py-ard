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
"""
Lightweight tests for the py-ard CLI entry points.

These exercise the argparse-level behavior of each ``main()`` (``--help`` /
``--config`` validation) without needing a reference database, confirming the
console-script modules are importable and wired correctly.

``pyard-reduce-csv`` and ``pyard-import``'s mapping helper depend on pandas
(the ``script`` optional-dependency group), so tests touching ``reduce_csv``
are skipped when pandas is not installed.
"""

import importlib.util
import sys
import unittest

from pyard.cli import import_db, redux, status

HAS_PANDAS = importlib.util.find_spec("pandas") is not None


class CliEntryPointTest(unittest.TestCase):
    def _assert_help_exits_zero(self, module):
        # argparse raises SystemExit(0) on --help
        argv = sys.argv
        try:
            sys.argv = [module.__name__, "--help"]
            with self.assertRaises(SystemExit) as cm:
                module.main()
        finally:
            sys.argv = argv
        self.assertEqual(cm.exception.code, 0)

    def test_all_main_callables(self):
        for module in (redux, import_db, status):
            self.assertTrue(callable(module.main), f"{module.__name__}.main")

    def test_redux_help(self):
        self._assert_help_exits_zero(redux)

    def test_import_db_help(self):
        self._assert_help_exits_zero(import_db)

    def test_status_help(self):
        self._assert_help_exits_zero(status)

    @unittest.skipUnless(HAS_PANDAS, "requires the 'script' extra (pandas)")
    def test_reduce_csv_help(self):
        from pyard.cli import reduce_csv

        self._assert_help_exits_zero(reduce_csv)

    @unittest.skipUnless(HAS_PANDAS, "requires the 'script' extra (pandas)")
    def test_reduce_csv_requires_config(self):
        from pyard.cli import reduce_csv

        # Without a config file (and not --generate), reduce_csv exits with 1.
        argv = sys.argv
        try:
            sys.argv = ["pyard-reduce-csv"]
            with self.assertRaises(SystemExit) as cm:
                reduce_csv.main()
            self.assertEqual(cm.exception.code, 1)
        finally:
            sys.argv = argv


if __name__ == "__main__":
    unittest.main()
