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
import pathlib
import tempfile
from typing import List

from pyard.constants import VALID_REDUCTION_TYPES, expression_chars, PandG_chars


def get_n_field_allele(allele: str, n: int, preserve_expression=False) -> str:
    """
    Given an HLA allele of >= n field, return n field allele.
    Preserve the expression character if it exists

    :param allele: Original allele
    :param n: n number of fields to reduce to
    :param preserve_expression: keep the expression character ?
    :return: trimmed to n fields of the original allele
    """
    last_char = allele[-1]
    fields = allele.split(":")
    if preserve_expression and last_char in expression_chars and len(fields) > n:
        return ":".join(fields[0:n]) + last_char
    else:
        return ":".join(fields[0:n])


def get_3field_allele(a: str) -> str:
    last_char = a[-1]
    if last_char in PandG_chars:
        a = a[:-1]

    return get_n_field_allele(a, 3)


def get_2field_allele(a: str) -> str:
    last_char = a[-1]
    if last_char in PandG_chars:
        a = a[:-1]
    return get_n_field_allele(a, 2)


def get_1field_allele(a: str) -> str:
    return get_n_field_allele(a, 1)


def number_of_fields(allele: str) -> int:
    return len(allele.split(":"))


# computes a valid G name based on the ambiguity string
def get_G_name(a: str) -> str:
    a = a.split("/")[0]
    last_char = a[-1]
    if last_char in PandG_chars + expression_chars:
        a = a[:-1]
    if len(a.split(":")) == 2:
        return ":".join([a, "01"]) + "G"
    else:
        return ":".join(a.split(":")[0:3]) + "G"


# computes a valid P name based on the ambiguity string
def get_P_name(a: str) -> str:
    a = a.split("/")[0]
    last_char = a[-1]
    if last_char in PandG_chars + expression_chars:
        a = a[:-1]
    return ":".join(a.split(":")[0:2]) + "P"


def get_imgt_db_versions() -> List[str]:
    import urllib.request
    import json

    req = urllib.request.Request(
        url="https://api.github.com/repos/ANHIG/IMGTHLA/branches?per_page=100"
    )
    res = urllib.request.urlopen(req, timeout=5)
    if res.status == 200:
        json_body = json.loads(res.read())
        versions = list(map(lambda x: x["name"], json_body))
        return versions


def download_to_file(url: str, local_filename: str):
    import urllib.request

    req = urllib.request.Request(url)
    res = urllib.request.urlopen(req, timeout=5)
    if res.status == 200:
        file_content = res.read().decode("utf-8")
        with open(local_filename, "wt") as f:
            f.write(file_content)
    else:
        print(f"Error downloading {url}")


def get_data_dir(data_dir):
    if data_dir:
        path = pathlib.Path(data_dir)
        if not path.exists() or not path.is_dir():
            raise RuntimeError(f"{data_dir} is not a valid directory")
        data_dir = path
    else:
        data_dir = get_default_db_directory()
    return data_dir


def get_imgt_version(imgt_version):
    if imgt_version:
        version = imgt_version.replace(".", "")
        if version.isdigit():
            return version
        raise RuntimeError(
            f"{imgt_version} is not a valid IMGT database version number"
        )
    return "Latest"


def get_default_db_directory():
    return pathlib.Path(tempfile.gettempdir()) / "pyard"


def validate_reduction_type(ars_type):
    if ars_type not in VALID_REDUCTION_TYPES:
        raise ValueError(f"Reduction type needs to be one of {VALID_REDUCTION_TYPES}")
