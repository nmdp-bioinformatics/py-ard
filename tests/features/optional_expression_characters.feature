Feature: Expression characters are optional

  An allele is valid if it's valid with any expression character or
  without an expression character

  Scenario Outline:

    Given the allele as <Allele>
    When reducing on the <Level> level
    Then the reduced allele is found to be <Redux Allele>

    Examples: expression characters not propagated for C*04:09
      | Allele   | Level | Redux Allele |
      | C*04:09L | lgx   | C*04:01      |
      | C*04:09N | lgx   | C*04:01      |
      | C*04:09  | lgx   | C*04:01      |

    Examples: expression characters not propagated for A*24:329
      | Allele    | Level | Redux Allele |
      | A*24:329N | lgx   | A*24:329Q    |
      | A*24:329Q | lgx   | A*24:329Q    |
      | A*24:329L | lgx   | A*24:329Q    |
      | A*24:329  | lgx   | A*24:329Q    |
