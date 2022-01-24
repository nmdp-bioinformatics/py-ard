Feature: U2 Reduction
  Unambiguous Reduction to 2 fields

  For cases when we want 2 field reduction, but we don't want additional
  ambiguity with G group reduction.
  In general:
  - If the 2 field reduction is unambiguous, reduce to 2 field level
  - If ambiguous, reduce to G group level

  # See Issue 121 for discussion
  # https://github.com/nmdp-bioinformatics/py-ard/issues/121

  Scenario Outline: Reduce to 2 Unambiguous feilds

    Given the allele as <Allele>
    When reducing on the <Level> level
    Then the reduced allele is found to be <Redux Allele>

    Examples: Unambiguous Reductions
      | Allele         | Level | Redux Allele |
      | A*01:04:01:01N | U2    | A*01:04N     |
      | A*01:04:01:02N | U2    | A*01:04N     |

      | A*01:52:01N    | U2    | A*01:52N     |
      | A*01:52:02N    | U2    | A*01:52N     |

      | DRB5*01:08:01N | U2    | DRB5*01:08N  |
      | DRB5*01:08:02N | U2    | DRB5*01:08N  |

      | B*56:01:01:05S | U2    | B*56:01S     |
      | B*39:01:01:02L | U2    | B*39:01L     |


    Examples: Ambiguous Reductions
      | Allele                  | Level | Redux Allele |
      | B*44:66                 | U2    | B*44:66      |
      | B*44:270:01             | U2    | B*44:270     |

      | B*44:270:01/B*44:270:02 | U2    | B*44:270     |

      | B*44:66:01/B*44:66:02   | U2    | B*44:66      |