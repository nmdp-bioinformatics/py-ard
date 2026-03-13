Feature: Transplant Mismatch Analysis

  For solid organ transplant, a mismatch is a donor chromosome whose expressed
  protein sequence is absent from the recipient's set of protein sequences.

  Notation:
    '+' separates the two chromosomes of a diplotype
    '/' separates ambiguous allele alternatives for one chromosome
    Alleles ending in 'N' are null (not expressed) and are never counted as mismatches

  @hlatools
  Scenario Outline: Mismatch count for donor-recipient pairs

    Given the donor genotype <Donor>
    And the recipient genotype <Recipient>
    And the locus is <Locus>
    When analyzing transplant mismatches
    Then the mismatch count is <Count>

    Examples: Unambiguous genotypes
      | Donor                             | Recipient                        | Locus | Count |
      | DPB1*04:01+DPB1*03:01             | DPB1*04:01+DPB1*03:01            | DPB1  | 0     |
      | DPB1*04:01+DPB1*02:01             | DPB1*04:01+DPB1*03:01            | DPB1  | 1     |

    Examples: Null allele in donor — not counted as a mismatch
      | Donor                             | Recipient                        | Locus | Count |
      | DPB1*04:01+DPB1*02:01N            | DPB1*04:01+DPB1*03:01            | DPB1  | 0     |

    Examples: Ambiguous donor chromosome
      | Donor                             | Recipient                        | Locus | Count |
      | DPB1*04:01/DPB1*04:02+DPB1*02:01 | DPB1*04:01+DPB1*03:01            | DPB1  | 1     |

  @hlatools
  Scenario Outline: Per-haplotype status in mismatch analysis

    Given the donor genotype <Donor>
    And the recipient genotype <Recipient>
    And the locus is <Locus>
    When analyzing transplant mismatches
    Then the haplotype <Haplotype> has status <Status>

    Examples: Clear match and mismatch
      | Donor                   | Recipient               | Locus | Haplotype    | Status   |
      | DPB1*04:01+DPB1*02:01   | DPB1*04:01+DPB1*03:01   | DPB1  | DPB1*04:01   | match    |
      | DPB1*04:01+DPB1*02:01   | DPB1*04:01+DPB1*03:01   | DPB1  | DPB1*02:01   | mismatch |

    Examples: Null allele in donor
      | Donor                    | Recipient               | Locus | Haplotype     | Status |
      | DPB1*04:01+DPB1*02:01N   | DPB1*04:01+DPB1*03:01   | DPB1  | DPB1*02:01N   | null   |

    Examples: Ambiguous donor — 04:01 matches but 04:02 full sequence differs → possible_match
      | Donor                              | Recipient               | Locus | Haplotype               | Status         |
      | DPB1*04:01/DPB1*04:02+DPB1*02:01  | DPB1*04:01+DPB1*03:01   | DPB1  | DPB1*04:01/DPB1*04:02   | possible_match |
