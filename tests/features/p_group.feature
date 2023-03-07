Feature: P Groups

  Scenario Outline:

    Given the allele as <Allele>
    When reducing on the <Level> level (ambiguous)
    Then the reduced allele is found to be <Redux Allele>

    Examples:
      | Allele        | Level | Redux Allele |
      | B*44:15:01:01 | P     | B*44:15P     |
      | A*02:01:01    | P     | A*02:01:01   |
