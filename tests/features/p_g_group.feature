Feature: P and G Groups

  Scenario Outline:

    Given the allele as <Allele>
    When reducing on the <Level> level (ambiguous)
    Then the reduced allele is found to be <Redux Allele>

    Examples:
      | Allele      | Level | Redux Allele |
      | A*02:01P    | lgx   | A*02:01      |
      | A*02:01:01G | lgx   | A*02:01      |