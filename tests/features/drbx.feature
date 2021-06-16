Feature: DRBX Mapping

  Create a single DRBX genotype from DRB3, DRB4, DRB5 alleles

  Scenario Outline:

    Given a subject has <DRB3_Type1> and <DRB3_Type2> DRB3 alleles
    And a subject has <DRB4 Type1> and <DRB4 Type2> DRB4 alleles
    And a subject has <DRB5 Type1> and <DRB5 Type2> DRB5 alleles
    When I create a DRBX genotype
    Then it should be <DRBX_Type1> and <DRBX_Type2>

    Examples: All NNNS
      | DRB3_Type1 | DRB3_Type2 | DRB4 Type1 | DRB4 Type2 | DRB5 Type1 | DRB5 Type2 | DRBX_Type1 | DRBX_Type2 |
      | DRB3*NNNN  | x          | DRB4*NNNN  | x          | DRB5*NNNN  | x          | DRBX*NNNN  | DRBX*NNNN  |
      | DRB3*NNNN  | x          | x          | x          | x          | x          | DRBX*NNNN  | DRBX*NNNN  |
      | DRB3*NNNN  | x          | DRB4*NNNN  | x          | x          | x          | DRBX*NNNN  | DRBX*NNNN  |

    Examples: Some NNNS
      | DRB3_Type1 | DRB3_Type2 | DRB4 Type1 | DRB4 Type2 | DRB5 Type1 | DRB5 Type2 | DRBX_Type1 | DRBX_Type2 |
      | DRB3*02:02 | x          | x          | x          | x          | x          | DRB3*02:02 | DRBX*NNNN  |
      | DRB3*02:02 | x          | DRB4*01:01 | x          | DRB5*NNNN  | x          | DRB3*02:02 | DRB4*01:01 |

    Examples: No NNNS
      | DRB3_Type1 | DRB3_Type2 | DRB4 Type1 | DRB4 Type2 | DRB5 Type1 | DRB5 Type2 | DRBX_Type1 | DRBX_Type2 |
      | DRB3*02:02 | x          | DRB4*01:01 | x          | x          | x          | DRB3*02:02 | DRB4*01:01 |
      | DRB3*02:02 | DRB3*01:01 | x          | x          | x          | x          | DRB3*02:02 | DRB3*01:01 |
      | DRB3*01:01 | x          | DRB4*01:01 | x          | x          | x          | DRB3*01:01 | DRB4*01:01 |

    Examples: Homozygous
      | DRB3_Type1 | DRB3_Type2 | DRB4 Type1 | DRB4 Type2 | DRB5 Type1 | DRB5 Type2 | DRBX_Type1 | DRBX_Type2 |
      | DRB3*02:02 | DRB3*02:02 | x          | x          | x          | x          | DRB3*02:02 | x          |
