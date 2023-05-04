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
from .blender import blender as dr_blender
from .broad_splits import find_splits as find_broad_splits
from .constants import DEFAULT_CACHE_SIZE
from .misc import get_imgt_db_versions as db_versions

__author__ = """NMDP Bioinformatics"""
__version__ = "1.0.0"


def init(
    imgt_version: str = "Latest",
    data_dir: str = None,
    load_mac: bool = True,
    cache_size: int = DEFAULT_CACHE_SIZE,
    config: dict = None,
):
    from .ard import ARD

    ard = ARD(
        imgt_version=imgt_version,
        data_dir=data_dir,
        load_mac=load_mac,
        max_cache_size=cache_size,
        config=config,
    )
    return ard
