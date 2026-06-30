Feature: Validate Allele

  Scenario Outline: Valid alleles in strict mode

    Given the allele as <Allele>
    When checking if the allele is valid in strict mode
    Then the allele validity is <Validity>

    Examples:
      | Allele          | Validity |
      | A*01:01         | Valid    |
      | A*01:01:01      | Valid    |
      | A*01:01:01:01   | Valid    |
      | B*07:02         | Valid    |
      | C*04:01         | Valid    |
      | DRB1*03:01      | Valid    |
      | DQB1*06:02      | Valid    |
      | A*01:01:01G     | Valid    |
      | B*07:02:01G     | Valid    |
      | A*01:01P        | Valid    |
      | B*07:02P        | Valid    |

  Scenario Outline: Invalid alleles in strict mode

    Given the allele as <Allele>
    When checking if the allele is valid in strict mode
    Then the allele validity is <Validity>

    Examples:
      | Allele          | Validity |
      | A*99:99         | Invalid  |
      | Z*01:01         | Invalid  |
      | A*01:01g        | Invalid  |
      | A*01:01:99G     | Invalid  |

  Scenario Outline: Valid alleles in non-strict mode

    In non-strict mode, alleles with 'g' suffix are considered valid.

    Given the allele as <Allele>
    When checking if the allele is valid in non-strict mode
    Then the allele validity is <Validity>

    Examples:
      | Allele          | Validity |
      | A*01:01         | Valid    |
      | A*01:01:01      | Valid    |
      | A*01:01g        | Valid    |
      | B*07:02g        | Valid    |
      | A*01:01:01G     | Valid    |
      | A*01:01P        | Valid    |

  Scenario Outline: Invalid alleles in non-strict mode

    Given the allele as <Allele>
    When checking if the allele is valid in non-strict mode
    Then the allele validity is <Validity>

    Examples:
      | Allele          | Validity |
      | A*99:99         | Invalid  |
      | Z*01:01         | Invalid  |

  Scenario Outline: Alleles with more than 2 fields fall back to 2-field check

    Given the allele as <Allele>
    When checking if the allele is valid in strict mode
    Then the allele validity is <Validity>

    Examples:
      | Allele            | Validity |
      | A*01:01:01        | Valid    |
      | A*01:01:01:01     | Valid    |
      | A*01:01:99:99     | Valid    |
      | A*99:99:01:01     | Invalid  |

  Scenario Outline: Allele validation in strict mode

    little g alleles are valid in non-strict mode

    Given the allele as <Allele>
    When checking for validity of the allele in strict mode
    Then the validness of the allele is <Validity>

    Examples:
      | Allele        | Validity |
      | A*24:329      | InValid  |
      | DRBX*NNNN     | Invalid  |
      | A*30:02g      | Invalid  |
      | HLA-A*01:04Ng | Invalid  |

  Scenario Outline: Allele validation in non-strict mode

  Similar to reduction, handle non-strict mode when validating an allele.
  The test version of IPD/IMGT-HLA database (see environment.py),
  A*11:403 is invalid and A*24:329 is valid for A*24:329Q

    Given the allele as <Allele>
    When checking for validity of the allele in non-strict mode
    Then the validness of the allele is <Validity>

    Examples:
      | Allele        | Validity |
      | A*11:403      | Invalid  |
      | A*24:329      | Valid    |
      | DRBX*NNNN     | Invalid  |
      | A*30:02g      | Valid    |
      | HLA-A*01:04Ng | Valid    |
