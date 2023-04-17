# py-ard

Swiss army knife of **HLA** Nomenclature

[![PyPi Version](https://img.shields.io/pypi/v/py-ard.svg)](https://pypi.python.org/pypi/py-ard)

![py-ard-logo.png](images/py-ard-logo.png)

### `py-ard` is ARD reduction for HLA in Python

Human leukocyte antigen (HLA) genes encode cell surface proteins that are important for immune regulation. Exons encoding the Antigen Recognition Domain (ARD) are the most polymorphic region of HLA genes and are important for donor/recipient [HLA matching](https://bethematch.org/patients-and-families/before-transplant/find-a-donor/hla-matching/). The history of allele typing methods has played a major role in determining resolution and ambiguity of reported HLA values. Although HLA [nomenclature](https://www.theatlantic.com/magazine/archive/2023/04/clint-smith-nomenclature-poem/673097/) has not always conformed to the same standard, it is now defined by [The WHO Nomenclature Committee for Factors of the HLA System](https://hla.alleles.org/nomenclature/committee.html). `py-ard` is aware of the variation in historical resolutions and grouping and is able to translate from one representation to another based on alleles published quarterly by [IPD/IMGT-HLA](https://github.com/ANHIG/IMGTHLA/).


## Table of Contents
1. [Installation](#installation)
    * [Install From PyPi](#install-from-pypi)
    * [Install With Homebrew](#install-with-homebrew)
    * [Install From Source](#install-from-source)
2. [Using `py-ard`](#using-py-ard)
    * [Using `py-ard` from Python](#using-py-ard-from-python-code)
    * [Using `py-ard` from R](#using-py-ard-from-r-code)
    * [Perform Reduxtion](#reduce-typings)
    * [DRBX blending](#perform-drb1-blending-with-drb3-drb4-and-drb5)
    * [Expand/Lookup MAC](#mac-codes)
3. [Command Line Tools](#command-line-tools)
    * [`pyard-import` Import Reference Data](#pyard-import-import-the-latest-ipd-imgthla-database)
    * [`pyard-status` Show Statuses of Databases](#pyard-status-show-database-status)
    * [`pyard` Redux](#pyard-redux-quickly)
    * [`pyard-csv-reduce` Batch Mode Redux](#pyard-csv-reduce-batch-reduce-a-csv-file)
4. [`py-ard` REST Webservice](#py-ard-rest-web-service)
5. [Docker Deployment](#docker-deployment-of-py-ard-rest-web-service)

## Installation
`py-ard` works with Python 3.8 and higher.

### Install from PyPi

```shell
pip install py-ard
```
Note: With `py-ard` version *1.0.0* and higher, the redux API has changed. If your use requires the older API, please install with `pip install py-ard==0.9.2`


### Install With Homebrew

On macOS, `py-ard` can be installed using Homebrew package manager.
This is very handy for using the command line versions of the tool without having to create virtual environments.

First time, you'd need to tap the `nmdp-bioinformatics` tap.

```shell
brew tap nmdp-bioinformatics/tap
```

Install `py-ard`

```shell
brew install py-ard
```

Homebrew will notify you as new versions of `py-ard` are released.

### Install from source

```shell
python3 -m venv venv
source venv/bin/activate

python setup.py install
```

See [Our Contribution Guide](CONTRIBUTING.rst) for open source contribution to `py-ard`.

## Using `py-ard`

### Using `py-ard` from Python code

`py-ard` can be used in a program to reduce/expand HLA GL String representation. If pyard discovers an invalid Allele, it'll throw an Invalid Exception, not silently return an empty result.

#### Initialize `py-ard`

Import `pyard` package.

```python
import pyard
```


Initialize `ARD` object with a version of IMGT HLA database

```python
import pyard

ard = pyard.init('3510')
```

When processing a large numbers of typings, it's helpful to have a cache of previously calculated reductions to make similar typings reduce faster. The cache size of pre-computed reductions can be changed from the default of 1,000 by setting `cache_size` argument. This increases the memory footprint but will significantly increase the processing times for large number of reductions.

```python
import pyard

max_cache_size = 1_000_000
ard = pyard.init('3510', cache_size=max_cache_size)
```

By default, the IPD-IMGT/HLA data is stored locally in `$TMPDIR/pyard`. This may be removed when your computer restarts. You can specify a different, more permanent directory for the cached data.

```python
import pyard.ard

ard = pyard.init('3510', data_dir='/tmp/py-ard')
```

As MAC data changes frequently, you can choose to refresh the MAC code for current IMGT HLA database version.

```python
ard.refresh_mac_codes()
```

The default initialization is to use the latest version of IPD-IMGT/HLA database.

```python
import pyard

ard = pyard.init()
```

You can check the current version of IPD-IMGT/HLA database.
```python
ard.get_db_version()
```

### Reduce Typings

**Note**: Previous to version of 1.0.0 release of `py-ard`, there was `redux` and `redux_gl` methods on `ard`. They have been consolidated so that `redux` handles both GL Strings and individual alleles.

Reduce a single locus HLA Typing by specifying the allele/MAC/XX code and the reduction method to `redux` method.

```python
allele = "A*01:01:01"

ard.redux(allele, 'G')
# >>> 'A*01:01:01G'

ard.redux(allele, 'lg')
# >>> 'A*01:01g'

ard.redux(allele, 'lgx')
# >>> 'A*01:01'
```

Reduce an ambiguous GL String

```python
# Reduce GL String
#
ard.redux("A*01:01/A*01:01N+A*02:AB^B*07:02+B*07:AB", "G")
# 'B*07:02:01G+B*07:02:01G^A*01:01:01G+A*02:01:01G/A*02:02'
```

You can also reduce serology based typings.

```python
ard.redux('B14', 'lg')
# >>> 'B*14:01g/B*14:02g/B*14:03g/B*14:04g/B*14:05g/B*14:06g/B*14:08g/B*14:09g/B*14:10g/B*14:11g/B*14:12g/B*14:13g/B*14:14g/B*14:15g/B*14:16g/B*14:17g/B*14:18g/B*14:19g/B*14:20g/B*14:21g/B*14:22g/B*14:23g/B*14:24g/B*14:25g/B*14:26g/B*14:27g/B*14:28g/B*14:29g/B*14:30g/B*14:31g/B*14:32g/B*14:33g/B*14:34g/B*14:35g/B*14:36g/B*14:37g/B*14:38g/B*14:39g/B*14:40g/B*14:42g/B*14:43g/B*14:44g/B*14:45g/B*14:46g/B*14:47g/B*14:48g/B*14:49g/B*14:50g/B*14:51g/B*14:52g/B*14:53g/B*14:54g/B*14:55g/B*14:56g/B*14:57g/B*14:58g/B*14:59g/B*14:60g/B*14:62g/B*14:63g/B*14:65g/B*14:66g/B*14:68g/B*14:70Qg/B*14:71g/B*14:73g/B*14:74g/B*14:75g/B*14:77g/B*14:82g/B*14:83g/B*14:86g/B*14:87g/B*14:88g/B*14:90g/B*14:93g/B*14:94g/B*14:95g/B*14:96g/B*14:97g/B*14:99g/B*14:102g'
```

## Valid Reduction Types

| Reduction Type | Description                                     |
|----------------|-------------------------------------------------|
| `G`            | Reduce to G Group Level                         |
| `P`            | Reduce to P Group Level                         |
| `lg`           | Reduce to 2 field ARD level (append `g`)        |
| `lgx`          | Reduce to 2 field ARD level                     |
| `W`            | Reduce/Expand to 3 field WHO nomenclature level |
| `exon`         | Reduce/Expand to exon level                     |
| `U2`           | Reduce to 2 field unambiguous level             |

### Perform DRB1 blending with DRB3, DRB4 and DRB5

```python
import pyard

pyard.dr_blender(drb1='HLA-DRB1*03:01+DRB1*04:01', drb3='DRB3*01:01', drb4='DRB4*01:03')
# >>> 'DRB3*01:01+DRB4*01:03'
```

## MAC Codes

`py-ard` supports not only reducing to various types but helps in expanding and
looking up MAC representation. See [MAC Service UI](https://hml.nmdp.org/MacUI/) for detail.

### Expand MAC

You can also use `py-ard` to expand MAC codes. Use `expand_mac` method on `ard`.
```python
ard.expand_mac('HLA-A*01:BC')
# 'HLA-A*01:02/HLA-A*01:03'
```

### Lookup MAC

Find the corresponding MAC code for an allele list GL String.

```python
ard.lookup_mac('A*01:02/A*01:01/A*01:03')
# A*01:MN
```

### CWD Reduction

Reduce a MAC code or an allele list GL String to CWD reduced list.
```python
ard.cwd_redux("B*15:01:01/B*15:01:03/B*15:04/B*15:07/B*15:26N/B*15:27")
# => B*15:01/B*15:07
```

The above 2 methods can be chained to get back a MAC code that has a CWD reduced version.

```python
ard.lookup_mac(ard.cwd_redux("B*15:01:01/B*15:01:03/B*15:04/B*15:07/B*15:26N/B*15:27"))
# 'B*15:AH'
```

### Using `py-ard` from R code

`py-ard` works well from `R` as well. Please see [Using pyard from R language](https://github.com/nmdp-bioinformatics/py-ard/wiki/Using-pyard-library-from-R-language) page for detailed walkthrough.

## Command Line Tools

Various command line interface (CLI) tools are available to use for managing local IPD-IMGT/HLA cache database, running impromptu reduction queries and batch processing of CSV files.

For all tools, use `--imgt-version` and `--data-dir` to specify the IPD-IMGT/HLA database version and the directory where the SQLite files are created.

### `pyard-import` Import the latest IPD-IMGT/HLA database

`pyard-import` helps with importing and reinstalling of prepared IPD-IMGT/HLA and MAC data.

Use `pyard-import -h` to see all the options available.
```shell
$ pyard-import -h
usage: pyard-import [-h] [--list] [-i IMGT_VERSION] [-d DATA_DIR] [--v2-to-v3-mapping V2_V3_MAPPING] [--refresh-mac] [--re-install] [--skip-mac]

py-ard tool to generate reference SQLite database. Allows updating db with custom V2 to V3 mappings. Displays the list of available IMGT database
versions.

options:
  -h, --help            show this help message and exit
  --list                Show Versions of available IMGT Databases
  -i IMGT_VERSION, --imgt-version IMGT_VERSION
                        Import supplied IMGT_VERSION DB Version
  -d DATA_DIR, --data-dir DATA_DIR
                        Data directory to store imported data
  --v2-to-v3-mapping V2_V3_MAPPING
                        V2 to V3 mapping CSV file
  --refresh-mac         Only refresh MAC data
  --re-install          reinstall a fresh version of database
  --skip-mac            Skip creating MAC mapping
```

Run `pyard-import` without any option to download and prepare the latest version of IPD-IMGT/HLA and MAC data.

```shell
$ pyard-import
Created Latest py-ard database
```

#### Import particular version of IMGT database

```shell
$ pyard-import --db-version 3.29.0
Created py-ard version 3290 database
```

Import particular version of IMGT database and replace the v2 to v3 mapping
table from a CSV file.

```shell
$ pyard-import --imgt-version 3.29.0 --v2-to-v3-mapping map2to3.csv
Created py-ard version 3290 database
Updated v2_mapping table with 'map2to3.csv' mapping file.
```

#### Reinstall a particular IMGT database

```shell
pyard-import --imgt-version 3340 --re-install
```

#### Replace the Latest IMGT database with V2 mappings

```shell
$ pyard-import --v2-to-v3-mapping map2to3.csv
```

#### Refresh the MAC for the specified version

```shell
$ pyard-import --imgt-version 3450 --refresh-mac
```

#### Skip MAC loading

You can skip loading MAC if you don't need by using `--skip-mac`

```shell
$ pyard-import --imgt-version 3150 --skip-mac
```

### `pyard-status` Show database status

Show the statuses of all `py-ard` databases

`pyard-status` goes through all the available databases and checks all the tables that should be available. This is very helpful to show all the databases, number of rows in each table, any missing tables and the stored IPD-IMGT/HLA version.

```shell
$ pyard-status
```

Use ` --data-dir` to specify an alternate directory for cached database files.
```shell
$ pyard-status  --data-dir ~/.pyard/
IMGT DB Version: Latest (3440)
There is a newer IMGT release than version 3440
Upgrade to latest version '3510' with 'pyard-import --re-install'
File: /Users/pbashyal/.pyard/pyard-Latest.sqlite3
Size: 533.37MB
-------------------------------------------
|Table Name          |Rows                |
|-----------------------------------------|
|dup_g               |                  59|
|dup_lgx             |                   1|
|g_group             |               14223|
|p_group             |               18872|
|lgx_group           |               14223|
|exon_group          |               12934|
|p_not_g             |                1681|
|xx_codes            |                1517|
|who_group           |               30785|
|alleles             |               32504|
|exp_alleles         |                  60|
|who_alleles         |               30523|
|mac_codes           |             1089379|
-------------------------------------------
```

### `pyard` Redux quickly

`pyard` command can be used for quick reductions from the command line. Use `--help` option to see all the available options.
```shell
$ pyard --help
usage: pyard [-h] [-v] [-d DATA_DIR] [-i IMGT_VERSION] [-g GL_STRING]
             [-r {G,P,lg,lgx,W,exon,U2}] [--splits SPLITS]

py-ard tool to redux GL String

options:
  -h, --help            show this help message and exit
  -v, --version         IPD-IMGT/HLA DB Version number
  -d DATA_DIR, --data-dir DATA_DIR
                        Data directory to store imported data
  -i IMGT_VERSION, --imgt-version IMGT_VERSION
                        IPD-IMGT/HLA db to use for redux
  -g GL_STRING, --gl GL_STRING
                        GL String to reduce
  -r {G,P,lg,lgx,W,exon,U2}, --redux-type {G,P,lg,lgx,W,exon,U2}
                        Reduction Method
  --splits SPLITS       Find Broad and Splits

```

Reduce from command line by specifying any typing with `-g` or `--gl` option and the reduction method with `-r` or `--redux-type` option.

```shell
$ pyard -g 'A*01:AB' -r lgx
A*01:01/A*01:02

$ pyard --gl 'DRB1*08:XX' -r G
DRB1*08:01:01G/DRB1*08:02:01G/DRB1*08:03:02G/DRB1*08:04:01G/DRB1*08:05/ ...

$ pyard -i 3290 --gl 'A1' -r lgx # For a particular version of DB
A*01:01/A*01:02/A*01:03/A*01:06/A*01:07/A*01:08/A*01:09/A*01:10/A*01:12/ ...
```

If the `-r` option is left out, `pyard` will print out the result of all reduction methods.

```shell
$ pyard -g 'A*01:01:01:01'
Reduction Method: G
-------------------
A*01:01:01G

Reduction Method: P
-------------------
A*01:01P

Reduction Method: lg
--------------------
A*01:01g

Reduction Method: lgx
---------------------
A*01:01

Reduction Method: W
-------------------
A*01:01:01:01

Reduction Method: exon
----------------------
A*01:01:01

Reduction Method: U2
--------------------
A*01:01
```

`py-ard` knows about the broad/splits of serology and DNA, you can find by using `--splits` option to `pyard` command.

```shell
$ pyard --splits "A*10"
A*10 = A*25/A*26/A*34/A*66

$ pyard --splits B14
B14 = B64/B65
```

### `pyard-csv-reduce` Batch Reduce a CSV file

`pyard-csv-reduce` can be used to batch process a CSV file with HLA typings. See [documentation](extras/README.md) for detailed information about all the options.


## `py-ard` REST Web Service

Run `py-ard` as a service so that it can be accessed as a REST service endpoint.

To start in debug mode, you can run the `app.py` script. The endpoint should then be available at [localhost:8080](http://0.0.0.0:8080)
```shell
$ python app.py
 * Serving Flask app 'app'
 * Debug mode: on
WARNING: This is a development server. Do not use it in a production deployment. Use a production WSGI server instead.
 * Running on all addresses (0.0.0.0)
 * Running on http://127.0.0.1:8080
 * Running on http://10.0.1.37:8080
Press CTRL+C to quit
```

## Docker deployment of py-ard REST Web Service

For deploying to production, build a Docker image and use that image for deploying to a server.

Build the docker image:
```shell
make docker-build
```

builds a Docker image named `pyard-service:latest`

Build the docker and run it with:
```shell
make docker
```

The endpoint should then be available at [localhost:8080](http://0.0.0.0:8080)
