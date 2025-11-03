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
import getpass
import pathlib
import tempfile
from typing import List

from pyard.constants import VALID_REDUCTION_MODES, expression_chars, P_and_G_chars


def get_n_field_allele(allele: str, n: int, preserve_expression=False) -> str:
    """
    Given an HLA allele of >= n field, return n field allele.
    Preserve the expression character if it exists

    :param allele: Original allele
    :param n: n number of fields to reduce to
    :param preserve_expression: keep the expression character ?
    :return: trimmed to n fields of the original allele
    """
    # Check if allele ends with expression character (N, L, S, C, A, Q)
    last_char = allele[-1]
    fields = allele.split(":")
    # Preserve expression character if requested and present, and we're reducing fields
    if preserve_expression and last_char in expression_chars and len(fields) > n:
        return ":".join(fields[0:n]) + last_char
    else:
        # Standard field reduction without expression character
        return ":".join(fields[0:n])


def get_3field_allele(a: str) -> str:
    """Reduce allele to 3 fields, removing P/G group suffixes

    Converts alleles like 'A*01:01:01:01G' to 'A*01:01:01'
    by removing P/G group indicators and reducing to 3 fields.

    Args:
        a: HLA allele string

    Returns:
        3-field allele without P/G suffixes
    """
    last_char = a[-1]
    # Remove P or G group suffixes before field reduction
    if last_char in P_and_G_chars:
        a = a[:-1]

    return get_n_field_allele(a, 3)


def get_2field_allele(a: str) -> str:
    """Reduce allele to 2 fields, removing P/G group suffixes

    Converts alleles like 'A*01:01:01:01G' to 'A*01:01'
    by removing P/G group indicators and reducing to 2 fields.

    Args:
        a: HLA allele string

    Returns:
        2-field allele without P/G suffixes
    """
    last_char = a[-1]
    # Remove P or G group suffixes before field reduction
    if last_char in P_and_G_chars:
        a = a[:-1]
    return get_n_field_allele(a, 2)


def get_1field_allele(a: str) -> str:
    """Reduce allele to 1 field (locus and allele group only)

    Converts alleles like 'A*01:01:01:01' to 'A*01'

    Args:
        a: HLA allele string

    Returns:
        1-field allele (locus*group)
    """
    return get_n_field_allele(a, 1)


def number_of_fields(allele: str) -> int:
    """Count the number of fields in an HLA allele

    Fields are separated by colons in HLA nomenclature.

    Args:
        allele: HLA allele string

    Returns:
        Number of colon-separated fields
    """
    return len(allele.split(":"))


def is_2_field_allele(allele: str) -> bool:
    """Check if allele has exactly 2 fields

    Args:
        allele: HLA allele string

    Returns:
        True if allele has exactly 2 colon-separated fields
    """
    return number_of_fields(allele) == 2


def get_G_name(a: str) -> str:
    """Compute a valid G group name from an allele or ambiguity string

    G groups represent alleles with identical exon 2 and 3 sequences.
    This function creates a standardized G group name by taking the first
    allele from ambiguous strings and formatting it appropriately.

    Args:
        a: Allele or ambiguous allele string

    Returns:
        Standardized G group name with 'G' suffix
    """
    # Take first allele if ambiguous (contains '/')
    a = a.split("/")[0]
    last_char = a[-1]
    # Remove existing P/G group or expression suffixes
    if last_char in P_and_G_chars + expression_chars:
        a = a[:-1]
    # For 2-field alleles, add '01' as third field before 'G' suffix
    if len(a.split(":")) == 2:
        return ":".join([a, "01"]) + "G"
    else:
        # For 3+ field alleles, use first 3 fields with 'G' suffix
        return ":".join(a.split(":")[0:3]) + "G"


def get_P_name(a: str) -> str:
    """Compute a valid P group name from an allele or ambiguity string

    P groups represent alleles with identical protein sequences.
    This function creates a standardized P group name using the first
    two fields of the allele.

    Args:
        a: Allele or ambiguous allele string

    Returns:
        Standardized P group name with 'P' suffix
    """
    # Take first allele if ambiguous (contains '/')
    a = a.split("/")[0]
    last_char = a[-1]
    # Remove existing P/G group or expression suffixes
    if last_char in P_and_G_chars + expression_chars:
        a = a[:-1]
    # Use first 2 fields with 'P' suffix
    return ":".join(a.split(":")[0:2]) + "P"


def get_imgt_db_versions() -> List[str]:
    """Fetch available IPD-IMGT/HLA database versions from GitHub

    Queries the ANHIG/IMGTHLA repository to get all available branch names,
    which correspond to different database versions.

    Returns:
        List of available database version names

    Raises:
        Network errors if GitHub API is unreachable
    """
    import urllib.request
    import json

    # Query GitHub API for IMGT/HLA repository branches
    req = urllib.request.Request(
        url="https://api.github.com/repos/ANHIG/IMGTHLA/branches?per_page=100"
    )
    res = urllib.request.urlopen(req, timeout=5)
    if res.status == 200:
        json_body = json.loads(res.read())
        # Extract branch names as version identifiers
        versions = list(map(lambda x: x["name"], json_body))
        return versions


def download_to_file(url: str, local_filename: str):
    """Download content from URL and save to local file

    Downloads text content from a URL and writes it to a local file.
    Used for fetching IMGT/HLA database files and other resources.

    Args:
        url: URL to download from
        local_filename: Local file path to save content

    Prints error message if download fails
    """
    import urllib.request

    req = urllib.request.Request(url)
    res = urllib.request.urlopen(req, timeout=5)
    if res.status == 200:
        # Decode content as UTF-8 text and write to file
        file_content = res.read().decode("utf-8")
        with open(local_filename, "wt") as f:
            f.write(file_content)
    else:
        print(f"Error downloading {url}")


def get_data_dir(data_dir):
    """Validate and return data directory path

    Validates the provided data directory or returns the default directory
    if none is specified. Ensures the directory exists and is accessible.

    Args:
        data_dir: User-specified data directory path or None

    Returns:
        Validated pathlib.Path object for data directory

    Raises:
        RuntimeError: If specified directory doesn't exist or isn't a directory
    """
    if data_dir:
        path = pathlib.Path(data_dir)
        # Validate that the specified path exists and is a directory
        if not path.exists() or not path.is_dir():
            raise RuntimeError(f"{data_dir} is not a valid directory")
        data_dir = path
    else:
        # Use default directory if none specified
        data_dir = get_default_db_directory()
    return data_dir


def get_imgt_version(imgt_version):
    """Validate and normalize IMGT database version

    Converts version strings like '3.51.0' to '3510' format used internally.
    Returns 'Latest' if no version is specified.

    Args:
        imgt_version: Version string (e.g., '3.51.0') or None

    Returns:
        Normalized version string ('3510') or 'Latest'

    Raises:
        RuntimeError: If version format is invalid
    """
    if imgt_version:
        # Remove dots and validate that result is numeric
        version = imgt_version.replace(".", "")
        if version.isdigit():
            return version
        raise RuntimeError(
            f"{imgt_version} is not a valid IMGT database version number"
        )
    return "Latest"


def get_default_db_directory():
    """Get the default directory for py-ard database files

    Creates a user-specific directory in the system temp directory
    for storing SQLite database files and cached data.

    Returns:
        pathlib.Path object for default database directory
    """
    try:
        # Get current username for directory naming
        username = getpass.getuser()
    except OSError:
        # Fallback if username cannot be determined
        username = "nonuser"
    # Create path in system temp directory with user-specific name
    return pathlib.Path(tempfile.gettempdir()) / f"pyard-{username}"


def validate_reduction_type(ars_type):
    """Validate that reduction type is supported

    Checks that the provided reduction type is one of the valid options
    supported by py-ard (G, P, lg, lgx, W, exon, U2, S).

    Args:
        ars_type: Reduction type string to validate

    Raises:
        ValueError: If reduction type is not supported
    """
    if ars_type not in VALID_REDUCTION_MODES:
        raise ValueError(f"Reduction type needs to be one of {VALID_REDUCTION_MODES}")
