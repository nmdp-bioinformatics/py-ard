import sys
from urllib.error import URLError
from urllib.request import urlopen

from ..loader import IMGT_HLA_URL
from ..misc import get_G_name, get_2field_allele, get_3field_allele
from ..simple_table import Table


def load_g_group(imgt_version):
    """
    load the hla_nom_g.txt
    Sample file:
    # file: hla_nom_g.txt
    # date: 2025-10-08
    # version: IPD-IMGT/HLA 3.62.0
    # origin: http://hla.alleles.org/wmda/hla_nom_g.txt
    # repository: https://raw.githubusercontent.com/ANHIG/IMGTHLA/Latest/wmda/hla_nom_g.txt
    # author: IPD Team (ipdsubs@anthonynolan.org)
    A*;01:01:01:01/01:01:01:02N/01:01:01:03/ ... /01:481;01:01:01G
    A*;01:01:02;
    A*;01:01:03;
    A*;01:01:04;
    A*;01:01:05;
    A*;01:01:06;
    A*;01:01:07;
    A*;01:01:08;
    A*;01:01:09;
    A*;01:01:10;
    A*;01:01:11;
    A*;01:01:12;
    A*;01:01:13;
    A*;01:01:14;
    A*;01:01:15;
    A*;01:01:16;
    ...
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
