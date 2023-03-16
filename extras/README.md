# Extras

# Script to batch process a CSV File

**Example Scripts to batch reduce HLA typings from a CSV File**

`pyard-reduce-csv` command can be used with a config file(that describes ways to reduce the file) to take a
CSV file with HLA typing data and reduce certain columns and produce a new CSV or an Excel file.

Steps on batch processing a CSV file.

1. [Install `py-ard`](../README.md#installation)
2. Specify the configuration on how the file should be processed in a JSON `.json` config file.
3. Run `pyard-reduce-csv -c <config-file>` to produce a processed file based on the configuration in the config file.

To help with creating configuration file, you can use `-g` or `--generate-sample` option to `pyard-reduce-csv` and
generate a sample configuration and a sample CSV file.

These files should be used as a template for your own data.

Once the configuration file is created, use `-c` option to specify the configuration file to be used for batch
processing.

In the following example, we generate a sample configuration and CSV file.

```shell
$ pyard-reduce-csv --generate-sample
Created sample_reduce_conf.json
Created sample.csv
```

We specify the config file with `-c` and a `-q` to suppress verbose log messages.
```shell
$ pyard-reduce-csv -c sample_reduce_conf.json -q
Using config file: reduce_conf.json
Failed reducing 'C*02:85:02' in column r_c_typ2
Failed reducing 'DRB1*14:167:01' in column r_drb1_typ2
...

Summary
-------
16 alleles failed to reduce.
| Column  Name    |      Allele      |      Did you mean ?
| --------------- | ---------------- | -------------------------
| r_c_typ2        | C*02:85:02       | NA
| r_drb1_typ2     | DRB1*14:167:01   | NA
...

Saved result to file:clean_sample.csv.gz
```

See [Example JSON config file](reduce_conf.json).

# Configuration Options

The configuration file provides the following options to modify how the reduction happens.

| Configuration Option        | Type | Description                                                         |
|-----------------------------|------|---------------------------------------------------------------------|
| `in_csv_filename`           | str  | [Input CSV filename](#input-csv-filename)                           |
| `out_csv_filename`          | str  | [Output CSV filename](#output-csv-filename)                         |
| `columns_from_csv`          | list | [CSV Columns to read](#csv-columns-to-read)                         |
| `locus_column_mapping`      | dict | [CSV Columns to reduce](#csv-columns-to-reduce)                     |
| `redux_type`                | str  | [Reduction Type](#redux-options)                                    |
| `redux_cache_size`          | int  | [Cache size](#cache-size)                                           |
| `reduce_serology`           | bool | [Reduce Serology ?](#kinds-of-typings-to-reduce)                    |
| `reduce_v2`                 | bool | [Reduce V2 formatted alleles ?](#kinds-of-typings-to-reduce)        |
| `convert_v2_to_v3`          | bool | [Convert V2 format to V3 ?](#kinds-of-typings-to-reduce)            |
| `reduce_2field`             | bool | [Reduced alleles that are 2 field ?](#kinds-of-typings-to-reduce)   |
| `reduce_3field`             | bool | [Reduced alleles that are 3 field ?](#kinds-of-typings-to-reduce)   |
| `reduce_P`                  | bool | [Reduced alleles that have P suffix ?](#kinds-of-typings-to-reduce) |
| `reduce_XX`                 | bool | [Reduced XX Alleles ?](#kinds-of-typings-to-reduce)                 |
| `reduce_MAC`                | bool | [Reduced MAC Alleles ?](#kinds-of-typings-to-reduce)                |
| `map_drb345_to_drbx`        | bool | [Map DRB3,4,5 to DRBX using WMDA Rules ?](#map-to-drbx)             |
| `locus_in_allele_name`      | bool | [Is Locus name specified for each allele ?](#locus-name-in-allele)  |
| `keep_locus_in_allele_name` | bool | [Output Locus name for each allele ?](#keep-locus-name-in-allele)   |
| `new_column_for_redux`      | bool | [Create a new column or replace the original ?](#create-new-column) |
| `reduced_column_prefix`     | str  | [Prefix to use for reduced column](#create-new-column)              |
| `generate_glstring`         | bool | [Generate a GL String column for each subject ?](#gl-string)        |
| `output_file_format`        | str  | [Format of the output file](#output-format)                         |
| `apply_compression`         | str  | [Compression format for the output file](#compression-options)      |
| `verbose_log`               | bool | [Output verbose log to the screen ?](#verbose-log-options)          |

### Input CSV filename

`in_csv_filename` Directory path and file name of the Input CSV file

### Output CSV filename

`out_csv_filename` Directory path and file name of the Reduced Output CSV file

### CSV Columns to read

`columns_from_csv` The column names to read from CSV file

```json
 [
  "nmdp_id",
  "r_a_typ1",
  "r_a_typ2",
  "r_b_typ1",
  "r_b_typ2",
  "r_c_typ1",
  "r_c_typ2",
  "d_a_typ1",
  "d_a_typ2",
  "d_b_typ1",
  "d_b_typ2",
  "d_c_typ1",
  "d_c_typ2"
]
```

### CSV Columns to reduce

`locus_column_mapping` Mapping of subject types (eg. Recipient, Donor) to their loci and the corresponding columns with
typings for those loci.
The column names corresponding to the loci will be reduced and must appear in the list of `columns_from_csv`.

```json
  "locus_column_mapping": {
    "recipient": {
        "A": [
            "r_a_typ1",
            "r_a_typ2"
        ],
        "B": [
            "r_b_typ1",
            "r_b_typ2"
        ],
        "C": [
            "r_c_typ1",
            "r_c_typ2"
        ]
    },
    "donor": {
        "A": [
            "d_a_typ1",
            "d_a_typ2"
        ],
        "B": [
            "d_b_typ1",
            "d_b_typ2"
        ],
        "C": [
            "d_c_typ1",
            "d_c_typ2"
        ]
    }
}
```

### GL String Columns

Instead of providing single locus alleles per column with `locus_column_mapping`, a GL String describing the whole
genotype can be provided per column. Use `glstring_columns` to provide a list of GL String columns to reduce.

```json
  "glstring_columns": [
    "donor_gl",
    "recip_gl"
  ],
```

Depending upon the data, only one of `locus_column_mapping` or `glstring_columns` needs to be provided.

### Redux Options

`redux_type` Reduction Type

Valid Options are:

| Reduction Type | Description                                     |
|----------------|-------------------------------------------------|
| `G`            | Reduce to G Group Level                         |
| `P`            | Reduce to P Group Level                         |
| `lg`           | Reduce to 2 field ARD level (append `g`)        |
| `lgx`          | Reduce to 2 field ARD level                     |
| `W`            | Reduce/Expand to 3 field WHO nomenclature level |
| `exon`         | Reduce/Expand to exon level                     |
| `U2`           | Reduce to 2 field unambiguous level             |

### Cache size

When processing a large file, it's helpful to cache results of previous reductions, the default is to cache
only 1,000 but this can be increased with the `redux_cache_size` option.

```json
  "redux_cache_size": 5000,
```

### Kinds of typings to reduce

Pick and choose which of the typings to reduce.

```json
    "reduce_serology": false,
    "reduce_v2": true,
    "convert_v2_to_v3": false,
    "reduce_3field": true,
    "reduce_P": true,
    "reduce_XX": false,
    "reduce_MAC": true,
```

Valid options: `true` or `false`

### Map to DRBX

`map_drb345_to_drbx` Map to DRBX Typings based on DRB3, DRB4 and DRB5 typings
using [WMDA method](https://www.nature.com/articles/1705672).

Valid options: `true` or `false`

### Locus Name in Allele

`locus_in_allele_name`
Is locus name present in allele ? E.g. `A*01:01` vs `01:01`

Valid options: `true` or `false`

### Keep Locus Name in Allele

`keep_locus_in_allele_name`
Should the reduced version have locus name present in allele ? E.g. `A*01:01` vs `01:01`

Valid options: `true` or `false`

### Create New Column

`new_column_for_redux` Add a separate column for processed column or replace the current column. Creates a `reduced_`
version of the column. Otherwise, the same column is replaced with the reduced version.

Valid options: `true`, `false`

Specify the prefix for the new column with `reduced_column_prefix`.

```json
"reduced_column_prefix": "reduced_",
```

### GL String

Generate a GL String column with reduced typings from each subject.

```json
  "generate_glstring": true,
```

Valid options: `true`, `false`

### Output Format

`output_file_format` Format of the output file

Valid options: `csv` or `xlsx`

For Excel output, `openpyxl` library needs to be installed. Install with:

```shell
 pip install openpyxl
```

### Compression Options

`apply_compression` Compression to use for output file. Applies only to CSV files.

Valid options: `'gzip'`, `'zip'` or `null`

### Verbose log Options

`verbose_log` Show verbose log ?

Valid options: `true` or `false`
