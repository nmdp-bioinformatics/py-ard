import csv
import os


def load_cwd2():
    cwd_csv_path = os.path.join(os.path.dirname(__file__), "CWD2.csv")
    cwd_map = {}

    with open(cwd_csv_path, "r") as file:
        reader = csv.DictReader(file)
        for row in reader:
            cwd_map[row["ALLELE"]] = row["LOCUS"]

    return cwd_map
