Feature: Mature Protein Redux (M Redux)

  Alleles that differ only in the leader peptide (exon 1, IMGT positions < 1)
  present the same mature protein to the immune system and are clinically
  equivalent. M redux collapses such groups down to the first representative
  allele annotated with '[M]'.

  Alleles that differ in the mature protein are kept as separate representatives.
  A single-allele group or a group of one is returned unchanged.

  An allele is never collapsed if:
    - its mature sequence is None (no reference sequence available in HLAtools), OR
    - its mature sequence contains '*' (one or more positions are unsequenced in the
      alignment); unknown positions mean protein identity cannot be confirmed.

  @hlatools
  Scenario Outline: M redux collapses alleles with identical mature protein

    Given the ambiguous allele group <Group>
    When applying M redux for locus <Locus>
    Then the M redux result is <Result>

    Examples: Pairs of alleles with the same mature protein
      | Group                    | Locus | Result          |
      | DQA1*05:01/DQA1*05:05   | DQA1  | DQA1*05:01[M]   |

    Examples: Single allele — no collapsing possible
      | Group       | Locus | Result      |
      | DQA1*05:01  | DQA1  | DQA1*05:01  |

    Examples: Alleles with different mature proteins — kept separate
      | Group                   | Locus | Result                  |
      | DQA1*05:01/DQA1*05:09  | DQA1  | DQA1*05:01/DQA1*05:09  |
      | DQA1*05:01/DQA1*05:11  | DQA1  | DQA1*05:01/DQA1*05:11  |
      | DQA1*05:01/DQA1*05:38  | DQA1  | DQA1*05:01/DQA1*05:38  |

    Examples: Full DQA1*05:xx group — partial collapsing
      | Group                                                                                      | Locus | Result                                                                        |
      | DQA1*05:01/DQA1*05:05/DQA1*05:09/DQA1*05:11/DQA1*05:13/DQA1*05:35/DQA1*05:38/DQA1*05:41 | DQA1  | DQA1*05:01[M]/DQA1*05:09/DQA1*05:11/DQA1*05:35/DQA1*05:38/DQA1*05:41 |

    Examples: Allele with no reference sequence — kept as a separate entry
      # DQA1*99:99 has no sequence at all in HLAtools (bridge returns None).
      # It cannot be evaluated and must remain unchanged.
      | Group                              | Locus | Result                    |
      | DQA1*05:01/DQA1*05:05/DQA1*99:99  | DQA1  | DQA1*05:01[M]/DQA1*99:99 |

    Examples: Allele with unsequenced positions ('*') — kept as a separate entry
      # DQA1*05:35 has a reference but its mature sequence contains '*' characters
      # (unsequenced positions in the HLAtools alignment, e.g. *****DHVASYGVNLYQ...).
      # Because one or more positions are unknown, protein identity cannot be confirmed
      # and the allele must remain separate — even if the known suffix matches another allele.
      | Group                    | Locus | Result                  |
      | DQA1*05:01/DQA1*05:35   | DQA1  | DQA1*05:01/DQA1*05:35  |

    Examples: DQB1 — allele with unsequenced positions stays separate from complete allele
      # DQB1*05:01:02 and *05:01:03 have unsequenced exons (shown as ***** in the
      # HLAtools alignment). Because one or more positions are unknown, they cannot
      # be confirmed as protein-identical and remain as separate entries.
      | Group                                                          | Locus | Result                                           |
      | DQB1*05:01:01:01/DQB1*05:01:02                                | DQB1  | DQB1*05:01:01:01/DQB1*05:01:02                  |
      | DQB1*05:01:01:01/DQB1*05:01:02/DQB1*05:01:03                 | DQB1  | DQB1*05:01:01:01/DQB1*05:01:02/DQB1*05:01:03   |

    Examples: DRB1 — allele with unsequenced positions stays separate from complete allele
      # DRB1*01:01:03 has an unsequenced exon (contains '*') → stays separate.
      | Group                                  | Locus | Result                              |
      | DRB1*01:01:01:01/DRB1*01:01:03        | DRB1  | DRB1*01:01:01:01/DRB1*01:01:03     |
