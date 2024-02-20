Feature: Serology Reduction

  For a GL String, find the serological equivalents
  Serological reduction mode is *S*

  Scenario Outline: Serology Reduction

    Given the allele as <Allele>
    When reducing on the <Level> level with ping
    Then the reduced allele is found to be <Redux Serology>

    Examples: Alleles to Serology
      | Allele                      | Level | Redux Serology |
      | A*01:01:01:01               | S     | A1             |
      | A*01:01                     | S     | A1             |
      | A*01:AABJE                  | S     | A1/A36         |
      | A*03:XX                     | S     | A3             |
      | B*44:02:01:11/B*44:02:01:12 | S     | B12/B44        |
      | B*13:03                     | S     | B13            |
      | B*13:04                     | S     | B15/B21        |

    Examples: Serology Sorted Properly
      | Allele                                   | Level | Redux Serology      |
      | B*15:01/B*15:02/B*15:03/B*15:04          | S     | B15/B62/B70/B72/B75 |
      | B*15:10                                  | S     | B15/B70/B71         |
      | A*24:03/A*24:10/A*24:23/A*24:33/A*24:374 | S     | A9/A24/A2403        |


    Examples:  Skip Loci that don't have Serology mappings
      | Allele                                                                          | Level | Redux Serology      |
      | A*01:01+A*01:01^B*08:ASXJP+B*07:02^C*02:02+C*07:HTGM^DPB1*28:01:01G+DPB1*296:01 | S     | A1+A1^B7+B8^Cw2+Cw7 |

    Examples: 2 field Serology Reduction uses lgx version of serology mapping

      | Allele        | Level | Redux Serology |
      | DRB1*07:34    | S     | DR7            |
      | DRB1*07:34:01 | S     | DR7            |
      | DRB1*07:34:02 | S     | DR7            |
      | DRB4*01:03N   | S     | X              |
