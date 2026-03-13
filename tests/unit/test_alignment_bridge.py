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
import sys
from unittest.mock import patch, MagicMock, PropertyMock

import pytest

from pyard.alignment_bridge import HLAToolsBridge, VALID_LOCI
from pyard.exceptions import HLAToolsNotAvailableError


class TestIsAvailable:
    def test_unavailable_when_rpy2_missing(self):
        bridge = HLAToolsBridge()
        with patch.dict(sys.modules, {"rpy2": None}):
            with patch("importlib.import_module", side_effect=ImportError):
                assert bridge.is_available is False

    def test_unavailable_when_hlatools_not_installed(self):
        bridge = HLAToolsBridge()
        mock_rpy2 = MagicMock()
        with patch("importlib.import_module", return_value=mock_rpy2):
            with patch("rpy2.robjects.packages.isinstalled", return_value=False):
                assert bridge.is_available is False

    def test_available_when_both_present(self):
        bridge = HLAToolsBridge()
        mock_rpy2 = MagicMock()
        mock_packages = MagicMock()
        mock_packages.isinstalled = MagicMock(return_value=True)
        mock_robjects = MagicMock()
        mock_robjects.packages = mock_packages
        with patch.dict(
            sys.modules,
            {
                "rpy2": mock_rpy2,
                "rpy2.robjects": mock_robjects,
                "rpy2.robjects.packages": mock_packages,
            },
        ):
            assert bridge.is_available is True


class TestEnsureRInitialized:
    def test_raises_when_not_available(self):
        bridge = HLAToolsBridge()
        with patch.object(
            type(bridge), "is_available", new_callable=PropertyMock, return_value=False
        ):
            with pytest.raises(HLAToolsNotAvailableError):
                bridge._ensure_r_initialized()

    def test_does_not_reinitialize(self):
        bridge = HLAToolsBridge()
        bridge._r_initialized = True
        # Should return immediately without checking availability
        bridge._ensure_r_initialized()


class TestGetAlignment:
    def test_invalid_locus_raises_value_error(self):
        bridge = HLAToolsBridge()
        with pytest.raises(ValueError, match="Invalid locus"):
            bridge.get_alignment("INVALID")

    def test_cache_hit(self):
        bridge = HLAToolsBridge()
        cached_data = {"DPB1*04:01:01:01": "MMVLQ"}
        bridge._alignment_cache["DPB1"] = cached_data

        result = bridge.get_alignment("DPB1")
        assert result is cached_data

    def test_cache_populated_after_first_call(self):
        """Verify that after populating the cache, subsequent calls return cached data."""
        bridge = HLAToolsBridge()
        # Pre-populate cache to simulate a successful R call
        bridge._alignment_cache["DPB1"] = {
            "DPB1*04:01:01:01": "MVLQ",
            "DPB1*04:02:01:01": "MVAQ",
        }
        result = bridge.get_alignment("DPB1")
        assert result == {
            "DPB1*04:01:01:01": "MVLQ",
            "DPB1*04:02:01:01": "MVAQ",
        }

    def test_uncached_locus_raises_without_r(self):
        """Verify that accessing an uncached locus without R raises."""
        bridge = HLAToolsBridge()
        with patch.object(
            type(bridge), "is_available", new_callable=PropertyMock, return_value=False
        ):
            with pytest.raises(HLAToolsNotAvailableError):
                bridge.get_alignment("DPB1")


class TestGetSequence:
    def test_none_for_empty_allele(self):
        bridge = HLAToolsBridge()
        assert bridge.get_sequence("") is None
        assert bridge.get_sequence(None) is None

    def test_none_for_allele_without_star(self):
        bridge = HLAToolsBridge()
        assert bridge.get_sequence("DPB1") is None

    def test_exact_match(self):
        bridge = HLAToolsBridge()
        bridge._alignment_cache["DPB1"] = {
            "DPB1*04:01:01:01": "MMVLQ",
            "DPB1*04:02:01:01": "MMVAQ",
        }
        assert bridge.get_sequence("DPB1*04:01:01:01") == "MMVLQ"

    def test_prefix_fallback(self):
        bridge = HLAToolsBridge()
        bridge._alignment_cache["DPB1"] = {
            "DPB1*04:01:01:01": "MMVLQ",
            "DPB1*04:02:01:01": "MMVAQ",
        }
        # 3-field prefix should match the 4-field allele
        assert bridge.get_sequence("DPB1*04:01:01") == "MMVLQ"

    def test_2field_prefix_fallback(self):
        bridge = HLAToolsBridge()
        bridge._alignment_cache["DPB1"] = {
            "DPB1*04:01:01:01": "MMVLQ",
        }
        assert bridge.get_sequence("DPB1*04:01") == "MMVLQ"

    def test_none_when_no_match(self):
        bridge = HLAToolsBridge()
        bridge._alignment_cache["DPB1"] = {
            "DPB1*04:01:01:01": "MMVLQ",
        }
        assert bridge.get_sequence("DPB1*99:99:99:99") is None


class TestGetPositionMapping:
    def test_invalid_locus_raises(self):
        bridge = HLAToolsBridge()
        with pytest.raises(ValueError, match="Invalid locus"):
            bridge.get_position_mapping("INVALID")

    def test_cache_hit(self):
        bridge = HLAToolsBridge()
        cached = {0: -2, 1: -1, 2: 1, 3: 2}
        bridge._position_cache["DPB1"] = cached
        assert bridge.get_position_mapping("DPB1") is cached


class TestClearCache:
    def test_clears_all_caches(self):
        bridge = HLAToolsBridge()
        bridge._alignment_cache["DPB1"] = {"allele": "seq"}
        bridge._position_cache["DPB1"] = {0: 1}

        bridge.clear_cache()

        assert bridge._alignment_cache == {}
        assert bridge._position_cache == {}


class TestValidLoci:
    @pytest.mark.parametrize(
        "locus",
        ["A", "B", "C", "DRB1", "DRB3", "DRB4", "DRB5", "DQA1", "DQB1", "DPA1", "DPB1"],
    )
    def test_all_standard_loci_valid(self, locus):
        assert locus in VALID_LOCI


class TestModuleFunctions:
    def test_get_bridge_returns_singleton(self):
        import pyard.alignment_bridge as ab

        ab._bridge_instance = None
        b1 = ab.get_bridge()
        b2 = ab.get_bridge()
        assert b1 is b2
        ab._bridge_instance = None  # cleanup

    def test_load_protein_alignment_delegates(self):
        import pyard.alignment_bridge as ab

        ab._bridge_instance = None
        mock_bridge = MagicMock()
        mock_bridge.get_alignment.return_value = {"DPB1*01:01": "MMVLQ"}
        ab._bridge_instance = mock_bridge

        result = ab.load_protein_alignment("DPB1")
        mock_bridge.get_alignment.assert_called_once_with("DPB1")
        assert result == {"DPB1*01:01": "MMVLQ"}
        ab._bridge_instance = None  # cleanup
