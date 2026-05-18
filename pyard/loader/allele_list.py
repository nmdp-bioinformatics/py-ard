import csv
import sys
from urllib.error import URLError
from urllib.request import urlopen

from ..loader import IMGT_HLA_URL
from ..simple_table import Table


def load_allele_list(imgt_version):
    """
    The format of the AlleleList file has a 6-line header with a header
    on the 7th line

    **Fields (2, semicolon-separated):**

    | # | Field    | Type   | Description        | Example         |
    |---|----------|--------|--------------------|-----------------|
    | 1 | AlleleID | String | HLA locus with `*` |                 |
    | 2 | Allele   | String | HLA locus with `*` | `A*01:01:01:05` |

    ```
    ┌──────────────────────────────┐
    │        Allelelist.txt        │
    ├────────────┬─────────────────┤
    │  AlleleID  │     Allele      │
    ├────────────┬─────────────────┤
    │  HLA00001  │  A*01:01:01:01  │
    │  HLA02169  │  A*01:01:01:02N │
    │  HLA16415  │  A*01:01:01:05  │
    └────────────┴─────────────────┘
    ```

    Returns a Table object with AlleleID and Allele columns

    :param imgt_version: IMGT database version
    :return: Table object with AlleleID and Allele data
    """

    if imgt_version == "Latest":
        allele_list_url = f"{IMGT_HLA_URL}Latest/Allelelist.txt"
    else:
        if imgt_version == "3130":
            # 3130 was renamed to 3131 for Allelelist file only 🤷🏾
            imgt_version = "3131"
        allele_list_url = (
            f"{IMGT_HLA_URL}Latest/allelelist/Allelelist.{imgt_version}.txt"
        )

    try:
        response = urlopen(allele_list_url)
        lines = [line.decode("utf-8").strip() for line in response]

        # Skip first 6 header lines
        data_lines = lines[6:]

        reader = csv.DictReader(data_lines)
        columns = ["AlleleID", "Allele"]

        return Table(reader, columns)
    except URLError as e:
        print(f"Error downloading {allele_list_url}", e, file=sys.stderr)
        sys.exit(1)
