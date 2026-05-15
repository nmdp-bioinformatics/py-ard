import sys
from urllib.error import URLError
from urllib.request import urlopen

from ..loader import IMGT_HLA_URL
from ..misc import get_2field_allele, get_3field_allele
from ..simple_table import Table


def load_p_group(imgt_version):
    """
    `hla_nom_p.txt` — P Groups (Protein-level)

    Groups alleles with identical protein sequences
    in the antigen-binding domains (exons 2+3 for Class I, exon 2 for Class II).

    **Fields (3, semicolon-separated):**

    | # | Field        | Type   | Description                                 | Example                       |
    |---|--------------|--------|---------------------------------------------|-------------------------------|
    | 1 | Locus        | String | HLA locus with `*`                          | `A*`                          |
    | 2 | Allele List  | String | `/`-separated allele names in the group     | `01:01:01:01/01:01:01:03/...` |
    | 3 | P Group Name | String | Group designation (empty if not in a group) | `01:01P`                      |

    **Key observations:**
    - Same structure as G groups but based on protein (not nucleotide) identity
    - Null alleles (`N` suffix) are excluded from P groups
    - P group names use 2-field allele designation + `P` suffix

    ```
    ┌──────────────────────────────────────────────────────────────┐
    │                       hla_nom_p.txt                          │
    ├─────────┬────────────────────────────────────┬───────────────┤
    │  Locus  │         Allele List                │  P Group Name │
    ├─────────┼────────────────────────────────────┼───────────────┤
    │ A*      │ 01:01:01:01/01:01:01:03/.../01:513 │ 01:01P        │
    │ A*      │ 01:02:01:01/01:02:01:02/01:412     │ 01:02P        │
    │ A*      │ 01:06                              │ (empty)       │
    └─────────┴────────────────────────────────────┴───────────────┘


    :param imgt_version: version of IPD/IMGT database
    :return:
    """
    ars_p_url = f"{IMGT_HLA_URL}{imgt_version}/wmda/hla_nom_p.txt"
    try:
        response = urlopen(ars_p_url)
        lines = [line.decode("utf-8").strip() for line in response]
        data_lines = lines[6:]  # Skip first 6 header lines

        data_tuples = []
        for line in data_lines:
            if line:
                fields = line.split(";")
                if len(fields) >= 3 and fields[1] and fields[2]:
                    locus, a_list, p = fields[0], fields[1], fields[2]

                    # Explode slash-delimited alleles
                    for a in a_list.split("/"):
                        full_a = locus + a
                        full_p = locus + p
                        data_tuples.append(
                            (
                                locus,
                                full_a,
                                full_p,
                                get_2field_allele(full_a),
                                get_3field_allele(full_a),
                                get_2field_allele(full_p),
                            )
                        )

        columns = ["Locus", "A", "P", "2d", "3d", "lgx"]
        return Table(data_tuples, columns)

    except URLError as e:
        print(f"Error downloading {ars_p_url}", e, file=sys.stderr)
        sys.exit(1)
