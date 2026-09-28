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
#
#  Quick script to reduce alleles from a CSV file
#
#  Use configuration file from `--config` to setup configurations that's used here
#  For Excel output, openpyxl library needs to be installed.
#       pip install openpyxl
#
from __future__ import annotations

import argparse
import json
import pprint
import re
import sys
from typing import Any
from urllib.error import HTTPError

import pandas as pd

import pyard
from pyard import drbx
from pyard.ard import ARD
from pyard.db import similar_alleles
from pyard.exceptions import InvalidAlleleError, InvalidTypingError, PyArdError
from pyard.misc import download_to_file, get_data_dir, get_imgt_version

# Module-level state shared with the reduction helper functions below.
# These are initialized in main() before the helpers are invoked.
ard = None
ard_config = None
verbose = False
error_file = sys.stderr
log_file = sys.stdout
failed_to_reduce_alleles = []
white_space_regex = re.compile(r"\s+")


def is_serology(allele: str) -> bool:
    return ard.is_serology(allele)


def is_3field(allele: str) -> bool:
    return len(allele.split(":")) > 2


def is_2field(allele: str) -> bool:
    if "*" in allele:
        allele = allele.split("*")[1]
    fields = allele.split(":")
    # Check to see the 2 fields are digits to distinguish from MAC.
    return len(fields) == 2 and fields[0].isdigit() and fields[1].isdigit()


def is_P(allele: str) -> bool:
    if allele.endswith("P"):
        fields = allele.split(":")
        if len(fields) == 2:  # Ps are 2 fields
            # Check both fields are digits only
            # Eg: A*02:01P
            # Check last 2 digits of first field: 02 is numeric
            # Check digits of seconds field: 01 is numeric
            return fields[0][-2:].isdigit() and fields[1][:-1].isdigit()
    return False


def should_be_reduced(allele, locus_allele):
    if is_serology(allele):
        return ard_config["reduce_serology"]

    if ard_config["reduce_v2"] and ard.is_v2(locus_allele):
        return True

    if ard_config["reduce_2field"] and is_2field(locus_allele):
        return True

    if ard_config["reduce_3field"] and is_3field(locus_allele):
        return True

    if ard_config["reduce_P"] and is_P(allele):
        return True

    if ard_config["reduce_XX"] and ard.is_XX(locus_allele):
        return True

    if ard_config["reduce_MAC"]:  # noqa: SIM102
        if ard.is_mac(locus_allele) and not ard.is_XX(locus_allele):
            return True

    return False


def remove_locus_name(reduced_allele):
    return "/".join(a.split("*")[1] for a in reduced_allele.split("/"))


def redux(allele, locus, column_name):
    # Does the allele name have the locus in it ?
    if allele == "":
        return allele
    if "*" in allele or ard_config.get("locus_in_allele_name"):
        locus_allele = allele
    else:
        if allele.startswith(locus):
            locus_allele = allele
        else:
            if ":" in allele:
                locus_allele = f"{locus}*{allele}"
            else:
                if allele.isnumeric():
                    # Serology alleles are all numeric
                    locus_allele = f"{locus}{allele}"  # serology
                else:
                    # Watch out, we may get floats when exported from Excel.
                    message = f"Failed reducing '{allele}' in column {column_name}"
                    print(message, file=error_file)
                    failed_to_reduce_alleles.append((column_name, allele))
                    return allele

    # Check the config if this allele should be reduced
    if should_be_reduced(allele, locus_allele):
        # print(f"reducing '{locus_allele}'")
        try:
            reduced_allele = ard.redux(locus_allele, ard_config["redux_type"])
        except PyArdError as e:
            if verbose:
                print(e.message, file=error_file)
            message = f"Failed reducing '{locus_allele}' in column {column_name}"
            print(message, file=log_file)
            print(message, file=log_file)
            failed_to_reduce_alleles.append((column_name, locus_allele))
            return allele
        # print(f"reduced to '{reduced_allele}'")
        if reduced_allele:
            if ard_config.get("keep_locus_in_allele_name"):
                allele = reduced_allele
            else:
                allele = remove_locus_name(reduced_allele)
        else:
            if verbose:
                print(f"Failed to reduce {locus_allele}", file=log_file)
        if verbose:
            print(f"\t{locus_allele} => {allele}", file=log_file)
    else:
        if ard_config.get("convert_v2_to_v3"):
            if ard.is_v2(locus_allele):
                v3_allele = ard.v2_to_v3(locus_allele)
                if not ard_config.get("keep_locus_in_allele_name"):
                    allele = remove_locus_name(v3_allele)
                else:
                    allele = v3_allele
                if verbose:
                    print(f"\t{locus_allele} => {allele}", file=log_file)
        elif ard_config.get("keep_locus_in_allele_name"):
            allele = locus_allele

    return allele


def clean_locus(allele: str, locus: str, column_name: str = "Unknown") -> str:
    if allele:
        # Remove all white spaces
        allele = white_space_regex.sub("", allele)
        # If the allele comes in as an allele list, apply reduce to all alleles
        if "/" in allele:
            return "/".join([redux(a, locus, column_name) for a in allele.split("/")])
        else:
            return redux(allele, locus, column_name)
    return allele


def create_drbx(row, locus_in_allele_name):
    return drbx.map_drbx(row.values, locus_in_allele_name)


def reduce_locus_columns(df, ard_config, locus_column_mapping, verbose):
    reduce_prefix = ard_config.get("reduced_column_prefix", "reduced_")
    for subject in locus_column_mapping:
        for locus in locus_column_mapping[subject]:
            # Reduce each of the specified columns
            locus_columns = locus_column_mapping[subject][locus]
            for column in locus_columns:
                if verbose:
                    print(f"Column:{column} =>", file=log_file)
                if ard_config.get("new_column_for_redux"):
                    # insert a new column
                    new_column_name = f"{reduce_prefix}{column}"
                    new_column_index = df.columns.get_loc(column) + 1
                    # Apply clean_locus function to the column and insert as a new column
                    df.insert(
                        new_column_index,
                        new_column_name,
                        df[column].apply(
                            clean_locus, locus=locus.upper(), column_name=column
                        ),
                    )
                    locus_columns[locus_columns.index(column)] = new_column_name
                else:
                    # Apply clean_locus function to the column and replace the column
                    df[column] = df[column].apply(
                        clean_locus, locus=locus, column_name=column
                    )
    # Map DRB3,DRB4,DRB5 to DRBX if specified
    # New columns DRBX_1 and DRBX_2 are created
    if ard_config.get("map_drb345_to_drbx"):
        drbx_loci = ["DRB3", "DRB4", "DRB5"]
        for subject in ard_config["locus_column_mapping"]:
            subject_loci = ard_config["locus_column_mapping"][subject]
            subject_drbs = []
            for locus in ard_config["locus_column_mapping"][subject]:
                if locus.upper() in drbx_loci:
                    subject_drbs.extend(subject_loci[locus])

            # If all the DRBs are there
            # ['DRB3_1', 'DRB3_2', 'DRB4_1', 'DRB4_2', 'DRB5_1', 'DRB5_2']
            if len(subject_drbs) == 6:
                locus_in_allele_name = ard_config["keep_locus_in_allele_name"]
                df_drbx = df[subject_drbs].apply(
                    create_drbx, axis=1, args=(locus_in_allele_name,)
                )
                df[f"{subject}_DRBX_1"], df[f"{subject}_DRBX_2"] = zip(*df_drbx)

    if ard_config.get("generate_glstring", False) or ard_config.get(
        "generate_slugs", False
    ):
        for subject in locus_column_mapping:
            subject_loci_columns = locus_column_mapping[subject]
            slug_columns = []
            for locus in subject_loci_columns:
                slug_column = f"{subject}_{locus}_slug"
                slug_columns.append(slug_column)
                locus_typ_pair = subject_loci_columns[locus]
                if len(locus_typ_pair) > 1:
                    df[slug_column] = df[locus_typ_pair].apply(
                        create_reduced_slug, axis=1
                    )
                else:
                    df[slug_column] = df[subject_loci_columns[locus][0]]

                if ard_config.get("suppress_reduced_locus_column"):
                    df.drop(columns=locus_typ_pair, inplace=True)

            if ard_config.get("generate_glstring"):
                df[subject + "_gl"] = df[slug_columns].agg(
                    lambda slugs: "^".join(slug for slug in slugs if slug), axis=1
                )
            if not ard_config.get("generate_slugs"):
                df.drop(columns=slug_columns, inplace=True)


def create_reduced_slug(locus_typ1_typ2_pair):
    typ1 = locus_typ1_typ2_pair.iloc[0]
    typ2 = locus_typ1_typ2_pair.iloc[1]

    if not typ1 and not typ2:
        return ""

    if typ1 and typ2:
        return typ1 + "+" + typ2
    elif ard_config.get("homozygosify_glstring"):
        if typ1:
            return typ1 + "+" + typ1
        if typ2:
            return typ2 + "+" + typ2
    else:
        if typ2:
            return typ2
    return typ1


def apply_drbx(gl_string):
    slugs = gl_string.split("^")
    alleles = [allele for slug in slugs for allele in slug.split("+")]
    drbx_loci = ("DRB3", "DRB4", "DRB5")

    # Filter for DRBX alleles
    drbx_alleles = [
        allele
        for allele in alleles
        if any(allele.startswith(locus) for locus in drbx_loci)
    ]

    # Create new GL string without DRBX alleles
    filtered_slugs = []
    for slug in slugs:
        non_drbx_alleles = []
        for allele in slug.split("+"):
            if not any(allele.startswith(locus) for locus in drbx_loci):
                non_drbx_alleles.append(allele)
        if non_drbx_alleles:
            filtered_slugs.append("+".join(non_drbx_alleles))

    new_gl_string = "^".join(filtered_slugs)

    drbx_slug = drbx.map_drbx(drbx_alleles, True)
    gl_string_drbx = new_gl_string + "^" + "+".join(drbx_slug)

    return gl_string_drbx


def reduce_glstring(glstring: str) -> str:
    try:
        if not glstring:
            print("Missing glstring", file=error_file)
            return ""
        ard_redux = ard.redux(glstring, ard_config["redux_type"])
        if ard_config.get("map_drb345_to_drbx"):
            glstring_drbx = apply_drbx(ard_redux)
            return glstring_drbx
        else:
            return ard_redux
    except (InvalidTypingError, InvalidAlleleError) as e:
        print(f"Error reducing {glstring} \n", e.message, file=error_file)
        return "Failed"


def reduce_glstring_columns(df, ard_config, glstring_columns):
    reduce_prefix = ard_config.get("reduced_column_prefix", "reduced_")
    for column in glstring_columns:
        if ard_config.get("new_column_for_redux"):
            # insert a new column
            new_column_name = f"{reduce_prefix}{column}"
            new_column_index = df.columns.get_loc(column) + 1
            # Apply clean_locus function to the column and insert as a new column
            df.insert(
                new_column_index, new_column_name, df[column].apply(reduce_glstring)
            )
        else:
            # Apply clean_locus function to the column and replace the column
            df[column] = df[column].apply(reduce_glstring)


def reduce_and_save(
    ard: ARD, ard_config, in_csv_filename, out_csv_filename, verbose: bool | Any
):
    global failed_to_reduce_alleles
    # Read the Input File
    # Read only the columns to be saved.
    # Header is the first row
    # Don't convert to NAs
    columns_from_csv = ard_config["columns_from_csv"]
    try:
        df = pd.read_csv(
            in_csv_filename,
            usecols=columns_from_csv,
            header=0,
            dtype=str,
            keep_default_na=False,
        )[columns_from_csv]
    except FileNotFoundError as e:
        print(
            f"File not found {in_csv_filename}. Error: {e}",
            file=error_file,
        )
        sys.exit(1)

    failed_to_reduce_alleles = []
    locus_column_mapping = ard_config.get("locus_column_mapping", None)
    if locus_column_mapping:
        reduce_locus_columns(df, ard_config, locus_column_mapping, verbose)

    glstring_columns = ard_config.get("glstring_columns", None)
    if glstring_columns:
        reduce_glstring_columns(df, ard_config, glstring_columns)

    # Save as XLSX if specified
    if ard_config["output_file_format"] == "xlsx":
        out_csv_filename = f"{ard_config['out_csv_filename']}.xlsx"
        df.to_excel(out_csv_filename, index=False)
    else:
        # Save as compressed CSV if specified
        compression_type = ard_config["apply_compression"]
        # Valid compression_type: gzip, zip, null
        if compression_type == "gzip":
            out_csv_filename = out_csv_filename + ".gz"
        elif compression_type == "zip":
            out_csv_filename = out_csv_filename + ".zip"

        df.to_csv(
            out_csv_filename,
            index=False,
            compression=compression_type,
            header=True,
        )

    if len(failed_to_reduce_alleles) == 0:
        print("No Errors", file=error_file)
    else:
        print("Summary", file=log_file)
        print("-------", file=log_file)
        print(
            f"{len(failed_to_reduce_alleles)} alleles failed to reduce.",
            file=log_file,
        )
        print(
            "| Column  Name    |      Allele      |      Did you mean ?       ",
            file=log_file,
        )
        print(
            "| --------------- | ---------------- | ------------------------- ",
            file=log_file,
        )
        for column_name, locus_allele in failed_to_reduce_alleles:
            similar_allele_names = similar_alleles(ard.db_connection, locus_allele)
            if similar_allele_names:
                similar_allele_names = ",".join(
                    sorted(similar_allele_names, reverse=True)
                )
            else:
                similar_allele_names = "NA"
            print(
                f"| {column_name:15} | {locus_allele:16} | {similar_allele_names} ",
                file=log_file,
            )
    # Done
    print(f"Saved result to file: {out_csv_filename}")
    if log_file is not sys.stdout:
        print(f"Saved log to file: {log_file.name}")
    if error_file is not sys.stderr:
        print(f"Saved errors to file: {error_file.name}")


def get_redux_config(ard_config) -> dict[str | Any, Any]:
    csv_redux_config = {
        "reduce_serology": ard_config.get("reduce_serology", True),
        "reduce_v2": ard_config.get("reduce_v2", True),
        "reduce_3field": ard_config.get("reduce_3field", True),
        "reduce_P": ard_config.get("reduce_P", True),
        "reduce_XX": ard_config.get("reduce_XX", True),
        "reduce_MAC": ard_config.get("reduce_MAC", True),
        "reduce_shortnull": ard_config.get("reduce_shortnull", True),
        "ping": ard_config.get("ping", True),
        "verbose_log": ard_config.get("verbose_log", True),
        "ARS_as_lg": ard_config.get("ARS_as_lg", False),
        "strict": ard_config.get("strict", True),
        "ignore_allele_with_suffixes": tuple(
            ard_config.get("ignore_allele_with_suffixes", "").split(",")
        ),
    }
    pprint.pprint(csv_redux_config, indent=4, stream=log_file)
    return csv_redux_config


def main():
    global ard, ard_config, verbose

    # config is specified with a -c parameter
    parser = argparse.ArgumentParser()
    parser.add_argument("-c", "--config", help="JSON Configuration file")
    parser.add_argument(
        "-d",
        "--data-dir",
        dest="data_dir",
        help="Data directory to store imported data",
    )
    parser.add_argument(
        "-i",
        "--ipd-version",
        dest="ipd_version",
        help="IPD-IMGT/HLA db to use for redux",
    )
    parser.add_argument(
        "-q",
        "--quiet",
        dest="quiet",
        action="store_true",
        default=False,
        help="Don't print verbose log",
    )
    parser.add_argument(
        "-g",
        "--generate-sample",
        dest="generate",
        action="store_true",
        default=False,
        help="Generate sample config file and csv file",
    )

    args = parser.parse_args()

    if args.generate:
        sample_files = [
            "reduce_conf.json",
            "sample.csv",
            "reduce_conf_glstring.json",
            "sample_glstring.csv",
        ]
        for sample_file in sample_files:
            try:
                url = f"https://raw.githubusercontent.com/nmdp-bioinformatics/py-ard/master/extras/{sample_file}"
                download_to_file(url, sample_file)
                print(f"Created {sample_file}", file=log_file)
            except HTTPError:
                print(f"Download failed for {sample_file}", file=error_file)
        sys.exit(0)

    config_filename = args.config
    if not config_filename:
        print("Config file required. Specify with -c/--config", file=error_file)
        sys.exit(1)

    print("Using config file:", config_filename, file=log_file)
    with open(config_filename) as conf_file:
        ard_config = json.load(conf_file)

    if not args.quiet:
        verbose = ard_config.get("verbose_log")
    else:
        verbose = False

    if ard_config.get("output_file_format") == "xlsx":
        from importlib import util

        excel_support_available = util.find_spec("openpyxl")
        if not excel_support_available:
            print(
                "For Excel output, openpyxl library needs to be installed. "
                "Install with:",
                file=error_file,
            )
            print("  pip install openpyxl", file=error_file)
            sys.exit(1)

    data_dir = get_data_dir(args.data_dir)
    imgt_version = get_imgt_version(args.ipd_version)
    max_cache_size = ard_config.get("redux_cache_size", pyard.DEFAULT_CACHE_SIZE)
    csv_redux_config = get_redux_config(ard_config)
    ard = pyard.init(
        imgt_version=imgt_version,
        data_dir=data_dir,
        cache_size=max_cache_size,
        config=csv_redux_config,
    )

    in_csv_filename = ard_config["in_csv_filename"]
    out_csv_filename = ard_config["out_csv_filename"]

    reduce_and_save(ard, ard_config, in_csv_filename, out_csv_filename, verbose)


if __name__ == "__main__":
    main()
