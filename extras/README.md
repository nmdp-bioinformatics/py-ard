# Extras

# Script to batch process a CSV File

**Example Scripts to batch reduce HLA typings from a CSV File**

`pyard-reduce-csv` command can be used with a config file(that describes ways
to reduce the file) can be used to take a CSV file with HLA typing data and 
reduce certain columns and produce a new CSV or an Excel file.

Install `py-ard` and use `pyard-reduce-csv` command specifying the changes in a JSON
config file and running `pyard-reduce-csv -c <config-file>` will produce result based
on the configuration in the config file.


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

**NOTE**: The locus is the 2nd term in the column name
E.g., for column `column R_DRB1_type1`, `DPB1` is the locus name

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
  ],
```


### Redux Options
`redux_type` Reduction Type

Valid Options: `G`, `lg` and `lgx`

### Compression Options
`apply_compression` Compression to use for output file

Valid options: `'gzip'`, `'zip'` or `null`

### Verbose log Options
`log_comment` Show verbose log ?

Valid options: `true` or `false`

### Types of typings to reduce 
```json
  "verbose_log": true,
  "reduce_serology": false,
  "reduce_v2": true,
  "reduce_3field": true,
  "reduce_P": true,
  "reduce_XX": false,
  "reduce_MAC": true,
```
Valid options: `true` or `false`


### Locus Name in Allele
`locus_in_allele_name` 
Is locus name present in allele ? E.g. A*01:01 vs 01:01

Valid options: `true` or `false`

### Output Format
`output_file_format` Format of the output file

Valid options: `csv` or `xlsx`

### Create New Column 
`new_column_for_redux` Add a separate column for processed column or replace
the current column. Creates a `reduced_` version of the column.

Valid options: `true`, `false`

### Map to DRBX
`map_drb345_to_drbx` Map to DRBX Typings based on DRB3, DRB4 and DRB5 typings.

Valid options: `true` or `false`
