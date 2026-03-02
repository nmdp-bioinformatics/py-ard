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

    Examples: Ambiguous recipient where the two alternatives are NOT protein-identical
      # DPB1*04:02 and DPB1*03:01 have different protein sequences (they differ at
      # position 207). The two recipient phasings therefore produce different AAMM sets.
      | Donor                    | Recipient                         | Locus | Identical | Distinct |
      | DPB1*126:01+DPB1*105:01  | DPB1*04:01+DPB1*04:02/DPB1*03:01 | DPB1  | False     | 2        |

    Examples: Ambiguous donor where all phasing combinations yield the same AAMM set
      # DPB1*04:01 and DPB1*126:01 are protein-identical; DPB1*04:02 and DPB1*105:01
      # are protein-identical. Every combination of donor × recipient phasing gives the
      # same (empty) AAMM set — the clinical assessment is unambiguous.
      | Donor                                  | Recipient                | Locus | Identical | Distinct |
      | DPB1*04:01/126:01+DPB1*04:02/105:01   | DPB1*126:01+DPB1*105:01 | DPB1  | True      | 1        |

    Examples: Ambiguous chr1 with different proteins — two distinct AAMM sets
      # DPB1*01:01 and DPB1*02:01 have different protein sequences. The two chr1
      # alternatives produce different AAMM sets against the recipient → False/2.
      | Donor                                           | Recipient                              | Locus | Identical | Distinct |
      | DPB1*01:01:01:01/02:01:02:01+DPB1*03:01:01:01  | DPB1*04:01:01:01+DPB1*04:02:01:01  | DPB1  | False     | 2        |

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
