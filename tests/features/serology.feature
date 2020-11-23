Feature: Serology

  py-ard is able to map serology to the corresponding alleles and reduce to the desired
  level.

  Scenario Outline:

    Given the serology typing is <Serology>
    When reducing on the <Level> level (ambiguous)
    Then the reduced allele is found to be <Redux Allele>


    Examples: Valid A serology typings
      | Serology | Level | Redux Allele                                                |
      | A10      | G     | A*26:01:01G/A*26:10/A*26:15/A*26:92/A*66:01:01G/A*66:03:01G |
      | A10      | lg    | A*26:01g/A*26:10g/A*26:15g/A*26:92g/A*66:01g/A*66:03g       |
      | A10      | lgx   | A*26:01/A*26:10/A*26:15/A*26:92/A*66:01/A*66:03             |
      | A19      | G     | A*02:65/A*33:09                                             |
      | DR1403   | G     | DRB1*14:03:01/DRB1*14:03:02                                 |
      | DR2      | G     | DRB1*15:08/DRB1*16:03                                       |
