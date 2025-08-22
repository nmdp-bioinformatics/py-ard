<a id="1.5.5"></a>
# [Allow ignorable alleles in GL String (1.5.5)](https://github.com/nmdp-bioinformatics/py-ard/releases/tag/1.5.5) - 2025-08-22

## What's Changed
* Fix issue when floating point numbers are present in batch by [@pbashyal-nmdp](https://github.com/pbashyal-nmdp) in [#340](https://github.com/nmdp-bioinformatics/py-ard/pull/340)
* Add setuptools by [@pbashyal-nmdp](https://github.com/pbashyal-nmdp) in [#343](https://github.com/nmdp-bioinformatics/py-ard/pull/343)
* Bump gunicorn from 22.0.0 to 23.0.0 by [@dependabot](https://github.com/dependabot)[bot] in [#346](https://github.com/nmdp-bioinformatics/py-ard/pull/346)
* Bump setuptools from 75.8.0 to 78.1.1 by [@dependabot](https://github.com/dependabot)[bot] in [#349](https://github.com/nmdp-bioinformatics/py-ard/pull/349)
* Allow absent/pseudo-gene alleles to be ignored. by [@pbashyal-nmdp](https://github.com/pbashyal-nmdp) in [#353](https://github.com/nmdp-bioinformatics/py-ard/pull/353)


**Full Changelog**: https://github.com/nmdp-bioinformatics/py-ard/compare/1.5.3...1.5.5

[Changes][1.5.5]


<a id="1.5.3"></a>
# [1.5.3 - Single `lgx` reductions and `/ard` endpoint](https://github.com/nmdp-bioinformatics/py-ard/releases/tag/1.5.3) - 2024-10-30

## What's Changed
* Only single `lgx` reductions by [@pbashyal-nmdp](https://github.com/pbashyal-nmdp) in [#334](https://github.com/nmdp-bioinformatics/py-ard/pull/334)
* `/ard/{allele}` endpoint for `lgx` reduction by [@pbashyal-nmdp](https://github.com/pbashyal-nmdp) in [#335](https://github.com/nmdp-bioinformatics/py-ard/pull/335)


**Full Changelog**: https://github.com/nmdp-bioinformatics/py-ard/compare/1.5.1...1.5.3

[Changes][1.5.3]


<a id="1.5.1"></a>
# [1.5.1](https://github.com/nmdp-bioinformatics/py-ard/releases/tag/1.5.1) - 2024-09-11

## What's Changed
* pyard-service Docker changes by [@pbashyal-nmdp](https://github.com/pbashyal-nmdp) in [#329](https://github.com/nmdp-bioinformatics/py-ard/pull/329)
* Homozygosify GL String, Suppress loci by [@pbashyal-nmdp](https://github.com/pbashyal-nmdp) in [#332](https://github.com/nmdp-bioinformatics/py-ard/pull/332)


**Full Changelog**: https://github.com/nmdp-bioinformatics/py-ard/compare/1.5.0...1.5.1

[Changes][1.5.1]


<a id="1.5.0"></a>
# [Support for Python 3.12 (1.5.0)](https://github.com/nmdp-bioinformatics/py-ard/releases/tag/1.5.0) - 2024-06-11

- Able to run in **Python 3.12**
- Upgraded Pandas to `2.2.2`
- *Python 3.8* is **deprecated**. Use `py-ard==1.2.1` for Python 3.8.

## What's Changed
* Support for Python 3.12 by [@pbashyal-nmdp](https://github.com/pbashyal-nmdp) in [#328](https://github.com/nmdp-bioinformatics/py-ard/pull/328)



[Changes][1.5.0]


<a id="1.2.1"></a>
# [Fix for ping mode (1.2.1)](https://github.com/nmdp-bioinformatics/py-ard/releases/tag/1.2.1) - 2024-05-31

## What's Changed
* Ping reductions for duplicates by [@pbashyal-nmdp](https://github.com/pbashyal-nmdp) in [#326](https://github.com/nmdp-bioinformatics/py-ard/pull/326)


**Full Changelog**: https://github.com/nmdp-bioinformatics/py-ard/compare/1.2.0...1.2.1

[Changes][1.2.1]


<a id="1.2.0"></a>
# [`ping` mode is default (1.2.0)](https://github.com/nmdp-bioinformatics/py-ard/releases/tag/1.2.0) - 2024-05-29

When in ping mode, alleles that do not have a G group, their corresponding P group is used. This will be the default behavior unless a `"ping": False` is supplied to `pyard.init()` call.


## What's Changed
* Make `ping` mode default by [@pbashyal-nmdp](https://github.com/pbashyal-nmdp) in [#323](https://github.com/nmdp-bioinformatics/py-ard/pull/323)


**Full Changelog**: https://github.com/nmdp-bioinformatics/py-ard/compare/1.1.3...1.2.0

[Changes][1.2.0]


<a id="1.1.3"></a>
# [Fix `exon` redux for 2 field alleles (1.1.3)](https://github.com/nmdp-bioinformatics/py-ard/releases/tag/1.1.3) - 2024-05-07

To correctly reduce to the exon version, it first expands to `W` and then reduce to `exon` level producing all possibilities at exon level.

Fixes [#320](https://github.com/nmdp-bioinformatics/py-ard/issues/320)

## What's Changed
* Bump gunicorn from 20.1.0 to 22.0.0 by [@dependabot](https://github.com/dependabot) in [#319](https://github.com/nmdp-bioinformatics/py-ard/pull/319)
* Fix `exon` reductions for 2 field alleles by [@pbashyal-nmdp](https://github.com/pbashyal-nmdp) in [#322](https://github.com/nmdp-bioinformatics/py-ard/pull/322)


**Full Changelog**: https://github.com/nmdp-bioinformatics/py-ard/compare/1.1.2...1.1.3

[Changes][1.1.3]


<a id="1.1.2"></a>
# [ARD default redux + Bug Fixes (1.1.2)](https://github.com/nmdp-bioinformatics/py-ard/releases/tag/1.1.2) - 2024-03-22

Feature:
 - ARD reduction (`lgx`) is the default for `ard.redux()`

Bug Fixes:
 - When looking up MAC codes for allele list, look up with smart sort
 - Batch processing failed for zip and no compression
 

[Changes][1.1.2]


<a id="1.1.1"></a>
# [Serology Updates (1.1.1)](https://github.com/nmdp-bioinformatics/py-ard/releases/tag/1.1.1) - 2024-03-05

Serolgy Updates

Note: This release changes and updates Serology related data. Please rebuild the cache database if there's a missing Serology error.
```
pyard-import --re-install
```

- Support Associated Antigens in addition to broad/splits [#303](https://github.com/nmdp-bioinformatics/py-ard/issues/303) 
- Fix Serology reduction for 2 field alleles
- All recognized serology to be valid, not only the ones that have corresponding DNA Alleles [#306](https://github.com/nmdp-bioinformatics/py-ard/issues/306) 
- Fix batch processing for DRBX column
- Map Serology to the correct XX version

[Changes][1.1.1]


<a id="1.0.11"></a>
# [Fix CWD and Serology reduction issues (1.0.11)](https://github.com/nmdp-bioinformatics/py-ard/releases/tag/1.0.11) - 2024-02-02


- CWD reduction issues for XX alleles
- Allow S reduction mode for REST endpoint

See [#301](https://github.com/nmdp-bioinformatics/py-ard/issues/301) For details.

[Changes][1.0.11]


<a id="1.0.10"></a>
# [1.0.10](https://github.com/nmdp-bioinformatics/py-ard/releases/tag/1.0.10) - 2024-01-19

## What's Changed
* Fix serology sort by [@pbashyal-nmdp](https://github.com/pbashyal-nmdp) in [#297](https://github.com/nmdp-bioinformatics/py-ard/pull/297)


**Full Changelog**: https://github.com/nmdp-bioinformatics/py-ard/compare/1.0.9...1.0.10

[Changes][1.0.10]


<a id="1.0.9"></a>
# [1.0.9 Updated CWD2 Reference Data](https://github.com/nmdp-bioinformatics/py-ard/releases/tag/1.0.9) - 2023-12-15

- Updated CWD2 Reference Data from igdawg
- `cwd_redux()` can handle CWD2 allele that are Nulls 


[Changes][1.0.9]


<a id="1.0.8"></a>
# [1.0.8 - `/similar` endpoint and validation fix](https://github.com/nmdp-bioinformatics/py-ard/releases/tag/1.0.8) - 2023-12-05

- [#286](https://github.com/nmdp-bioinformatics/py-ard/issues/286) `similar` endpoint return all alleles/MAC with given prefixes
- [#287](https://github.com/nmdp-bioinformatics/py-ard/issues/287)  Allele validation in non-strict mode


[Changes][1.0.8]


<a id="1.0.7"></a>
# [Find Similar Alleles (1.0.7)](https://github.com/nmdp-bioinformatics/py-ard/releases/tag/1.0.7) - 2023-11-09

Features:
 - Find similar Alleles options with `pyard` command [#264](https://github.com/nmdp-bioinformatics/py-ard/issues/264) 

Bug Fixes:
 - V2 formats that are not valid [#283](https://github.com/nmdp-bioinformatics/py-ard/issues/283) 
 - MICA, MICB, HFE alleles that show up as V2 formats [#280](https://github.com/nmdp-bioinformatics/py-ard/issues/280) 

[Changes][1.0.7]


<a id="1.0.6"></a>
# [1.0.6 Validation of allele specific MAC codes](https://github.com/nmdp-bioinformatics/py-ard/releases/tag/1.0.6) - 2023-10-30

- Use allele specific antigen code rules when validating MACs that cross antigen group similar to [MAC Service](https://hml.nmdp.org/macui/)
- Returns the original `InvalidAlleleError` instead of wrapping it in `InvalidTypingError` when an allele is not valid.

[Changes][1.0.6]


<a id="1.0.5"></a>
# [1.0.5 Non strict mode](https://github.com/nmdp-bioinformatics/py-ard/releases/tag/1.0.5) - 2023-10-04

Supports non-strict mode makes valid alleles by adding expression characters to invalid alleles.

## Use non `strict` mode in config to reduce alleles that may be valid with expression characters.

```python
>>> my_configs = {'strict': False, 'verbose_log': True}
>>> import pyard
>>> ard = pyard.init(config=my_configs, load_mac=False)

>>> ard.redux('A*24:329', 'lgx')
A*24:329 is not valid. Using A*24:329Q
'A*24:329Q'

>>> ard.redux('DQB1*03:276', 'lgx')
DQB1*03:276 is not valid. Using DQB1*03:276N
'DQB1*03:01'
```

## Add non-strict and verbose modes to pyard CLI.

```bash
❯ pyard --gl "DQB1*03:276" -r lgx
Typing Error: DQB1*03:276 is not valid GL String.
 DQB1*03:276 is not a valid Allele

❯ pyard --non-strict --gl "DQB1*03:276" -r lgx
DQB1*03:01

❯ pyard --non-strict --verbose --gl "DQB1*03:276" -r lgx
DQB1*03:276 is not valid. Using DQB1*03:276N
DQB1*03:01
```


[Changes][1.0.5]


<a id="1.0.4"></a>
# [Fixes when used without login user (1.0.4)](https://github.com/nmdp-bioinformatics/py-ard/releases/tag/1.0.4) - 2023-09-19

Fixed the OSError when running without a login user.

[Changes][1.0.4]


<a id="1.0.3"></a>
# [1.0.3 – Permission Errors and pyard updates](https://github.com/nmdp-bioinformatics/py-ard/releases/tag/1.0.3) - 2023-08-17

- Alert permission Errors when `data_dir` is not writable
- Add `--lookup-mac` and `--expand-mac` to `pyard` command

[Changes][1.0.3]


<a id="1.0.2"></a>
# [Fixes issue with using py-ard without MAC (1.0.2)](https://github.com/nmdp-bioinformatics/py-ard/releases/tag/1.0.2) - 2023-08-03

Fixes issue with using py-ard without MAC 
 - When using py-ard with `load_mac=False`, check if the allele looks like a MAC

[Changes][1.0.2]


<a id="1.0.1"></a>
# [1.0.1 → Bug Fixes for 1.0.0 Release](https://github.com/nmdp-bioinformatics/py-ard/releases/tag/1.0.1) - 2023-06-23

Fixed bugs and added some niceties

[#237](https://github.com/nmdp-bioinformatics/py-ard/issues/237)	Additional functionalities for `pyard` CLI command	enhancement	
[#235](https://github.com/nmdp-bioinformatics/py-ard/issues/235)	Invalid allele in CWD2 mapping	bug	
[#234](https://github.com/nmdp-bioinformatics/py-ard/issues/234)	Success with lgx when given Invalid format	bug	
[#233](https://github.com/nmdp-bioinformatics/py-ard/issues/233)	`validate` endpoint can be a GET request	enhancement	
[#230](https://github.com/nmdp-bioinformatics/py-ard/issues/230)	Redux with a "P" option does not return P-groups for two-field or three-field alleles	bug	


[Changes][1.0.1]


<a id="1.0.0"></a>
# [Final Release 1.0.0](https://github.com/nmdp-bioinformatics/py-ard/releases/tag/1.0.0) - 2023-05-04

Release YAY!! 🎉

[Changes][1.0.0]


<a id="0.9.2"></a>
# [Fix Pandas dependencies Latest (0.9.2)](https://github.com/nmdp-bioinformatics/py-ard/releases/tag/0.9.2) - 2023-03-23

Set to `pandas==1.5.3`

[Changes][0.9.2]


<a id="0.9.1"></a>
# [Bug fixes, blend endpoint (0.9.1)](https://github.com/nmdp-bioinformatics/py-ard/releases/tag/0.9.1) - 2023-02-09

 - `blend` endpoint added to the service
 - removed `lg` tables and dictionaries.
 - remove `p_group` table
 - store IMGT db version
 - Fix XX errors for broad/splits
 - Fix loading of IMGT DB version 3130

[Changes][0.9.1]


<a id="0.8.2"></a>
# [Shortnulls for exon mode fixed (0.8.2)](https://github.com/nmdp-bioinformatics/py-ard/releases/tag/0.8.2) - 2022-11-18

See PR [#183](https://github.com/nmdp-bioinformatics/py-ard/issues/183) to fix [#161](https://github.com/nmdp-bioinformatics/py-ard/issues/161) 

[Changes][0.8.2]


<a id="0.8.1"></a>
# [Ping! Mode and DR Blending (0.8.1)](https://github.com/nmdp-bioinformatics/py-ard/releases/tag/0.8.1) - 2022-10-03

PING mode
 - When `ping=True` alleles in P-groups are included in addition to the alleles in G-groups in the corresponding lg/lgx groups.

DR Blending
 - Support DRBX Blending from DRB1
 

[Changes][0.8.1]


<a id="0.8.0"></a>
# [`py-ard` REST Service (0.8.0)](https://github.com/nmdp-bioinformatics/py-ard/releases/tag/0.8.0) - 2022-06-10

`py-ard` REST Service
 - REST service with `/redux`, `/validate`, `/mac` endpoints
 - Run in a Docker container


[Changes][0.8.0]


<a id="0.7.7"></a>
# [BugFix for HLA  Prefix (0.7.7)](https://github.com/nmdp-bioinformatics/py-ard/releases/tag/0.7.7) - 2022-05-19

See [#165](https://github.com/nmdp-bioinformatics/py-ard/issues/165) 

[Changes][0.7.7]


<a id="0.7.6"></a>
# [Reduce to Shortnulls (0.7.6)](https://github.com/nmdp-bioinformatics/py-ard/releases/tag/0.7.6) - 2022-03-29

Implement **shortnulls** behavior with new config variable set to True by default.

This will address things like `DRB4*01:03N` and `DRB5*01:08N` both in terms of accepting them as valid and also by expanding them as appropriate to the list of longer alleles that have the same expression character.

`DRB5*01:08N` is acceptable by WHO rules since all suballeles have N.
`DRB4*01:03N` is acceptable by WMDA (but not WHO) rules but this needs to be handled for things like HF analysis by expansion to something valid (vs rejection) to avoid bias


When there are multiple expression characters in the same group defined by a shortname create multiple shortnulls for the same WHO group. e.g.
```
{'N', 'L'}  A*02:01
{'L', 'Q'}  A*02:01:01
{'L', 'Q'}  A*24:02
{'L', 'Q'}  A*24:02:01
{'L', 'Q'}  A*31:01
{'N', 'Q'}  A*31:01:02
{'N', 'Q'}  B*15:01
{'N', 'Q'}  B*15:01:01
{'N', 'Q'}  B*44:02
```

See [#154](https://github.com/nmdp-bioinformatics/py-ard/issues/154) and [#155](https://github.com/nmdp-bioinformatics/py-ard/issues/155) 

[Changes][0.7.6]


<a id="0.7.5"></a>
# [Support shortnull (0.7.5)](https://github.com/nmdp-bioinformatics/py-ard/releases/tag/0.7.5) - 2022-03-26

Implements **shortnulls** behavior with new config variable set to `True` by default.

This will address things like `DRB4*01:03N` and `DRB5*01:08N` both in terms of accepting them as valid and also by expanding them as appropriate to the list of longer alleles that have the same expression character.

`DRB5*01:08N` is acceptable by **WHO** rules since all suballeles have N.
`DRB4*01:03N` is acceptable by **WMDA** (but not WHO) rules but this needs to be handled for things like HF analysis by expansion to something valid (vs rejection) to avoid bias

[Changes][0.7.5]


<a id="0.7.4"></a>
# [Summary Table for Batch (0.7.4)](https://github.com/nmdp-bioinformatics/py-ard/releases/tag/0.7.4) - 2022-03-23

Show summary table for failed alleles.
```
Summary
-------
35 alleles failed to reduce.
| Column  Name    |      Allele      |      Did you mean ?
| --------------- | ---------------- | -------------------------
| r_A_TYPE1       | A*24:09          | A*24:09N
| r_A_TYPE1       | A*33:157         | A*33:157N
| r_A_TYPE1       | A*26:25          | A*26:25N
| r_A_TYPE1       | A*23:19          | A*23:19N
| r_A_TYPE1       | A*24:02:01:02    | A*24:02:01:02L
```

[Changes][0.7.4]


<a id="0.7.3"></a>
# [Fix batch regression error (0.7.3)](https://github.com/nmdp-bioinformatics/py-ard/releases/tag/0.7.3) - 2022-03-21

 Fix regression error for MAC reduction [#152](https://github.com/nmdp-bioinformatics/py-ard/issues/152) 

[Changes][0.7.3]


<a id="0.7.1.1"></a>
# [Add reduce_2field reduce option (0.7.1.1)](https://github.com/nmdp-bioinformatics/py-ard/releases/tag/0.7.1.1) - 2022-02-23

Batch csv `pyard-reduce-csv` takes in `reduce_2field` option to reduce 2 fields alleles like `B*15:220`, `DPB1*104:01` and `A*02:642`

[Changes][0.7.1.1]


<a id="0.7.2"></a>
# [Stricter Data Validation (0.7.2)](https://github.com/nmdp-bioinformatics/py-ard/releases/tag/0.7.2) - 2022-02-14

Version `0.7.0` has stricter data validation. It will not silently fail by returning an empty `''` string. It'll return of the  `Invalid` exceptions in `pyard.exceptions` when calling `redux_gl` method with invalid GL String. 

See [CHANGELOG.md](https://github.com/nmdp-bioinformatics/py-ard/blob/master/CHANGELOG.md) for full changelog.

[Changes][0.7.2]


<a id="0.6.11"></a>
# [Fix for IMGT URL Change (0.6.11)](https://github.com/nmdp-bioinformatics/py-ard/releases/tag/0.6.11) - 2022-01-24

Fixes a breaking change where all allele lists in IMGTHLA repo have been moved to `/allelelist/` subdirectory.

[Changes][0.6.11]


<a id="0.6.10"></a>
# [Bug fixes for Batch Processing (0.6.10)](https://github.com/nmdp-bioinformatics/py-ard/releases/tag/0.6.10) - 2021-12-13

Batch Reduce Fixes:
- Fix Instantiation of `pyard.ARD` object.
- Fix serology check
- Fix issue with P groups
- A new flag `convert_v2_to_v3` to convert v2 to v3 but not reduce.


[Changes][0.6.10]


<a id="0.6.9"></a>
# [pyard-status command to check the status of all tables in the databases (0.6.9)](https://github.com/nmdp-bioinformatics/py-ard/releases/tag/0.6.9) - 2021-09-27

`pyard-status` command to check the status of all tables in the databases. This will help to see if there are missing tables and also to compare number of data between versions.

```
-------------------------------------------
IMGT DB Version: 3290
-------------------------------------------
|Table Name          |Rows                |
|-----------------------------------------|
|dup_g               |                  17|
|dup_lg              |                   0|
|dup_lgx             |                   0|
|g_group             |                2786|
|lg_group            |                2786|
|lgx_group           |                2786|
MISSING: exon_group table
MISSING: p_group table
|alleles             |               18451|
|xx_codes            |                 946|
MISSING: who_alleles table
MISSING: who_group table
-------------------------------------------
```


[Changes][0.6.9]


<a id="0.6.8"></a>
# [Supports WHO and exon Reduction Types (0.6.8)](https://github.com/nmdp-bioinformatics/py-ard/releases/tag/0.6.8) - 2021-09-24

- Handle cases when there is no typing and when redux fails.
- added `exon` resolution group 
- added `W` resolution group
- Fix validation issues with empty alleles, NNNNs, and non-allelic values. 
- pyard-import can refresh MACs and rebuild databases

[Changes][0.6.8]


<a id="0.6.6"></a>
# [handle invalid/blank input (0.6.6)](https://github.com/nmdp-bioinformatics/py-ard/releases/tag/0.6.6) - 2021-07-29

handle cases with no input and redux fails

[Changes][0.6.6]


<a id="0.6.5"></a>
# [updates to pyard-reduce-csv and unit tests (0.6.5)](https://github.com/nmdp-bioinformatics/py-ard/releases/tag/0.6.5) - 2021-06-17


    Use pyard-reduce-csv command to reduce a CSV file based on a JSON config file.
    Use db_version 3440 in unit test to match behave tests
    Re-run the tests again so local db is used.



[Changes][0.6.5]


<a id="0.6.4"></a>
# [DRBX Mapping and Cw Serology (0.6.4)](https://github.com/nmdp-bioinformatics/py-ard/releases/tag/0.6.4) - 2021-06-16

 - Map DRB3, DRB4 and DRB5 typings to DRBX. [#82](https://github.com/nmdp-bioinformatics/py-ard/issues/82) 
 - Change C to Cw for serology; [#84](https://github.com/nmdp-bioinformatics/py-ard/issues/84) 
 - Return '' for invalid MACs [#84](https://github.com/nmdp-bioinformatics/py-ard/issues/84) 

[Changes][0.6.4]


<a id="0.6.3"></a>
# [0.6.3 release](https://github.com/nmdp-bioinformatics/py-ard/releases/tag/0.6.3) - 2021-06-09

 addresses one-to-many relationship from 2d to lg/lgx

[Changes][0.6.3]


<a id="0.6.2"></a>
# [Fixes serology mappings for broad to include alleles in the split (0.6.2)](https://github.com/nmdp-bioinformatics/py-ard/releases/tag/0.6.2) - 2021-06-07

Fixes serology mappings for broad to include alleles in the split.

[Changes][0.6.2]


<a id="0.6.1"></a>
# [V2 to V3 Mapping (0.6.1)](https://github.com/nmdp-bioinformatics/py-ard/releases/tag/0.6.1) - 2021-02-04


   - Heuristically predict V3 from V2 when not in exceptional case list
   - Make is_XX a public method on the ARD object
   - Update README and fix bug in pyard-import for importing into Latest


[Changes][0.6.1]


<a id="0.6.0"></a>
# [Nomenclature versioning (0.6.0)](https://github.com/nmdp-bioinformatics/py-ard/releases/tag/0.6.0) - 2020-12-08

adds nomenclature versioning, cmdline options, GL string examples

[Changes][0.6.0]


<a id="0.5.1"></a>
# [fix mac expansion (0.5.1)](https://github.com/nmdp-bioinformatics/py-ard/releases/tag/0.5.1) - 2020-11-30

Fix serology mapping and mac expansions

[Changes][0.5.1]


<a id="0.4.1"></a>
# [Upgrade Pandas to 1.1.4 (0.4.1)](https://github.com/nmdp-bioinformatics/py-ard/releases/tag/0.4.1) - 2020-11-03

Update pandas 1.1.4

   - Pandas `1.1.2` doesn't work with Python 3.9. Upgrade Pandas to `1.1.4` which works with Python 3.8 and 3.9


[Changes][0.4.1]


<a id="0.4.0"></a>
# [Support reduction of serologically typed GL String (0.4.0)](https://github.com/nmdp-bioinformatics/py-ard/releases/tag/0.4.0) - 2020-10-22

Uses WMDA `rel_dna_ser.txt` for the corresponding version of IMGT database to produce serology mapping

[Changes][0.4.0]


<a id="0.3.0"></a>
# [Use sqlite3 database for reference data (0.3.0)](https://github.com/nmdp-bioinformatics/py-ard/releases/tag/0.3.0) - 2020-10-15

 Use sqlite3 database for data 

Offload MAC codes from memory to sqlite3 database (natively supported by Python) to reduce
memory footprint. All MAC lookups happen through the db. The alleles and G group expansions
are still held in memory.

In addition, all generated data is saved as tables in the same database. This leads to one
file for storing all reference data in a standard format.

This led to drastic reduction in memory usage and startup time.

|Version |First Time| Prebuilt Data|
|:--|--:|--:|
| 0.1.0 | 10.5 sec |  4.92 sec|
| 0.2.0 | 814 msec |  598 msec|
| 0.3.0 | 24.1 msec | 24.7 msec |

Heap memory used by ARD reference data after `ard = pyard.ARD(3290)`

|Version |Memory (MB) |
|:--|--:|
| 0.1.0 | 2977.86 MB |
| 0.2.0 | 420.76 MB |
| 0.3.0 | 3.74 MB |


[Changes][0.3.0]


<a id="0.2.0"></a>
# [rearrange data in memory (0.2.0)](https://github.com/nmdp-bioinformatics/py-ard/releases/tag/0.2.0) - 2020-10-14

This release rearranges how memory is used especially MAC codes and a lot of cleanup.

[Changes][0.2.0]


<a id="0.1.0"></a>
# [load_mac_file flag to load MAC file (0.1.0)](https://github.com/nmdp-bioinformatics/py-ard/releases/tag/0.1.0) - 2020-10-01

 Rename download_mac flag

  - Rename `download_mac` ARD flag to `load_mac_file` as it properly describes what it does.
  - Remove dead code
  - Reformat code and fix some comments
  - Version bumped to `0.1.0`
  - Updated `pandas` to `1.1.2`

[Changes][0.1.0]


<a id="0.0.21"></a>
# [fix tests and sorting (0.0.21)](https://github.com/nmdp-bioinformatics/py-ard/releases/tag/0.0.21) - 2020-09-09

fixes test and also a bug in 4th field sorting

[Changes][0.0.21]


<a id="0.0.20"></a>
# [allow P and G as input, fix lg and lgx behavior (0.0.20)](https://github.com/nmdp-bioinformatics/py-ard/releases/tag/0.0.20) - 2020-09-09

This release fixes the behavior of lg and lgx to always reduce to 2-field.
It also allows P and G alleles as input

[Changes][0.0.20]


<a id="0.0.18"></a>
# [Fixes G-codes expansion (0.0.18)](https://github.com/nmdp-bioinformatics/py-ard/releases/tag/0.0.18) - 2020-07-29

Fixes G-codes expansion when smart sorting.

[Changes][0.0.18]


<a id="0.0.17"></a>
# [Specify path for temporary files (0.0.17)](https://github.com/nmdp-bioinformatics/py-ard/releases/tag/0.0.17) - 2020-07-22

You can specify path when creating ARD object.
```
ard = ARD('3290', data_dir='/tmp/py-ard')
```

[Changes][0.0.17]


<a id="0.0.16"></a>
# [version 0.0.16](https://github.com/nmdp-bioinformatics/py-ard/releases/tag/0.0.16) - 2020-07-09

update MAC location and version to 0.0.16

[Changes][0.0.16]


<a id="0.0.15.0"></a>
# [update to MAC location (0.0.15.0)](https://github.com/nmdp-bioinformatics/py-ard/releases/tag/0.0.15.0) - 2020-05-28



[Changes][0.0.15.0]


<a id="0.0.15"></a>
# [update to MAC location (0.0.15)](https://github.com/nmdp-bioinformatics/py-ard/releases/tag/0.0.15) - 2020-05-28

yes

[Changes][0.0.15]


<a id="0.0.14"></a>
# [0.0.14](https://github.com/nmdp-bioinformatics/py-ard/releases/tag/0.0.14) - 2020-04-14

- Support for Python 3.7
- Broad XX enhancement 
- p Performance improvements

[Changes][0.0.14]


[1.5.5]: https://github.com/nmdp-bioinformatics/py-ard/compare/1.5.3...1.5.5
[1.5.3]: https://github.com/nmdp-bioinformatics/py-ard/compare/1.5.1...1.5.3
[1.5.1]: https://github.com/nmdp-bioinformatics/py-ard/compare/1.5.0...1.5.1
[1.5.0]: https://github.com/nmdp-bioinformatics/py-ard/compare/1.2.1...1.5.0
[1.2.1]: https://github.com/nmdp-bioinformatics/py-ard/compare/1.2.0...1.2.1
[1.2.0]: https://github.com/nmdp-bioinformatics/py-ard/compare/1.1.3...1.2.0
[1.1.3]: https://github.com/nmdp-bioinformatics/py-ard/compare/1.1.2...1.1.3
[1.1.2]: https://github.com/nmdp-bioinformatics/py-ard/compare/1.1.1...1.1.2
[1.1.1]: https://github.com/nmdp-bioinformatics/py-ard/compare/1.0.11...1.1.1
[1.0.11]: https://github.com/nmdp-bioinformatics/py-ard/compare/1.0.10...1.0.11
[1.0.10]: https://github.com/nmdp-bioinformatics/py-ard/compare/1.0.9...1.0.10
[1.0.9]: https://github.com/nmdp-bioinformatics/py-ard/compare/1.0.8...1.0.9
[1.0.8]: https://github.com/nmdp-bioinformatics/py-ard/compare/1.0.7...1.0.8
[1.0.7]: https://github.com/nmdp-bioinformatics/py-ard/compare/1.0.6...1.0.7
[1.0.6]: https://github.com/nmdp-bioinformatics/py-ard/compare/1.0.5...1.0.6
[1.0.5]: https://github.com/nmdp-bioinformatics/py-ard/compare/1.0.4...1.0.5
[1.0.4]: https://github.com/nmdp-bioinformatics/py-ard/compare/1.0.3...1.0.4
[1.0.3]: https://github.com/nmdp-bioinformatics/py-ard/compare/1.0.2...1.0.3
[1.0.2]: https://github.com/nmdp-bioinformatics/py-ard/compare/1.0.1...1.0.2
[1.0.1]: https://github.com/nmdp-bioinformatics/py-ard/compare/1.0.0...1.0.1
[1.0.0]: https://github.com/nmdp-bioinformatics/py-ard/compare/0.9.2...1.0.0
[0.9.2]: https://github.com/nmdp-bioinformatics/py-ard/compare/0.9.1...0.9.2
[0.9.1]: https://github.com/nmdp-bioinformatics/py-ard/compare/0.8.2...0.9.1
[0.8.2]: https://github.com/nmdp-bioinformatics/py-ard/compare/0.8.1...0.8.2
[0.8.1]: https://github.com/nmdp-bioinformatics/py-ard/compare/0.8.0...0.8.1
[0.8.0]: https://github.com/nmdp-bioinformatics/py-ard/compare/0.7.7...0.8.0
[0.7.7]: https://github.com/nmdp-bioinformatics/py-ard/compare/0.7.6...0.7.7
[0.7.6]: https://github.com/nmdp-bioinformatics/py-ard/compare/0.7.5...0.7.6
[0.7.5]: https://github.com/nmdp-bioinformatics/py-ard/compare/0.7.4...0.7.5
[0.7.4]: https://github.com/nmdp-bioinformatics/py-ard/compare/0.7.3...0.7.4
[0.7.3]: https://github.com/nmdp-bioinformatics/py-ard/compare/0.7.1.1...0.7.3
[0.7.1.1]: https://github.com/nmdp-bioinformatics/py-ard/compare/0.7.2...0.7.1.1
[0.7.2]: https://github.com/nmdp-bioinformatics/py-ard/compare/0.6.11...0.7.2
[0.6.11]: https://github.com/nmdp-bioinformatics/py-ard/compare/0.6.10...0.6.11
[0.6.10]: https://github.com/nmdp-bioinformatics/py-ard/compare/0.6.9...0.6.10
[0.6.9]: https://github.com/nmdp-bioinformatics/py-ard/compare/0.6.8...0.6.9
[0.6.8]: https://github.com/nmdp-bioinformatics/py-ard/compare/0.6.6...0.6.8
[0.6.6]: https://github.com/nmdp-bioinformatics/py-ard/compare/0.6.5...0.6.6
[0.6.5]: https://github.com/nmdp-bioinformatics/py-ard/compare/0.6.4...0.6.5
[0.6.4]: https://github.com/nmdp-bioinformatics/py-ard/compare/0.6.3...0.6.4
[0.6.3]: https://github.com/nmdp-bioinformatics/py-ard/compare/0.6.2...0.6.3
[0.6.2]: https://github.com/nmdp-bioinformatics/py-ard/compare/0.6.1...0.6.2
[0.6.1]: https://github.com/nmdp-bioinformatics/py-ard/compare/0.6.0...0.6.1
[0.6.0]: https://github.com/nmdp-bioinformatics/py-ard/compare/0.5.1...0.6.0
[0.5.1]: https://github.com/nmdp-bioinformatics/py-ard/compare/0.4.1...0.5.1
[0.4.1]: https://github.com/nmdp-bioinformatics/py-ard/compare/0.4.0...0.4.1
[0.4.0]: https://github.com/nmdp-bioinformatics/py-ard/compare/0.3.0...0.4.0
[0.3.0]: https://github.com/nmdp-bioinformatics/py-ard/compare/0.2.0...0.3.0
[0.2.0]: https://github.com/nmdp-bioinformatics/py-ard/compare/0.1.0...0.2.0
[0.1.0]: https://github.com/nmdp-bioinformatics/py-ard/compare/0.0.21...0.1.0
[0.0.21]: https://github.com/nmdp-bioinformatics/py-ard/compare/0.0.20...0.0.21
[0.0.20]: https://github.com/nmdp-bioinformatics/py-ard/compare/0.0.18...0.0.20
[0.0.18]: https://github.com/nmdp-bioinformatics/py-ard/compare/0.0.17...0.0.18
[0.0.17]: https://github.com/nmdp-bioinformatics/py-ard/compare/0.0.16...0.0.17
[0.0.16]: https://github.com/nmdp-bioinformatics/py-ard/compare/0.0.15.0...0.0.16
[0.0.15.0]: https://github.com/nmdp-bioinformatics/py-ard/compare/0.0.15...0.0.15.0
[0.0.15]: https://github.com/nmdp-bioinformatics/py-ard/compare/0.0.14...0.0.15
[0.0.14]: https://github.com/nmdp-bioinformatics/py-ard/tree/0.0.14

<!-- Generated by https://github.com/rhysd/changelog-from-release v3.9.0 -->
