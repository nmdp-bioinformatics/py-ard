Feature: Mature Protein Redux (M Redux)

  Alleles that differ only in the leader peptide (exon 1, IMGT positions < 1)
  present the same mature protein to the immune system and are clinically
  equivalent. M redux collapses such groups down to the first representative
  allele annotated with '[M]'.

  Alleles that differ in the mature protein are kept as separate representatives.
  A single-allele group or a group of one is returned unchanged.

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
      # DQA1*99:99 has no sequence in HLAtools; it cannot be evaluated for mature-protein
      # equivalence and must remain unchanged in the output rather than being dropped.
      | Group                              | Locus | Result                    |
      | DQA1*05:01/DQA1*05:05/DQA1*99:99  | DQA1  | DQA1*05:01[M]/DQA1*99:99 |

    Examples: DQB1 — partial allele (unsequenced exon) stays separate from complete allele
      # DQB1*05:01:02 and *05:01:03 have unsequenced exons (shown as ***** in the
      # HLAtools alignment). Because their sequences cannot be fully evaluated they
      # remain as separate entries rather than being collapsed with the complete allele.
      | Group                                                          | Locus | Result                                           |
      | DQB1*05:01:01:01/DQB1*05:01:02                                | DQB1  | DQB1*05:01:01:01/DQB1*05:01:02                  |
      | DQB1*05:01:01:01/DQB1*05:01:02/DQB1*05:01:03                 | DQB1  | DQB1*05:01:01:01/DQB1*05:01:02/DQB1*05:01:03   |

    Examples: DRB1 — partial allele stays separate from complete allele
      # DRB1*01:01:03 has an unsequenced exon → stays separate.
      | Group                                  | Locus | Result                              |
      | DRB1*01:01:01:01/DRB1*01:01:03        | DRB1  | DRB1*01:01:01:01/DRB1*01:01:03     |
