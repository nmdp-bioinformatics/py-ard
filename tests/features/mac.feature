Feature: MAC (Multiple Allele Code)

  Scenario Outline: Reduxing MAC Codes

    Given the allele as <Allele>
    When reducing on the <Level> level (ambiguous)
    Then the reduced allele is found to be <Redux Allele>


    Examples: MACs with group expansions
      | Allele      | Level | Redux Allele                |
      | A*01:AB     | G     | A*01:01:01G/A*01:02         |
      | A*01:AB     | lgx   | A*01:01/A*01:02             |
      | HLA-A*01:AB | G     | HLA-A*01:01:01G/HLA-A*01:02 |
      | HLA-A*01:AB | lgx   | HLA-A*01:01/HLA-A*01:02     |


    Examples: MACs with allelic expansions
      | Allele          | Level | Redux Allele                                                      |
      | B*08:ASXJP      | G     | B*08:01:01G                                                       |
      | B*08:ASXJP      | lgx   | B*08:01                                                           |
      | C*07:HTGM       | lgx   | C*07:01/C*07:150Q                                                 |
      | A*01:AC+A*01:AB | G     | A*01:01:01G/A*01:02+A*01:01:01G/A*01:03:01G                       |
      | A*01:01+A*01:AB | G     | A*01:01:01G+A*01:01:01G/A*01:02                                   |
      | C*05:APUF       | lg    | X                                                                 |
      | DRB1*13:NA      | lgx   | DRB1*13:01/DRB1*13:02/DRB1*13:06/DRB1*13:08/DRB1*13:09/DRB1*13:10 |

  Scenario Outline: Expand MAC Codes

    Given the MAC code is <MAC>
    When expanding the MAC
    Then the expanded MAC is <Expanded Alleles>

    Examples:
      | MAC           | Expanded Alleles                     |
      | A*01:AB       | A*01:01/A*01:02                      |
      | HLA-A*25:BYHR | HLA-A*25:01/HLA-A*26:01              |
      | HLA-A*02:GNF  | HLA-A*02:01/HLA-A*02:09/HLA-A*02:43N |

  Scenario Outline: Decode to MAC Codes

    Given the allele list is <Expanded Alleles>
    When decoding to a MAC
    Then the decoded MAC is <MAC>

    Examples:
      | Expanded Alleles                     | MAC           |
      | A*01:01/A*01:02                      | A*01:AB       |
      | HLA-A*25:01/HLA-A*26:01              | HLA-A*25:BYHR |
      | HLA-A*02:01/HLA-A*02:09/HLA-A*02:43N | HLA-A*02:GNF  |


  Scenario Outline: Invalid MACs

    Given the MAC code is <MAC>
    When checking for validity of the MAC
    Then the validness is <Validity>

    Examples:
      | MAC          | Validity |
      | DRB1*07:DFJR | Invalid  |
      | DPB1*08:BHHE | Invalid  |
      | A*31:CMZEY   | Invalid  |
