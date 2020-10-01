Feature: MAC (Multiple Allele Code)

  Scenario Outline:

    Given the allele as <Allele>
    When reducing on the <Level> level (ambiguous)
    Then the reduced allele is found to be <Redux Allele>

    Examples:
      | Allele      | Level | Redux Allele                |
      | A*01:AB     | G     | A*01:01:01G/A*01:02         |
      | A*01:AB     | lgx   | A*01:01/A*01:02             |
      | HLA-A*01:AB | G     | HLA-A*01:01:01G/HLA-A*01:02 |
      | HLA-A*01:AB | lgx   | HLA-A*01:01/HLA-A*01:02     |