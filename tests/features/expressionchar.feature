Feature: Expression characters

  Scenario Outline: WHO expansion

    Given the typing is <Allele>
    When expanding at the <Level> level
    Then the expanded allele is found to be <Expanded Alleles>

    Examples:
      | Allele            | Level | Expanded Alleles |
      | DRB4*01:03N       | W     | DRB4*01:03:01:02N/DRB4*01:03:01:13N |
      | DRB4*01:03:01N    | W     | DRB4*01:03:01:02N/DRB4*01:03:01:13N |
      | DRB4*01:03:01:02N | W     | DRB4*01:03:01:02N |
      | A*24:02L          | W     | A*24:02:01:02L |
      | A*24:02:01L       | W     | A*24:02:01:02L |
      | A*24:02:01:02L    | W     | A*24:02:01:02L |


  Scenario Outline: Exon redux

    Given the typing is <Allele>
    When expanding at the <Level> level
    Then the expanded allele is found to be <Expanded Alleles>

    Examples:
      | Allele            | Level | Expanded Alleles |
      | DRB4*01:03N       | exon  | DRB4*01:03:01 |
      | DRB4*01:03:01N    | exon  | DRB4*01:03:01 |
      | DRB4*01:03:01:02N | exon  | DRB4*01:03:01 |
      | A*24:02L          | exon  | A*24:02:01  |
      | A*24:02:01L       | exon  | A*24:02:01 |
      | A*24:02:01:02L    | exon  | A*24:02:01 |

  Scenario Outline: lgx reduction

    Given the allele as <Allele>
    When reducing on the <Level> level (ambiguous)
    Then the reduced allele is found to be <Redux Allele>

    Examples:
      | Allele            | Level | Redux Allele |
      | DRB4*01:03N       | lgx   | DRB4*01:01 |
      | DRB4*01:03:01N    | lgx   | DRB4*01:01 |
      | DRB4*01:03:01:02N | lgx   | DRB4*01:01 |
      | A*24:02L          | lgx   | A*24:02 |
      | A*24:02:01L       | lgx   | A*24:02 |
      | A*24:02:01:02L    | lgx   | A*24:02 |

  Scenario Outline: lg reduction

    Given the allele as <Allele>
    When reducing on the <Level> level (ambiguous)
    Then the reduced allele is found to be <Redux Allele>

    Examples:
      | Allele            | Level | Redux Allele |
      | DRB4*01:03N       | lg    | DRB4*01:01g |
      | DRB4*01:03:01N    | lg    | DRB4*01:01g |
      | DRB4*01:03:01:02N | lg    | DRB4*01:01g |
      | A*24:02L          | lg    | A*24:02g |
      | A*24:02:01L       | lg    | A*24:02g |
      | A*24:02:01:02L    | lg    | A*24:02g |

  Scenario Outline: G reduction

    Given the allele as <Allele>
    When reducing on the <Level> level (ambiguous)
    Then the reduced allele is found to be <Redux Allele>

    Examples:
      | Allele            | Level | Redux Allele |
      | DRB4*01:03N       | G     | DRB4*01:01:01G |
      | DRB4*01:03:01N    | G     | DRB4*01:01:01G |
      | DRB4*01:03:01:02N | G     | DRB4*01:01:01G |
      | A*24:02L          | G     | A*24:02:01G |
      | A*24:02:01L       | G     | A*24:02:01G |
      | A*24:02:01:02L    | G     | A*24:02:01G |
