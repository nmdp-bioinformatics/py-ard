# Extras

# Batch Script for CSV File

**Example Scripts to batch reduce HLA typings from a CSV File**

`reduce_csv.py` and `conf.py` scripts can be used to take a CSV file with HLA 
typing data and reduce certain columns and produce a new CSV and Excel file.

For most use case, installing `py-ard`, specifying the changes in `conf.py` file
and running `python reduce_csv.py` will produce result based on the configuration
in the `conf.py`.


```python
#
# configurations for processing CSV files
#

# The column names that are in CSV
# The output file will have these columns
all_columns_in_csv = [
    "nmdp_id", "r_a_typ1", "r_a_typ2", "r_b_typ1", "r_b_typ2", "r_c_typ1", "r_c_typ2", "r_drb1_typ1", "r_drb1_typ2",
    "r_dpb1_typ1", "r_dpb1_typ2"
]

#
# List of columns which have typing information and need to be reduced.
# The locus is the 2nd term in the column name
# Eg: For column R_DRB1_type1, DPB1 is the locus name
#
columns_to_reduce_in_csv = [
    "r_a_typ1", "r_a_typ2", "r_b_typ1", "r_b_typ2", "r_c_typ1", "r_c_typ2", "r_drb1_typ1", "r_drb1_typ2", "r_dpb1_typ1",
    "r_dpb1_typ2"
]

#
# Configuration options to ARD reduction of a CSV file
#
ard_config = {
    # All Columns in the CSV file
    "csv_in_column_names": all_columns_in_csv,

    # Columns to check for typings
    "columns_to_check": columns_to_reduce_in_csv,

    # How should the typings be reduced
    # Valid Options:
    # - G
    # - lg
    # - lgx
    "redux_type": "lgx",

    # Input CSV filename
    "in_csv_filename": "sample.csv",

    # Output CSV filename
    "out_csv_filename": 'clean_sample.csv',

    # Use compression
    # Valid options
    # - 'gzip'
    # - 'zip'
    # - None
    "apply_compression": 'gzip',

    # Show verbose log
    # Valid options:
    # - True
    # - False
    "verbose_log": True,

    # What to reduce ?
    "reduce_serology": False,
    "reduce_v2": True,
    "reduce_3field": True,
    "reduce_P": True,
    "reduce_XX": False,
    "reduce_MAC": True,

    # Is locus name present in allele
    # Eg. A*01:01 vs 01:01
    "locus_in_allele_name": False,

    # Format
    # Valid options:
    # - csv
    # - xlsx
    "output_file_format": 'csv',

    # Add a separate column for processed column
    "new_column_for_redux": False,
}
```

The included sample CSV file `sample.csv` can be processed using the script.

```shell

```
