Feature: 1F Reduction
  Reduction to First Field only

  Reduces any allele to its first field (locus + allele group),
  discarding all subsequent fields and any expression suffixes.

  Scenario Outline: Reduce to First Field

    Given the allele as <Allele>
    When reducing on the <Level> level
    Then the reduced allele is found to be <Redux Allele>

    Examples: Multi-field alleles
      | Allele            | Level | Redux Allele |
      | A*01:01:01:01     | 1F    | A*01         |
      | A*01:01:01        | 1F    | A*01         |
      | A*01:01           | 1F    | A*01         |
      | B*07:02:01        | 1F    | B*07         |
      | C*07:02:01:03     | 1F    | C*07         |
      | DRB1*15:01:01:01  | 1F    | DRB1*15      |
      | DQB1*06:02:01     | 1F    | DQB1*06      |
      | DPB1*04:01:01:01  | 1F    | DPB1*04      |

    Examples: Alleles with expression suffixes
      | Allele            | Level | Redux Allele |
      | A*01:04:01:01N    | 1F    | A*01         |
      | B*56:01:01:05S    | 1F    | B*56         |
      | B*39:01:01:02L    | 1F    | B*39         |
      | DRB5*01:08:01N    | 1F    | DRB5*01      |

    Examples: HLA-prefixed alleles
      | Allele            | Level | Redux Allele |
      | HLA-A*01:01:01    | 1F    | HLA-A*01     |
      | HLA-B*07:02:01    | 1F    | HLA-B*07     |
      | HLA-DRB1*15:01:01 | 1F    | HLA-DRB1*15  |
