Feature: Alleles

  Scenario Outline: allele reduction with ping

    Given the allele as <Allele>
    When reducing on the <Level> level with ping
    Then the reduced allele is found to be <Redux Allele>

    Examples:
      | Allele         | Level | Redux Allele      |
      | C*02:02        | lg    | C*02:02g          |
      | C*02:02        | lgx   | C*02:02           |
      | C*02:10        | lg    | C*02:02g          |
      | C*02:10        | lgx   | C*02:02           |
      | C*06:17        | lgx   | C*06:02           |

  Scenario Outline: allele reduction

    Given the allele as <Allele>
    When reducing on the <Level> level
    Then the reduced allele is found to be <Redux Allele>

    Examples:
      | Allele         | Level | Redux Allele      |
      | A*01:01:01     | G     | A*01:01:01G       |
      | A*01:01:01     | lg    | A*01:01g          |
      | A*01:01:01     | lgx   | A*01:01           |

      | HLA-A*01:01:01 | G     | HLA-A*01:01:01G   |
      | HLA-A*01:01:01 | lg    | HLA-A*01:01g      |
      | HLA-A*01:01:01 | lgx   | HLA-A*01:01       |

      | DRB1*14:05:01  | lgx   | DRB1*14:05        |
      | DRB1*14:05:01  | lg    | DRB1*14:05g       |

      | DRB1*14:06:01  | lgx   | DRB1*14:06        |
      | DRB1*14:06:01  | lg    | DRB1*14:06g       |
      | C*02:02        | lg    | C*02:02g          |
      | C*02:02        | lgx   | C*02:02           |
      | C*02:10        | lg    | C*02:02g          |
      | C*02:10        | lgx   | C*02:02           |
      | C*06:17        | lgx   | C*06:17           |
