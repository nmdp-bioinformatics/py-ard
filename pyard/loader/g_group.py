import sys
from urllib.error import URLError
from urllib.request import urlopen

from ..loader import IMGT_HLA_URL
from ..misc import get_G_name, get_2field_allele, get_3field_allele
from ..simple_table import Table


def load_g_group(imgt_version):
    # load the hla_nom_g.txt
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
                    locus, a_list, g = fields[0], fields[1], fields[2]
                    g_name = get_G_name(a_list)

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
