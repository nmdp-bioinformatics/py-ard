Feature: Serology

  py-ard is able to map serology to the corresponding alleles and reduce to the desired
  level.

  Scenario Outline:

    Given the serology typing is <Serology>
    When reducing on the <Level> level (ambiguous)
    Then the reduced allele is found to be <Redux Allele>


    Examples: Valid A serology typings
      | Serology | Level | Redux Allele                                                |
      | A*10     | G     | A*26:01:01G/A*26:10/A*26:15/A*26:92/A*66:01:01G/A*66:03:01G |
      | A*10     | lg    | A*26:01g/A*26:10g/A*26:15g/A*26:92g/A*66:01g/A*66:03g       |
      | A*10     | lgx   | A*26:01/A*26:10/A*26:15/A*26:92/A*66:01/A*66:03             |

    Examples: With HLA- prefix
      | Serology    | Level | Redux Allele                                                                        |
      | HLA-A*10    | G     | HLA-A*26:01:01G/HLA-A*26:10/HLA-A*26:15/HLA-A*26:92/HLA-A*66:01:01G/HLA-A*66:03:01G |
      | HLA-B*15:03 | G     | HLA-B*15:03:01G                                                                     |
      | HLA-DQB1*1  | G     | HLA-DQB1*06:11:01/HLA-DQB1*06:11:02/HLA-DQB1*06:11:03/HLA-DQB1*06:12                |
      | HLA-DQB1*1  | lg    | HLA-DQB1*06:11g/HLA-DQB1*06:12g                                                     |
