Feature: Serology Reduction

  For a GL String, find the serological equivalents
  Serological reduction mode is *S*

  Scenario Outline: Serology Reduction

    Given the allele as <Allele>
    When reducing on the <Level> level with ping
    Then the reduced allele is found to be <Redux Allele>

    Examples:
      | Allele                          | Level | Redux Allele        |
      | A*01:01:01:01                   | S     | A1                  |
      | A*01:01                         | S     | A1                  |
      | A*01:AABJE                      | S     | A1/A36              |
      | A*03:XX                         | S     | A3                  |
      | B*44:02:01:11/B*44:02:01:12     | S     | B12/B44             |
      | B*13:03                         | S     | B13                 |
      | B*13:04                         | S     | B15/B21             |
      | B*15:01/B*15:02/B*15:03/B*15:04 | S     | B15/B62/B70/B72/B75 |
      | B*15:10                         | S     | B15/B70/B71         |
