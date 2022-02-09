# py-ard
[![PyPi Version](https://img.shields.io/pypi/v/py-ard.svg)](https://pypi.python.org/pypi/py-ard) 

ARD reduction for HLA with Python

`py-ard` works with Python 3.8 and higher.

## Install from PyPi

```shell
pip install py-ard
```

## Install from source

```shell
python3 -m venv venv
source venv/bin/activate

python setup.py install
```
## Testing

To run behavior-driven development (BDD) tests locally via the behave framework, you'll need to set up a virtual
environment. See Install from source.

```shell
# Install test dependencies
pip install --upgrade pip
pip install -r test-requirements.txt

# Running Behave and all BDD tests
behave

# Run unit-tests
python -m unittest tests.test_pyard
```

## Using `py-ard` from Python code

`py-ard` can be used in a program to reduce/expand HLA GL String representation. If pyard discovers an invalid Allele, it'll throw an Invalid Exception, not silently return an empty result.

### Initialize `py-ard`

Import `pyard` package.

```python
import pyard
```

The cache size of pre-computed reductions can be changed from the default of 1000 (_not working_: will be fixed in a later release.)
```python
pyard.max_cache_size = 1_000_000
```

Initialize `ARD` object with a version of IMGT HLA database

```python
ard = pyard.ARD(3290)
```

You can specify a different directory for the cached data.

```python
ard = pyard.ARD('3290', data_dir='/tmp/py-ard')
```

You can choose to refresh the MAC code for current IMGT HLA database version

```python
ard.refresh_mac_codes()
```

The default initialization is to use the latest IMGT HLA database

```python
ard = pyard.ARD()
```

### Reduce Typings

Reduce a single locus HLA Typing.

```python
allele = "A*01:01:01"

ard.redux_gl(allele, 'G')
# >>> 'A*01:01:01G'

ard.redux_gl(allele, 'lg')
# >>> 'A*01:01g'

ard.redux_gl(allele, 'lgx')
# >>> 'A*01:01'
```

Reduce an ambiguous GL String

```python
# Reduce GL String
#
ard.redux_gl("A*01:01/A*01:01N+A*02:AB^B*07:02+B*07:AB", "G")
# 'B*07:02:01G+B*07:02:01G^A*01:01:01G+A*02:01:01G/A*02:02'
```

You can also reduce serology based typings.

```python
ard.redux_gl('B14', 'lg')
# >>> 'B*14:01g/B*14:02g/B*14:03g/B*14:04g/B*14:05g/B*14:06g/B*14:08g/B*14:09g/B*14:10g/B*14:11g/B*14:12g/B*14:13g/B*14:14g/B*14:15g/B*14:16g/B*14:17g/B*14:18g/B*14:19g/B*14:20g/B*14:21g/B*14:22g/B*14:23g/B*14:24g/B*14:25g/B*14:26g/B*14:27g/B*14:28g/B*14:29g/B*14:30g/B*14:31g/B*14:32g/B*14:33g/B*14:34g/B*14:35g/B*14:36g/B*14:37g/B*14:38g/B*14:39g/B*14:40g/B*14:42g/B*14:43g/B*14:44g/B*14:45g/B*14:46g/B*14:47g/B*14:48g/B*14:49g/B*14:50g/B*14:51g/B*14:52g/B*14:53g/B*14:54g/B*14:55g/B*14:56g/B*14:57g/B*14:58g/B*14:59g/B*14:60g/B*14:62g/B*14:63g/B*14:65g/B*14:66g/B*14:68g/B*14:70Qg/B*14:71g/B*14:73g/B*14:74g/B*14:75g/B*14:77g/B*14:82g/B*14:83g/B*14:86g/B*14:87g/B*14:88g/B*14:90g/B*14:93g/B*14:94g/B*14:95g/B*14:96g/B*14:97g/B*14:99g/B*14:102g'
```

## Valid Reduction Types

| Reduction Type | Description                                     |
|----------------|-------------------------------------------------|
| `G`            | Reduce to G Group Level                         |
| `lg`           | Reduce to 2 field ARD level (append `g`)        |
| `lgx`          | Reduce to 2 field ARD level                     |
| `W`            | Reduce/Expand to 3 field WHO nomenclature level |
| `exon`         | Reduce/Expand to exon level                     |

# Command Line Tools

## Using `py-ard` from the command line

### Import the latest IMGT database

```shell
$ pyard-import
Created Latest py-ard database
```

### Import particular version of IMGT database

```shell
$ pyard-import --db-version 3.29.0
Created py-ard version 3290 database
```

Import particular version of IMGT database and replace the v2 to v3 mapping 
table from a CSV file.

```shell
$ pyard-import --db-version 3.29.0 --v2-to-v3-mapping map2to3.csv
Created py-ard version 3290 database
Updated v2_mapping table with 'map2to3.csv' mapping file.
```

### Reinstall a particular IMGT database

```shell
pyard-import --db-version 3340 --re-install
```

### Replace the Latest IMGT database with V2 mappings

```shell
$ pyard-import --v2-to-v3-mapping map2to3.csv
```

### Refresh the MAC for the specified version

```shell
$ pyard-import --db-version 3450 --refresh-mac
```

### Show the status of all `py-ard` databases

```shell
$ pyard-status
```

### Reduce a GL String from command line

```shell
$ pyard --gl 'A*01:AB' -r lgx
A*01:01/A*01:02

$ pyard --gl 'DRB1*08:XX' -r G
DRB1*08:01:01G/DRB1*08:02:01G/DRB1*08:03:02G/DRB1*08:04:01G/DRB1*08:05/ ...

$ pyard -v 3290 --gl 'A1' -r lgx # For a particular version of DB
A*01:01/A*01:02/A*01:03/A*01:06/A*01:07/A*01:08/A*01:09/A*01:10/A*01:12/ ...
```
### Batch Reduce a CSV file

`pyard-csv-reduce` can be used to batch process a CSV file with HLA typings. See [documentation](extras/README.md) for instructions on how to configure and run. 
