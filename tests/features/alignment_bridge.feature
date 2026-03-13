Feature: HLAtools Alignment Bridge

  The HLAToolsBridge wraps the HLAtools R package to provide authoritative
  HLA protein alignment data. Sequences include the full protein (leader +
  mature) as well as the mature region alone (IMGT positions >= 1).

  @hlatools
  Scenario: Bridge reports itself as available

    Given the HLAtools bridge is initialised
    Then the bridge is available

  @hlatools
  Scenario Outline: Full protein sequence length for known alleles

    Given the HLA allele <Allele>
    When looking up the full protein sequence
    Then the full sequence length is <Length>

    Examples:
      | Allele           | Length |
      | DPB1*04:01:01:01 | 258    |
      | DPB1*04:02:01:01 | 258    |
      | DQA1*05:01       | 254    |

  @hlatools
  Scenario Outline: Mature protein sequence is shorter by the leader length

    Given the HLA allele <Allele>
    When looking up full and mature protein sequences
    Then the mature sequence is <Leader> amino acids shorter than the full sequence

    Examples:
      | Allele     | Leader |
      | DQA1*05:01 | 23     |

  @hlatools
  Scenario Outline: Prefix fallback resolves 2-field alleles to the same sequence

    Looking up a 2-field allele (e.g. DPB1*04:01) should return the same
    sequence as the first matching 4-field allele in the alignment.

    Given the HLA allele <Allele>
    When looking up the full protein sequence
    Then the full sequence length is <Length>

    Examples:
      | Allele     | Length |
      | DPB1*04:01 | 258    |
      | DQA1*05:01 | 254    |

  @hlatools
  Scenario Outline: Known allele pair comparison

    Given the HLA allele <Allele1>
    And the second HLA allele <Allele2>
    When comparing the two allele sequences
    Then the comparison yields <Mismatches> amino acid mismatches

    Examples:
      | Allele1          | Allele2          | Mismatches |
      | DPB1*04:01:01:01 | DPB1*04:01:01:01 | 0          |
      | DPB1*04:01:01:01 | DPB1*04:02:01:01 | 4          |
      | DPB1*04:01       | DPB1*04:02       | 4          |

  @hlatools
  Scenario Outline: Position mapping leader and mature counts

    The position mapping maps each 0-based sequence index to its IMGT position
    number. Negative IMGT positions are leader peptide; positive are mature protein.

    Given the locus is <Locus>
    When building the position mapping
    Then the position mapping has <Leader> leader positions and <Mature> mature positions

    Examples:
      | Locus | Leader | Mature |
      | DPB1  | 29     | 244    |

  @hlatools
  Scenario Outline: Invalid allele returns no sequence

    Alleles without a '*' delimiter or empty strings cannot be looked up.
    '(empty)' in the examples table represents an empty string — behave
    cannot represent blank cells directly.

    Given the HLA allele <Allele>
    When looking up the full protein sequence
    Then no sequence is found

    Examples:
      | Allele  |
      | DPB1    |
      | (empty) |
