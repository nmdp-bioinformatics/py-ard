Feature: P Groups

  Scenario Outline: Protein-level reduction in *strict* mode

    Given the allele as <Allele>
    When reducing on the <Level> level (ambiguous)
    Then the reduced allele is found to be <Redux Allele>

    Examples:
      | Allele        | Level | Redux Allele |
      | B*44:15:01:01 | P     | B*44:15P     |
      | A*02:01:01    | P     | A*02:01P     |
      | B*07:02       | P     | B*07:02P     |
      | B*07:02:01    | P     | B*07:02P     |
      | B*07:02:01:01 | P     | B*07:02P     |
      | B*15:14       | P     | B*15:14P     |

  Scenario Outline: Protein-level reduction in *non-strict* mode

    Given the allele as <Allele>
    When reducing on the <Level> level in non-strict mode
    Then the reduced allele is found to be <Redux Allele>

    Examples:
      | Allele         | Level | Redux Allele |
      | DQB1*06:02:02G | P     | DQB1*06:02P  |
