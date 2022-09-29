Feature: DRB1 blends with DRB3, DRB4, DRB5

  Scenario Outline: DRB1 blends

    Given a subject has <DRB1_SLUG> DRB1 SLUG
    Given a subject has <DRB3> DRB3 allele
    And a subject has <DRB4> DRB4 allele
    And a subject has <DRB5> DRB5 allele
    When I blend the DRBX alleles with DRB1 allele
    Then it should blend as <DRBX_BLEND>

    Examples: All blends with DRB1
      | DRB1_SLUG                 | DRB3       | DRB4       | DRB5       | DRBX_BLEND            |
      | HLA-DRB1*03:01+DRB1*04:01 | DRB3*01:01 | DRB4*01:03 | no         | DRB3*01:01+DRB4*01:03 |
      | HLA-DRB1*03:01+DRB1*04:01 | DRB3*01:01 | DRB4*01:03 | no         | DRB3*01:01+DRB4*01:03 |
      | HLA-DRB1*03:01+DRB1*04:01 | no         | DRB4*01:03 | no         | DRB4*01:03            |
      | HLA-DRB1*03:01+DRB1*04:01 | DRB3*01:03 | no         | no         | DRB3*01:03            |
      | HLA-DRB1*01:01+DRB1*08:01 | no         | no         | no         | nothing               |
      | HLA-DRB1*01:01+DRB1*03:01 | no         | no         | no         | nothing               |
      | HLA-DRB1*01:01+DRB1*04:01 | no         | no         | no         | nothing               |
      | HLA-DRB1*03:01+DRB1*13:01 | DRB3*01:01 | no         | no         | DRB3*01:01            |
      | HLA-DRB1*15:01+DRB1*16:01 | no         | no         | DRB5*01:03 | DRB5*01:03            |

  Scenario Outline: DRB1 doesn't blend

    Given a subject has <DRB1_SLUG> DRB1 SLUG
    Given a subject has <DRB3> DRB3 allele
    And a subject has <DRB4> DRB4 allele
    And a subject has <DRB5> DRB5 allele
    When I blend the DRBX alleles with DRB1 allele, it shouldn't blend
    Then <Expected> was expected, but found <Found>

    Examples: Doesn't blend with DRB1
      | DRB1_SLUG                 | DRB3                  | DRB4                  | DRB5       | Expected | Found    |
      | HLA-DRB1*03:01+DRB1*04:01 | DRB3*01:01            | DRB4*01:03            | DRB5*01:05 | none     | DRB5     |
      | HLA-DRB1*03:01+DRB1*04:01 | DRB3*01:01+DRB3*02:01 | DRB4*01:03            | no         | hom      | DRB3 het |
      | HLA-DRB1*03:01+DRB1*04:01 | DRB3*01:01            | DRB4*01:03+DRB4*01:05 | no         | hom      | DRB4 het |
      | HLA-DRB1*01:01+DRB1*08:01 | DRB3*01:01            | no                    | no         | none     | DRB3     |
      | HLA-DRB1*01:01+DRB1*08:01 | no                    | DRB4*01:01            | no         | none     | DRB4     |
      | HLA-DRB1*01:01+DRB1*08:01 | no                    | no                    | DRB5*01:01 | none     | DRB5     |
      | HLA-DRB1*01:01+DRB1*03:01 | DRB3*01:01            | DRB4*01:03            | no         | none     | DRB4     |
      | HLA-DRB1*01:01+DRB1*03:01 | DRB3*01:01            | no                    | DRB5*01:03 | none     | DRB5     |
      | HLA-DRB1*01:01+DRB1*04:01 | no                    | DRB4*01:01+DRB4*01:03 | no         | hom      | DRB4 het |
      | HLA-DRB1*01:01+DRB1*04:01 | DRB3*01:01            | DRB4*01:03            | no         | none     | DRB3     |
      | HLA-DRB1*01:01+DRB1*04:01 | no                    | DRB4*01:01            | DRB5*01:03 | none     | DRB5     |
      | HLA-DRB1*03:01+DRB1*13:01 | DRB3*01:01            | DRB4*01:03            | no         | none     | DRB4     |
      | HLA-DRB1*03:01+DRB1*13:01 | DRB3*01:01            | no                    | DRB5*01:03 | none     | DRB5     |
      | HLA-DRB1*03:01+DRB1*13:01 | no                    | DRB4*01:01            | DRB5*01:03 | none     | DRB4     |
      | HLA-DRB1*04:01+DRB1*09:01 | DRB3*01:01            | no                    | no         | none     | DRB3     |
      | HLA-DRB1*04:01+DRB1*09:01 | DRB3*01:01            | DRB4*01:03            | no         | none     | DRB3     |
      | HLA-DRB1*04:01+DRB1*09:01 | DRB3*01:01            | no                    | DRB5*01:03 | none     | DRB3     |
      | HLA-DRB1*15:01+DRB1*16:01 | no                    | DRB4*01:01            | DRB5*01:03 | none     | DRB4     |
      | HLA-DRB1*15:01+DRB1*16:01 | DRB3*01:01            | no                    | no         | none     | DRB3     |
      | HLA-DRB1*15:01+DRB1*16:01 | DRB3*01:01            | DRB4*01:03            | no         | none     | DRB3     |
      | HLA-DRB1*15:01+DRB1*16:01 | DRB3*01:01            | no                    | DRB5*01:03 | none     | DRB3     |
      | HLA-DRB1*15:01+DRB1*16:01 | no                    | DRB4*01:01            | DRB5*01:03 | none     | DRB4     |
