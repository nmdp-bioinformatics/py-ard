#
#
#  Quick script to reduce alleles from a CSV file
#
#  Use `conf.py` to setup configurations that's used here
#  For Excel output, openpyxl library needs to be installed.
#       pip install openpyxl
#

import pandas as pd
import pyard
import re

from conf import ard_config

verbose = ard_config["verbose_log"]
white_space_regex = re.compile(r"\s+")


def is_serology(allele: str) -> bool:
    if len(allele.split(':')) == 1:
        return True


def is_3field(allele: str) -> bool:
    return len(allele.split(':')) > 2


def is_P(allele: str) -> bool:
    if allele.endswith('P'):
        fields = allele.split(':')
        if len(fields) == 2:  # Ps are 2 fields
            return fields[0].isdigit() and fields[0].isdigit()
    return False


def clean_locus(allele: str, column_name: str = 'Unknown') -> str:
    if allele:
        # Remove all white spaces
        allele = white_space_regex.sub('', allele)
        locus = column_name.split('_')[1].upper()
        # If the allele comes in as an allele list, apply reduce to all alleles
        if '/' in allele:
            return "/".join(map(reduce, allele.split('/'), locus))
        else:
            return reduce(allele, locus)
    return allele


def should_be_reduced(allele, locus_allele):
    if is_serology(allele):
        return ard_config["reduce_serology"]

    if ard_config["reduce_v2"]:
        if ard.is_v2(locus_allele):
            return True

    if ard_config["reduce_3field"]:
        if is_3field(locus_allele):
            return True

    if ard_config["reduce_P"]:
        if is_P(allele):
            return True

    if ard_config["reduce_XX"]:
        if ard.is_XX(locus_allele):
            return True

    if ard_config["reduce_MAC"]:
        if ard.is_mac(locus_allele) and not ard.is_XX(locus_allele):
            return True

    return False


def reduce(allele, locus):
    # Does the allele name have the locus in it ?
    if '*' in allele:
        locus_allele = allele
    elif ard_config["locus_in_allele_name"]:
        locus_allele = allele
    else:
        locus_allele = f"{locus}*{allele}"

    # Check the config if this allele should be reduced
    if should_be_reduced(allele, locus_allele):
        # print(f"reducing '{locus_allele}'")
        reduced_allele = ard.redux_gl(locus_allele, ard_config["redux_type"])
        # print(f"reduced to '{reduced_allele}'")
        if reduced_allele:
            allele = "/".join(map(lambda a: a.split('*')[1],
                                  reduced_allele.split('/')))
        else:
            if verbose:
                print(f"Failed to reduce {locus_allele}")

        if verbose:
            print(f"\t{locus_allele} => {allele}")
    return allele


if __name__ == '__main__':
    ard = pyard.ARD(remove_invalid=False)

    df = pd.read_csv(ard_config["in_csv_filename"], names=ard_config["csv_in_column_names"], header=0, dtype=str)
    df.fillna('', inplace=True)

    for column in ard_config["columns_to_check"]:
        if verbose:
            print(f"Column:{column} =>")
        if ard_config["new_column_for_redux"]:
            # insert a new column
            new_column_name = f"reduced_{column}"
            new_column_index = df.columns.get_loc(column) + 1
            df.insert(new_column_index, new_column_name, df[column].apply(clean_locus, column_name=column))
        else:
            df[column] = df[column].apply(clean_locus, column_name=column)

    if ard_config["output_file_format"] == 'xlsx':
        out_file_name = f"{ard_config['out_csv_filename']}.xlsx"
        df.to_excel(out_file_name, index=False)
    else:
        out_file_name = f"{ard_config['out_csv_filename'] + '.gz' if ard_config['apply_compression'] else ''}"
        df.to_csv(out_file_name, index=False, compression=ard_config["apply_compression"])
    if verbose:
        print(f"Saved result to file:{out_file_name}")
