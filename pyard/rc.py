# -*- coding: utf-8 -*-

import os
from pathlib import Path

RC_FILENAME = ".pyardrc"

_RC_SEARCH_PATHS = [
    Path.cwd(),
    Path.home(),
]


def _find_rc_file() -> Path | None:
    for directory in _RC_SEARCH_PATHS:
        rc = directory / RC_FILENAME
        if rc.exists():
            return rc
    return None


def load_rc() -> dict:
    """Load .pyardrc and return kwargs suitable for pyard.init()"""
    rc_file = _find_rc_file()
    if rc_file is None:
        return {}

    try:
        import tomllib

        with open(rc_file, "rb") as f:
            data = tomllib.load(f)
    except ImportError:
        import toml  # Python < 3.11

        data = toml.load(rc_file)

    pyard_section = data.get("pyard", {})
    config_section = pyard_section.pop("config", None)

    kwargs = dict(pyard_section)
    if config_section is not None:
        # Convert list to tuple for ignore_allele_with_suffixes
        if "ignore_allele_with_suffixes" in config_section:
            config_section["ignore_allele_with_suffixes"] = tuple(
                config_section["ignore_allele_with_suffixes"]
            )
        kwargs["config"] = config_section

    print(f"-- Loading config from {rc_file}")
    return kwargs
