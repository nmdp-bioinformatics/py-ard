Feature: Alleles

  Scenario Outline: allele reduction with ping

    Given the allele as <Allele>
    When reducing on the <Level> level with ping
    Then the reduced allele is found to be <Redux Allele>

    Examples:
      | Allele  | Level | Redux Allele |
      | C*02:02 | lg    | C*02:02g     |
      | C*02:02 | lgx   | C*02:02      |
      | C*02:10 | lg    | C*02:02g     |
      | C*02:10 | lgx   | C*02:02      |
      | C*06:17 | lgx   | C*06:02      |

  Scenario Outline: allele reduction

    Given the allele as <Allele>
    When reducing on the <Level> level
    Then the reduced allele is found to be <Redux Allele>

    Examples:
      | Allele         | Level | Redux Allele    |
      | A*01:01:01     | G     | A*01:01:01G     |
      | A*01:01:01     | lg    | A*01:01g        |
      | A*01:01:01     | lgx   | A*01:01         |

      | HLA-A*01:01:01 | G     | HLA-A*01:01:01G |
      | HLA-A*01:01:01 | lg    | HLA-A*01:01g    |
      | HLA-A*01:01:01 | lgx   | HLA-A*01:01     |

      | DRB1*14:05:01  | lgx   | DRB1*14:05      |
      | DRB1*14:05:01  | lg    | DRB1*14:05g     |

      | DRB1*14:06:01  | lgx   | DRB1*14:06      |
      | DRB1*14:06:01  | lg    | DRB1*14:06g     |
      | C*02:02        | lg    | C*02:02g        |
      | C*02:02        | lgx   | C*02:02         |
      | C*02:10        | lg    | C*02:02g        |
      | C*02:10        | lgx   | C*02:02         |
      | C*06:17        | lgx   | C*06:17         |


  Scenario Outline: allele reduction with ARS suffix

  In `g` mode, use `ARS` prefix rather than `g`.

    Given the allele as <Allele>
    When reducing on the <Level> level with ARS suffix enabled
    Then the reduced allele is found to be <Redux Allele>

    Examples:
      | Allele         | Level | Redux Allele   |
      | A*01:01:01     | lg    | A*01:01ARS     |
      | HLA-A*01:01:01 | lg    | HLA-A*01:01ARS |
      | DRB1*14:06:01  | lg    | DRB1*14:06ARS  |
      | C*02:02        | lg    | C*02:02ARS     |
      | C*02:10        | lg    | C*02:02ARS     |

  Scenario Outline: Allele reduction in non-strict mode

  The canon of HLA Nomenclature includes Deleted Alleles like A*24:329 that were renamed to add an expression character. https://hla.alleles.org/alleles/deleted.html
  Such alleles can be included by using non-strict mode where py-ard will try alleles with expression characters when the original allele is not valid

    Given the allele as <Allele>
    When reducing on the <Level> level in non-strict mode
    Then the reduced allele is found to be <Redux Allele>

    Examples:
      | Allele      | Level | Redux Allele |
      | A*24:329    | lgx   | A*24:329Q    |
      | DQB1*03:276 | lgx   | DQB1*03:01   |

  Scenario Outline: Allele validation in non-strict mode

    Similar to reduction, handle non-strict mode when validating an allele.
    The test version of IPD/IMGT-HLA database (see environment.py),
    A*11:403 is invalid and A*24:329 is valid for A*24:329Q

    Given the allele as <Allele>
    When checking for validity of the allele in non-strict mode
    Then the validness of the allele is <Validity>

    Examples:
      | Allele   | Validity |
      | A*11:403 | Invalid  |
      | A*24:329 | Valid    |


  Scenario Outline: Single field MICA, MICB Alleles

  For MICA, MICB alleles with single field, their reduced version is self.

    Given the allele as <Allele>
    When reducing on the <Level> level
    Then the reduced allele is found to be <Redux Allele>

    Examples:
      | Allele   | Level | Redux Allele |
      | HFE*002  | lgx   | HFE*002      |
      | MICA*040 | lgx   | MICA*040     |
      | MICB*006 | lgx   | MICB*006     |
      | MICB*029 | lgx   | MICB*029     |
