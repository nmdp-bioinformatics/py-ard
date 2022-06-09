# Extras

# Script to batch process a CSV File

**Example Scripts to batch reduce HLA typings from a CSV File**

`pyard-reduce-csv` command can be used with a config file(that describes ways to reduce the file) can be used to take a
CSV file with HLA typing data and reduce certain columns and produce a new CSV or an Excel file.

Install `py-ard` and use `pyard-reduce-csv` command specifying the changes in a JSON config file and
running `pyard-reduce-csv -c <config-file>` to produce a resulting file based on the configuration in the config file.

See [Example JSON config file](reduce_conf.json).

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
  "r_drb1_typ1",
  "r_drb1_typ2",
  "r_dpb1_typ1",
  "r_dpb1_typ2"
]
```

### CSV Columns to reduce

`columns_to_reduce_in_csv` List of columns which have typing information and need to be reduced.

**Important**: The locus is the 2nd term in the column name separated by `_`. The program uses this to figure out the
column name for the typings in that column.

E.g., for column `R_DRB1_type1`, `DPB1` is the locus name

```json
  [
  "r_a_typ1",
  "r_a_typ2",
  "r_b_typ1",
  "r_b_typ2",
  "r_c_typ1",
  "r_c_typ2",
  "r_drb1_typ1",
  "r_drb1_typ2",
  "r_dpb1_typ1",
  "r_dpb1_typ2"
]
```

### Redux Options

`redux_type` Reduction Type

Valid Options are:

| Reduction Type | Description                                     |
|----------------|-------------------------------------------------|
| `G`            | Reduce to G Group Level                         |
| `lg`           | Reduce to 2 field ARD level (append `g`)        |
| `lgx`          | Reduce to 2 field ARD level                     |
| `W`            | Reduce/Expand to 3 field WHO nomenclature level |
| `exon`         | Reduce/Expand to exon level                     |


### Kinds of typings to reduce

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

### Locus Name in Allele

`locus_in_allele_name`
Is locus name present in allele ? E.g. `A*01:01` vs `01:01`

Valid options: `true` or `false`

### Output Format

`output_file_format` Format of the output file

Valid options: `csv` or `xlsx`

For Excel output, `openpyxl` library needs to be installed. Install with:
```shell
 pip install openpyxl
```


### Create New Column

`new_column_for_redux` Add a separate column for processed column or replace the current column. Creates a `reduced_` version of the column. Otherwise, the same column is replaced with the reduced version.

Valid options: `true`, `false`

### Map to DRBX

`map_drb345_to_drbx` Map to DRBX Typings based on DRB3, DRB4 and DRB5 typings using [WMDA method](https://www.nature.com/articles/1705672).

Valid options: `true` or `false`

### Compression Options

`apply_compression` Compression to use for output file. Applies only to CSV files.

Valid options: `'gzip'`, `'zip'` or `null`

### Verbose log Options

`verbose_log` Show verbose log ?

Valid options: `true` or `false`
