Feature: Identical AAMM (Amino Acid Mismatch Match)

  When donor and recipient genotypes are ambiguous, there may be several
  possible true phasings. The identical AAMM check determines whether every
  combination of donor × recipient phasing produces the same set of amino acid
  mismatches. If so, the clinical assessment is unambiguous regardless of which
  alleles are actually present.

  An AAMM set is the set of (sequence_position, donor_amino_acid) pairs for
  every position where the donor amino acid is absent from all recipient alleles
  at that position.

  @hlatools
  Scenario Outline: Identical AAMM check for donor-recipient pairs

    Given the donor genotype <Donor>
    And the recipient genotype <Recipient>
    And the locus is <Locus>
    When checking for identical AAMM
    Then the AAMM is identical: <Identical>
    And the number of distinct AAMM sets is <Distinct>

    Examples: Unambiguous — single combination, trivially identical
      | Donor                    | Recipient                         | Locus | Identical | Distinct |
      | DPB1*126:01+DPB1*105:01  | DPB1*04:01+DPB1*04:02             | DPB1  | True      | 1        |

    Examples: Ambiguous recipient where different resolutions yield different AAMM sets
      | Donor                    | Recipient                         | Locus | Identical | Distinct |
      | DPB1*126:01+DPB1*105:01  | DPB1*04:01+DPB1*04:02/DPB1*03:01 | DPB1  | False     | 2        |

  @hlatools
  Scenario: AAMM positions for an unambiguous pair

    For the donor DPB1*126:01+DPB1*105:01 against recipient DPB1*04:01+DPB1*04:02,
    the union of recipient amino acids at every position covers all donor amino acids,
    so the AAMM set is empty (0 positions).

    Given the donor genotype DPB1*126:01+DPB1*105:01
    And the recipient genotype DPB1*04:01+DPB1*04:02
    And the locus is DPB1
    When checking for identical AAMM
    Then the number of common AAMM positions is 0
