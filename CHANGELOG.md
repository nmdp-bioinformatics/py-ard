<a name="1.0.6"></a>
# [1.0.6 Validation of allele specific MAC codes](https://github.com/nmdp-bioinformatics/py-ard/releases/tag/1.0.6) - 30 Oct 2023

- Use allele specific antigen code rules when validating MACs that cross antigen group similar to [MAC Service](https://hml.nmdp.org/macui/)
- Returns the original `InvalidAlleleError` instead of wrapping it in `InvalidTypingError` when an allele is not valid.

[Changes][1.0.6]


<a name="1.0.5"></a>
# [1.0.5 Non strict mode](https://github.com/nmdp-bioinformatics/py-ard/releases/tag/1.0.5) - 04 Oct 2023

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


<a name="1.0.4"></a>
# [Fixes when used without login user (1.0.4)](https://github.com/nmdp-bioinformatics/py-ard/releases/tag/1.0.4) - 19 Sep 2023

Fixed the OSError when running without a login user.

[Changes][1.0.4]


<a name="1.0.3"></a>
# [1.0.3 – Permission Errors and pyard updates](https://github.com/nmdp-bioinformatics/py-ard/releases/tag/1.0.3) - 17 Aug 2023

- Alert permission Errors when `data_dir` is not writable
- Add `--lookup-mac` and `--expand-mac` to `pyard` command

[Changes][1.0.3]


<a name="1.0.2"></a>
# [Fixes issue with using py-ard without MAC (1.0.2)](https://github.com/nmdp-bioinformatics/py-ard/releases/tag/1.0.2) - 03 Aug 2023

Fixes issue with using py-ard without MAC 
 - When using py-ard with `load_mac=False`, check if the allele looks like a MAC

[Changes][1.0.2]


<a name="1.0.1"></a>
# [1.0.1 → Bug Fixes for 1.0.0 Release](https://github.com/nmdp-bioinformatics/py-ard/releases/tag/1.0.1) - 23 Jun 2023

Fixed bugs and added some niceties

[#237](https://github.com/nmdp-bioinformatics/py-ard/issues/237)	Additional functionalities for `pyard` CLI command	enhancement	
[#235](https://github.com/nmdp-bioinformatics/py-ard/issues/235)	Invalid allele in CWD2 mapping	bug	
[#234](https://github.com/nmdp-bioinformatics/py-ard/issues/234)	Success with lgx when given Invalid format	bug	
[#233](https://github.com/nmdp-bioinformatics/py-ard/issues/233)	`validate` endpoint can be a GET request	enhancement	
[#230](https://github.com/nmdp-bioinformatics/py-ard/issues/230)	Redux with a "P" option does not return P-groups for two-field or three-field alleles	bug	


[Changes][1.0.1]


<a name="1.0.0"></a>
# [Final Release 1.0.0](https://github.com/nmdp-bioinformatics/py-ard/releases/tag/1.0.0) - 04 May 2023

Release YAY!! 🎉

[Changes][1.0.0]


<a name="1.0.0rc7"></a>
# [Fix PyPi Packaging (1.0.0rc7)](https://github.com/nmdp-bioinformatics/py-ard/releases/tag/1.0.0rc7) - 17 Apr 2023

Include `requirements.txt` files

[Changes][1.0.0rc7]


<a name="1.0.0rc6"></a>
# [Batch Reduce Fixes (1.0.0rc6)](https://github.com/nmdp-bioinformatics/py-ard/releases/tag/1.0.0rc6) - 05 Apr 2023

Bug fixes
- Fix issue when adding locus name to a serology value
- Fix issue when reducing an allele-list
- Account for lower case allele names

[Changes][1.0.0rc6]


<a name="1.0.0rc5"></a>
# [Decode MAC and CWD 2.0 Reductions (1.0.0rc5)](https://github.com/nmdp-bioinformatics/py-ard/releases/tag/1.0.0rc5) - 03 Apr 2023

Support looking up MAC code from allele list with `lookup_mac` method.

Support CWD Reduction:
 - add `cwd_redux` method to produce CWD only allele list
 - create `cwd2` table on load
 - `cwd-redux` endpoint to allow CWD reduction

[Changes][1.0.0rc5]


<a name="0.9.2"></a>
# [Fix Pandas dependencies Latest (0.9.2)](https://github.com/nmdp-bioinformatics/py-ard/releases/tag/0.9.2) - 23 Mar 2023

Set to `pandas==1.5.3`

[Changes][0.9.2]


<a name="1.0.0rc4"></a>
# [Documentation Update and Cleanup (1.0.0rc4)](https://github.com/nmdp-bioinformatics/py-ard/releases/tag/1.0.0rc4) - 15 Mar 2023

## What's Changed
* Documentation and cleanup for 1.0 by [@pbashyal-nmdp](https://github.com/pbashyal-nmdp) in https://github.com/nmdp-bioinformatics/py-ard/pull/219


**Full Changelog**: https://github.com/nmdp-bioinformatics/py-ard/compare/1.0.0rc3...1.0.0rc4

[Changes][1.0.0rc4]


<a name="1.0.0rc3"></a>
# [Performance Update (1.0.0rc3)](https://github.com/nmdp-bioinformatics/py-ard/releases/tag/1.0.0rc3) - 07 Mar 2023

This PR gathers all the performance improvements. speed of pyard increased multiple fold. Faster startups.

Update for performance:
- aggressive caching for most used functions
- import pandas only during loading of data
- query for column
- remove use of regex for simple checks
- option to choose cache in batch

Refactor/cleanup:
- make methods private that do not need to be exposed
- wrap with try/catch all calls to load data

[Changes][1.0.0rc3]


<a name="1.0.0rc2"></a>
# [2nd Release Candidate for 1.0 (1.0.0rc2)](https://github.com/nmdp-bioinformatics/py-ard/releases/tag/1.0.0rc2) - 07 Mar 2023

 Supports reduction type of `P` for P-group reduction.

[Changes][1.0.0rc2]


<a name="1.0.0rc1"></a>
# [Release Candidate for 1.0 (1.0.0rc1)](https://github.com/nmdp-bioinformatics/py-ard/releases/tag/1.0.0rc1) - 27 Feb 2023

- A single `redux` does allele and GL String reductions.
- Added API to show broad/splits
- Batchmode allows GL String output
- Set `$TEMPDIR/pyard/` as the default path for storing db files.
- Use `pyard-reduce-csv --generate-sample` to get sample config/input file
- Lots of improvements/features in the CLI tools
- Refactoring of code


[Changes][1.0.0rc1]


<a name="0.9.1"></a>
# [Bug fixes, blend endpoint (0.9.1)](https://github.com/nmdp-bioinformatics/py-ard/releases/tag/0.9.1) - 09 Feb 2023

 - `blend` endpoint added to the service
 - removed `lg` tables and dictionaries.
 - remove `p_group` table
 - store IMGT db version
 - Fix XX errors for broad/splits
 - Fix loading of IMGT DB version 3130

[Changes][0.9.1]


<a name="0.8.2"></a>
# [Shortnulls for exon mode fixed (0.8.2)](https://github.com/nmdp-bioinformatics/py-ard/releases/tag/0.8.2) - 18 Nov 2022

See PR [#183](https://github.com/nmdp-bioinformatics/py-ard/issues/183) to fix [#161](https://github.com/nmdp-bioinformatics/py-ard/issues/161) 

[Changes][0.8.2]


<a name="0.8.1"></a>
# [Ping! Mode and DR Blending (0.8.1)](https://github.com/nmdp-bioinformatics/py-ard/releases/tag/0.8.1) - 03 Oct 2022

PING mode
 - When `ping=True` alleles in P-groups are included in addition to the alleles in G-groups in the corresponding lg/lgx groups.

DR Blending
 - Support DRBX Blending from DRB1
 

[Changes][0.8.1]


<a name="0.8.0"></a>
# [`py-ard` REST Service (0.8.0)](https://github.com/nmdp-bioinformatics/py-ard/releases/tag/0.8.0) - 10 Jun 2022

`py-ard` REST Service
 - REST service with `/redux`, `/validate`, `/mac` endpoints
 - Run in a Docker container


[Changes][0.8.0]


<a name="0.7.7"></a>
# [BugFix for HLA  Prefix (0.7.7)](https://github.com/nmdp-bioinformatics/py-ard/releases/tag/0.7.7) - 19 May 2022

See [#165](https://github.com/nmdp-bioinformatics/py-ard/issues/165) 

[Changes][0.7.7]


<a name="0.7.6"></a>
# [Reduce to Shortnulls (0.7.6)](https://github.com/nmdp-bioinformatics/py-ard/releases/tag/0.7.6) - 29 Mar 2022

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


<a name="0.7.5"></a>
# [Support shortnull (0.7.5)](https://github.com/nmdp-bioinformatics/py-ard/releases/tag/0.7.5) - 26 Mar 2022

Implements **shortnulls** behavior with new config variable set to `True` by default.

This will address things like `DRB4*01:03N` and `DRB5*01:08N` both in terms of accepting them as valid and also by expanding them as appropriate to the list of longer alleles that have the same expression character.

`DRB5*01:08N` is acceptable by **WHO** rules since all suballeles have N.
`DRB4*01:03N` is acceptable by **WMDA** (but not WHO) rules but this needs to be handled for things like HF analysis by expansion to something valid (vs rejection) to avoid bias

[Changes][0.7.5]


<a name="0.7.4"></a>
# [Summary Table for Batch (0.7.4)](https://github.com/nmdp-bioinformatics/py-ard/releases/tag/0.7.4) - 23 Mar 2022

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


<a name="0.7.3"></a>
# [Fix batch regression error (0.7.3)](https://github.com/nmdp-bioinformatics/py-ard/releases/tag/0.7.3) - 21 Mar 2022

 Fix regression error for MAC reduction [#152](https://github.com/nmdp-bioinformatics/py-ard/issues/152) 

[Changes][0.7.3]


<a name="0.7.1.1"></a>
# [Add reduce_2field reduce option (0.7.1.1)](https://github.com/nmdp-bioinformatics/py-ard/releases/tag/0.7.1.1) - 23 Feb 2022

Batch csv `pyard-reduce-csv` takes in `reduce_2field` option to reduce 2 fields alleles like `B*15:220`, `DPB1*104:01` and `A*02:642`

[Changes][0.7.1.1]


<a name="0.7.2"></a>
# [Stricter Data Validation (0.7.2)](https://github.com/nmdp-bioinformatics/py-ard/releases/tag/0.7.2) - 14 Feb 2022

Version `0.7.0` has stricter data validation. It will not silently fail by returning an empty `''` string. It'll return of the  `Invalid` exceptions in `pyard.exceptions` when calling `redux_gl` method with invalid GL String. 

See [CHANGELOG.md](https://github.com/nmdp-bioinformatics/py-ard/blob/master/CHANGELOG.md) for full changelog.

[Changes][0.7.2]


<a name="0.6.11"></a>
# [Fix for IMGT URL Change (0.6.11)](https://github.com/nmdp-bioinformatics/py-ard/releases/tag/0.6.11) - 24 Jan 2022

Fixes a breaking change where all allele lists in IMGTHLA repo have been moved to `/allelelist/` subdirectory.

[Changes][0.6.11]


<a name="0.6.10"></a>
# [Bug fixes for Batch Processing (0.6.10)](https://github.com/nmdp-bioinformatics/py-ard/releases/tag/0.6.10) - 13 Dec 2021

Batch Reduce Fixes:
- Fix Instantiation of `pyard.ARD` object.
- Fix serology check
- Fix issue with P groups
- A new flag `convert_v2_to_v3` to convert v2 to v3 but not reduce.


[Changes][0.6.10]


<a name="0.6.9"></a>
# [pyard-status command to check the status of all tables in the databases (0.6.9)](https://github.com/nmdp-bioinformatics/py-ard/releases/tag/0.6.9) - 27 Sep 2021

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


<a name="0.6.8"></a>
# [Supports WHO and exon Reduction Types (0.6.8)](https://github.com/nmdp-bioinformatics/py-ard/releases/tag/0.6.8) - 24 Sep 2021

- Handle cases when there is no typing and when redux fails.
- added `exon` resolution group 
- added `W` resolution group
- Fix validation issues with empty alleles, NNNNs, and non-allelic values. 
- pyard-import can refresh MACs and rebuild databases

[Changes][0.6.8]


<a name="0.6.6"></a>
# [handle invalid/blank input (0.6.6)](https://github.com/nmdp-bioinformatics/py-ard/releases/tag/0.6.6) - 29 Jul 2021

handle cases with no input and redux fails

[Changes][0.6.6]


<a name="0.6.5"></a>
# [updates to pyard-reduce-csv and unit tests (0.6.5)](https://github.com/nmdp-bioinformatics/py-ard/releases/tag/0.6.5) - 17 Jun 2021


    Use pyard-reduce-csv command to reduce a CSV file based on a JSON config file.
    Use db_version 3440 in unit test to match behave tests
    Re-run the tests again so local db is used.



[Changes][0.6.5]


<a name="0.6.4"></a>
# [DRBX Mapping and Cw Serology (0.6.4)](https://github.com/nmdp-bioinformatics/py-ard/releases/tag/0.6.4) - 16 Jun 2021

 - Map DRB3, DRB4 and DRB5 typings to DRBX. [#82](https://github.com/nmdp-bioinformatics/py-ard/issues/82) 
 - Change C to Cw for serology; [#84](https://github.com/nmdp-bioinformatics/py-ard/issues/84) 
 - Return '' for invalid MACs [#84](https://github.com/nmdp-bioinformatics/py-ard/issues/84) 

[Changes][0.6.4]


<a name="0.6.3"></a>
# [0.6.3 release](https://github.com/nmdp-bioinformatics/py-ard/releases/tag/0.6.3) - 09 Jun 2021

 addresses one-to-many relationship from 2d to lg/lgx

[Changes][0.6.3]


<a name="0.6.2"></a>
# [Fixes serology mappings for broad to include alleles in the split (0.6.2)](https://github.com/nmdp-bioinformatics/py-ard/releases/tag/0.6.2) - 07 Jun 2021

Fixes serology mappings for broad to include alleles in the split.

[Changes][0.6.2]


<a name="0.6.1"></a>
# [V2 to V3 Mapping (0.6.1)](https://github.com/nmdp-bioinformatics/py-ard/releases/tag/0.6.1) - 04 Feb 2021


   - Heuristically predict V3 from V2 when not in exceptional case list
   - Make is_XX a public method on the ARD object
   - Update README and fix bug in pyard-import for importing into Latest


[Changes][0.6.1]


<a name="0.6.0"></a>
# [Nomenclature versioning (0.6.0)](https://github.com/nmdp-bioinformatics/py-ard/releases/tag/0.6.0) - 08 Dec 2020

adds nomenclature versioning, cmdline options, GL string examples

[Changes][0.6.0]


<a name="0.5.1"></a>
# [fix mac expansion (0.5.1)](https://github.com/nmdp-bioinformatics/py-ard/releases/tag/0.5.1) - 30 Nov 2020

Fix serology mapping and mac expansions

[Changes][0.5.1]


<a name="0.4.1"></a>
# [Upgrade Pandas to 1.1.4 (0.4.1)](https://github.com/nmdp-bioinformatics/py-ard/releases/tag/0.4.1) - 03 Nov 2020

Update pandas 1.1.4

   - Pandas `1.1.2` doesn't work with Python 3.9. Upgrade Pandas to `1.1.4` which works with Python 3.8 and 3.9


[Changes][0.4.1]


<a name="0.4.0"></a>
# [Support reduction of serologically typed GL String (0.4.0)](https://github.com/nmdp-bioinformatics/py-ard/releases/tag/0.4.0) - 22 Oct 2020

Uses WMDA `rel_dna_ser.txt` for the corresponding version of IMGT database to produce serology mapping

[Changes][0.4.0]


<a name="0.3.0"></a>
# [Use sqlite3 database for reference data (0.3.0)](https://github.com/nmdp-bioinformatics/py-ard/releases/tag/0.3.0) - 15 Oct 2020

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


<a name="0.2.0"></a>
# [rearrange data in memory (0.2.0)](https://github.com/nmdp-bioinformatics/py-ard/releases/tag/0.2.0) - 14 Oct 2020

This release rearranges how memory is used especially MAC codes and a lot of cleanup.

[Changes][0.2.0]


<a name="0.1.0"></a>
# [load_mac_file flag to load MAC file (0.1.0)](https://github.com/nmdp-bioinformatics/py-ard/releases/tag/0.1.0) - 01 Oct 2020

 Rename download_mac flag

  - Rename `download_mac` ARD flag to `load_mac_file` as it properly describes what it does.
  - Remove dead code
  - Reformat code and fix some comments
  - Version bumped to `0.1.0`
  - Updated `pandas` to `1.1.2`

[Changes][0.1.0]


<a name="0.0.21"></a>
# [fix tests and sorting (0.0.21)](https://github.com/nmdp-bioinformatics/py-ard/releases/tag/0.0.21) - 09 Sep 2020

fixes test and also a bug in 4th field sorting

[Changes][0.0.21]


<a name="0.0.20"></a>
# [allow P and G as input, fix lg and lgx behavior (0.0.20)](https://github.com/nmdp-bioinformatics/py-ard/releases/tag/0.0.20) - 09 Sep 2020

This release fixes the behavior of lg and lgx to always reduce to 2-field.
It also allows P and G alleles as input

[Changes][0.0.20]


<a name="0.0.18"></a>
# [Fixes G-codes expansion (0.0.18)](https://github.com/nmdp-bioinformatics/py-ard/releases/tag/0.0.18) - 29 Jul 2020

Fixes G-codes expansion when smart sorting.

[Changes][0.0.18]


<a name="0.0.17"></a>
# [Specify path for temporary files (0.0.17)](https://github.com/nmdp-bioinformatics/py-ard/releases/tag/0.0.17) - 22 Jul 2020

You can specify path when creating ARD object.
```
ard = ARD('3290', data_dir='/tmp/py-ard')
```

[Changes][0.0.17]


<a name="0.0.16"></a>
# [version 0.0.16](https://github.com/nmdp-bioinformatics/py-ard/releases/tag/0.0.16) - 09 Jul 2020

update MAC location and version to 0.0.16

[Changes][0.0.16]


<a name="0.0.15.0"></a>
# [update to MAC location (0.0.15.0)](https://github.com/nmdp-bioinformatics/py-ard/releases/tag/0.0.15.0) - 28 May 2020



[Changes][0.0.15.0]


<a name="0.0.15"></a>
# [update to MAC location (0.0.15)](https://github.com/nmdp-bioinformatics/py-ard/releases/tag/0.0.15) - 28 May 2020

yes

[Changes][0.0.15]


<a name="0.0.14"></a>
# [0.0.14](https://github.com/nmdp-bioinformatics/py-ard/releases/tag/0.0.14) - 14 Apr 2020

- Support for Python 3.7
- Broad XX enhancement 
- p Performance improvements

[Changes][0.0.14]


[1.0.6]: https://github.com/nmdp-bioinformatics/py-ard/compare/1.0.5...1.0.6
[1.0.5]: https://github.com/nmdp-bioinformatics/py-ard/compare/1.0.4...1.0.5
[1.0.4]: https://github.com/nmdp-bioinformatics/py-ard/compare/1.0.3...1.0.4
[1.0.3]: https://github.com/nmdp-bioinformatics/py-ard/compare/1.0.2...1.0.3
[1.0.2]: https://github.com/nmdp-bioinformatics/py-ard/compare/1.0.1...1.0.2
[1.0.1]: https://github.com/nmdp-bioinformatics/py-ard/compare/1.0.0...1.0.1
[1.0.0]: https://github.com/nmdp-bioinformatics/py-ard/compare/1.0.0rc7...1.0.0
[1.0.0rc7]: https://github.com/nmdp-bioinformatics/py-ard/compare/1.0.0rc6...1.0.0rc7
[1.0.0rc6]: https://github.com/nmdp-bioinformatics/py-ard/compare/1.0.0rc5...1.0.0rc6
[1.0.0rc5]: https://github.com/nmdp-bioinformatics/py-ard/compare/0.9.2...1.0.0rc5
[0.9.2]: https://github.com/nmdp-bioinformatics/py-ard/compare/1.0.0rc4...0.9.2
[1.0.0rc4]: https://github.com/nmdp-bioinformatics/py-ard/compare/1.0.0rc3...1.0.0rc4
[1.0.0rc3]: https://github.com/nmdp-bioinformatics/py-ard/compare/1.0.0rc2...1.0.0rc3
[1.0.0rc2]: https://github.com/nmdp-bioinformatics/py-ard/compare/1.0.0rc1...1.0.0rc2
[1.0.0rc1]: https://github.com/nmdp-bioinformatics/py-ard/compare/0.9.1...1.0.0rc1
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

<!-- Generated by https://github.com/rhysd/changelog-from-release v3.7.1 -->
