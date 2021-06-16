Feature: MAC (Multiple Allele Code)

  Scenario Outline:

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
      | Allele          | Level | Redux Allele                                |
      | B*08:ASXJP      | G     | B*08:01:01G                                 |
      | B*08:ASXJP      | lgx   | B*08:01                                     |
      | C*07:HTGM       | lgx   | C*07:01/C*07:150Q                           |
      | A*01:AC+A*01:AB | G     | A*01:01:01G/A*01:02+A*01:01:01G/A*01:03:01G |
      | A*01:01+A*01:AB | G     | A*01:01:01G+A*01:01:01G/A*01:02             |
      | C*05:APUF       | lg    | X                                           |
