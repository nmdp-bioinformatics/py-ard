Feature: P and G Groups

  Scenario Outline:

    Given the allele as <Allele>
    When reducing on the <Level> level (ambiguous)
    Then the reduced allele is found to be <Redux Allele>

    Examples:
      | Allele      | Level | Redux Allele |
      | A*02:01P    | lgx   | A*02:01      |
      | A*02:01:01G | lgx   | A*02:01      |


  Scenario Outline: allele reduction with ping
  `ping` is the default.

  If there is no G group for the allele, it should use the P group allele.

    Given the allele as <Allele>
    When reducing on the <Level> level with ping
    Then the reduced allele is found to be <Redux Allele>

    Examples:
      | Allele  | Level | Redux Allele |
      | C*06:17 | lgx   | C*06:02      |

    Examples: DRB4*01s
      | Allele           | Level | Redux Allele |
      | DRB4*01:03       | lgx   | DRB4*01:01   |
      | DRB4*01:03:01    | lgx   | DRB4*01:01   |
      | DRB4*01:03:02    | lgx   | DRB4*01:01   |
      | DRB4*01:03:03    | lgx   | DRB4*01:01   |
      | DRB4*01:03:04    | lgx   | DRB4*01:01   |
      | DRB4*01:03:05    | lgx   | DRB4*01:01   |
      | DRB4*01:03:06    | lgx   | DRB4*01:01   |
      | DRB4*01:03:07    | lgx   | DRB4*01:01   |
      | DRB4*01:03:08    | lgx   | DRB4*01:01   |
      | DRB4*01:03:09    | lgx   | DRB4*01:01   |
      | DRB4*01:03:10    | lgx   | DRB4*01:01   |
      | DRB4*01:03:11    | lgx   | DRB4*01:01   |
      | DRB4*01:03:12    | lgx   | DRB4*01:01   |
      | DRB4*01:03:13    | lgx   | DRB4*01:01   |
      | DRB4*01:03:14    | lgx   | DRB4*01:01   |
      | DRB4*01:03:15    | lgx   | DRB4*01:01   |
      | DRB4*01:03:16    | lgx   | DRB4*01:01   |
      | DRB4*01:03:17    | lgx   | DRB4*01:01   |
      | DRB4*01:03:18    | lgx   | DRB4*01:01   |
      | DRB4*01:03:19    | lgx   | DRB4*01:01   |
      | DRB4*01:03:20    | lgx   | DRB4*01:01   |
      | DRB4*01:03:21    | lgx   | DRB4*01:01   |
      | DRB4*01:03:22    | lgx   | DRB4*01:01   |
      | DRB4*01:03:23    | lgx   | DRB4*01:01   |
      | DRB4*01:03:24    | lgx   | DRB4*01:01   |
      | DRB4*01:03:25    | lgx   | DRB4*01:01   |
      | DRB4*01:03:26    | lgx   | DRB4*01:01   |
      | DRB4*01:03:27    | lgx   | DRB4*01:01   |
      | DRB4*01:03:28    | lgx   | DRB4*01:01   |
      | DRB4*01:03:29    | lgx   | DRB4*01:01   |
      | DRB4*01:03:30    | lgx   | DRB4*01:01   |
      | DRB4*01:03:31    | lgx   | DRB4*01:01   |
      | DRB4*01:03:32    | lgx   | DRB4*01:01   |
      | DRB4*01:03:33    | lgx   | DRB4*01:01   |
      | DRB4*01:03:34    | lgx   | DRB4*01:01   |
      | DRB4*01:03:35    | lgx   | DRB4*01:01   |
      | DRB4*01:03:01:01 | lgx   | DRB4*01:01   |
      | DRB4*01:03:01:03 | lgx   | DRB4*01:01   |
      | DRB4*01:03:01:04 | lgx   | DRB4*01:01   |
      | DRB4*01:03:01:05 | lgx   | DRB4*01:01   |
      | DRB4*01:03:01:06 | lgx   | DRB4*01:01   |
      | DRB4*01:03:01:07 | lgx   | DRB4*01:01   |
      | DRB4*01:03:01:08 | lgx   | DRB4*01:01   |
      | DRB4*01:03:01:09 | lgx   | DRB4*01:01   |
      | DRB4*01:03:01:10 | lgx   | DRB4*01:01   |
      | DRB4*01:03:01:11 | lgx   | DRB4*01:01   |
      | DRB4*01:03:01:12 | lgx   | DRB4*01:01   |
      | DRB4*01:03:01:14 | lgx   | DRB4*01:01   |
      | DRB4*01:03:01:15 | lgx   | DRB4*01:01   |
      | DRB4*01:03:01:16 | lgx   | DRB4*01:01   |
      | DRB4*01:03:01:17 | lgx   | DRB4*01:01   |
      | DRB4*01:03:01:18 | lgx   | DRB4*01:01   |
      | DRB4*01:03:02:01 | lgx   | DRB4*01:01   |
      | DRB4*01:03:02:02 | lgx   | DRB4*01:01   |

    Examples: C*02:10s
      | Allele     | Level | Redux Allele |
      | C*02:10:02 | lgx   | C*02:02      |
      | C*02:02    | lg    | C*02:02g     |
      | C*02:02    | lgx   | C*02:02      |
      | C*02:10    | lg    | C*02:02g     |
      | C*02:10    | lgx   | C*02:02      |

    Examples: lgx with duplicates
      | Allele        | Level | Redux Allele            |
      | DPA1*02:12    | lgx   | DPA1*02:02/DPA1*02:07   |
      | DPA1*02:12    | lg    | DPA1*02:02g/DPA1*02:07g |
      | DQA1*03:03    | lgx   | DQA1*03:01              |
      | DQA1*03:03    | lg    | DQA1*03:01g             |
      | DQA1*03:03:09 | lg    | DQA1*03:03g             |
