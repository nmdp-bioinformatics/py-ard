import sys
from urllib.error import URLError
from urllib.request import urlopen

from ..loader import IMGT_HLA_URL
from ..misc import get_G_name, get_2field_allele, get_3field_allele
from ..simple_table import Table


def load_g_group(imgt_version):
    """
    `hla_nom_g.txt` — G Groups (Nucleotide-level)

    Groups alleles with identical nucleotide sequences across peptide-binding
    domain exons (exons 2+3 for Class I, exon 2 for Class II).

    **Fields (3, semicolon-separated):**

    | # | Field        | Type   | Description                                           | Example                        |
    |---|--------------|--------|-------------------------------------------------------|--------------------------------|
    | 1 | Locus        | String | HLA locus with `*`                                    | `A*`                           |
    | 2 | Allele List  | String | `/`-separated allele names in the group               | `01:01:01:01/01:01:01:02N/...` |
    | 3 | G Group Name | String | Group designation (empty if allele is not in a group) | `01:01:01G`                    |

    **Key observations:**
    - Lines with a G group name contain all member alleles in field 2
    - Lines with an empty G group name are alleles not belonging to any group
    - Allele suffixes: `N` = Null, `L` = Low expression, `Q` = Questionable

    :param imgt_version: version of IPD/IMGT database
    :return: Table of data from hla_nom_g with "Locus", "A", "G", "2d", "3d", "lgx" columns
    """
    ars_g_url = f"{IMGT_HLA_URL}{imgt_version}/wmda/hla_nom_g.txt"
    try:
        response = urlopen(ars_g_url)
        lines = [line.decode("utf-8").strip() for line in response]
        data_lines = lines[6:]  # Skip first 6 header lines

        data_tuples = []
        for line in data_lines:
            if line:
                fields = line.split(";")
                if len(fields) >= 3 and fields[1] and fields[2]:
                    locus, a_list, g_name = fields[0], fields[1], fields[2]
                    # Explode slash-delimited alleles
                    for a in a_list.split("/"):
                        full_a = locus + a
                        full_g = locus + g_name
                        data_tuples.append(
                            (
                                locus,
                                full_a,
                                full_g,
                                get_2field_allele(full_a),
                                get_3field_allele(full_a),
                                get_2field_allele(full_g),
                            )
                        )

        columns = ["Locus", "A", "G", "2d", "3d", "lgx"]
        return Table(data_tuples, columns)

    except URLError as e:
        print(f"Error downloading {ars_g_url}", e, file=sys.stderr)
        sys.exit(1)
