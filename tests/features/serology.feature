Feature: Serology

  py-ard is able to map serology to the corresponding alleles and reduce to the desired
  level.

  Scenario Outline:

    Given the serology typing is <Serology>
    When reducing on the <Level> level (ambiguous)
    Then the reduced allele is found to be <Redux Allele>


    Examples: Valid A serology typings
      | Serology | Level | Redux Allele                                          |
      | DR1403   | G     | DRB1*14:03:01G/DRB1*14:03:02                          |
      | Cw10     | lg    | C*03:02g/C*03:04g/C*03:06g/C*03:26g/C*03:28g/C*03:46g |
