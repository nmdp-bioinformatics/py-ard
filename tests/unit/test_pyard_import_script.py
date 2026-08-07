# -*- coding: utf-8 -*-

import importlib.util
import pathlib
import sys
from importlib.machinery import SourceFileLoader
from unittest.mock import Mock

import pytest

SCRIPT_PATH = pathlib.Path(__file__).parents[2] / "scripts" / "pyard-import"


@pytest.fixture
def pyard_import(monkeypatch):
    """Load the extensionless `pyard-import` script as an importable module.

    `pandas` is only used to read the mapping CSV and is an optional extra,
    so it's stubbed out to keep these tests runnable without it installed.
    """
    monkeypatch.setitem(sys.modules, "pandas", Mock())
    loader = SourceFileLoader("pyard_import_script", str(SCRIPT_PATH))
    spec = importlib.util.spec_from_loader(loader.name, loader)
    module = importlib.util.module_from_spec(spec)
    loader.exec_module(module)
    return module


def test_missing_mapping_file_error_names_the_mapping_file(pyard_import, tmp_path):
    missing_file = tmp_path / "missing-mapping.csv"

    with pytest.raises(RuntimeError) as exc_info:
        pyard_import.get_v2_v3_mapping(str(missing_file))

    assert str(missing_file) in str(exc_info.value)


def test_directory_as_mapping_file_error_names_the_directory(pyard_import, tmp_path):
    with pytest.raises(RuntimeError) as exc_info:
        pyard_import.get_v2_v3_mapping(str(tmp_path))

    assert str(tmp_path) in str(exc_info.value)


def test_no_mapping_file_returns_none(pyard_import):
    assert pyard_import.get_v2_v3_mapping(None) is None
