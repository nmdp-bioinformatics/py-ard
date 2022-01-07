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
      | DRB4*01:03N       | exon  | DRB4*01:03:01/DRB4*01:03:02/DRB4*01:03:03/DRB4*01:03:04/DRB4*01:03:05/DRB4*01:03:06/DRB4*01:03:07/DRB4*01:03:08/DRB4*01:03:09/DRB4*01:03:10/DRB4*01:03:11/DRB4*01:03:12/DRB4*01:03:13/DRB4*01:03:14/DRB4*01:03:15/DRB4*01:03:16/DRB4*01:03:17/DRB4*01:03:18/DRB4*01:03:19/DRB4*01:03:20/DRB4*01:03:21 |
      | DRB4*01:03:01N    | exon  | DRB4*01:03:01 |
      | DRB4*01:03:01:02N | exon  | DRB4*01:03:01 |
      | A*24:02L          | exon  | A*24:02:01/A*24:02:02/A*24:02:03Q/A*24:02:04/A*24:02:05/A*24:02:06/A*24:02:07/A*24:02:08/A*24:02:09/A*24:02:10/A*24:02:11/A*24:02:12/A*24:02:13/A*24:02:14/A*24:02:15/A*24:02:16/A*24:02:17/A*24:02:18/A*24:02:19/A*24:02:20/A*24:02:21/A*24:02:22/A*24:02:23/A*24:02:24/A*24:02:25/A*24:02:26/A*24:02:27/A*24:02:28/A*24:02:29/A*24:02:30/A*24:02:31/A*24:02:32/A*24:02:33/A*24:02:34/A*24:02:35/A*24:02:36/A*24:02:37/A*24:02:38/A*24:02:39/A*24:02:40/A*24:02:41/A*24:02:42/A*24:02:43/A*24:02:44/A*24:02:45/A*24:02:46/A*24:02:47/A*24:02:48/A*24:02:49/A*24:02:50/A*24:02:51/A*24:02:52/A*24:02:53/A*24:02:54/A*24:02:55/A*24:02:56/A*24:02:57/A*24:02:58/A*24:02:59/A*24:02:60/A*24:02:61/A*24:02:62/A*24:02:63/A*24:02:64/A*24:02:65/A*24:02:66/A*24:02:67/A*24:02:68/A*24:02:69/A*24:02:70/A*24:02:71/A*24:02:72/A*24:02:73/A*24:02:74/A*24:02:75/A*24:02:76/A*24:02:77/A*24:02:78/A*24:02:79/A*24:02:80/A*24:02:81/A*24:02:82/A*24:02:83/A*24:02:84/A*24:02:85/A*24:02:86/A*24:02:87/A*24:02:88/A*24:02:89/A*24:02:90/A*24:02:91/A*24:02:92/A*24:02:93/A*24:02:94/A*24:02:95/A*24:02:96/A*24:02:97/A*24:02:98/A*24:02:99/A*24:02:100/A*24:02:101/A*24:02:102/A*24:02:103/A*24:02:104/A*24:02:105/A*24:02:106/A*24:02:107/A*24:02:108/A*24:02:109/A*24:02:110/A*24:02:111/A*24:02:112/A*24:02:113/A*24:02:114/A*24:02:115/A*24:02:116/A*24:02:117/A*24:02:118/A*24:02:119/A*24:02:120/A*24:02:121/A*24:02:122/A*24:02:123/A*24:02:124/A*24:02:125/A*24:02:126/A*24:02:127/A*24:02:128/A*24:02:129/A*24:02:130/A*24:02:131/A*24:02:132/A*24:02:133/A*24:02:134/A*24:02:135/A*24:02:136/A*24:02:137/A*24:02:138/A*24:02:139/A*24:02:140/A*24:02:141/A*24:02:142/A*24:02:143/A*24:02:144/A*24:02:145/A*24:02:146/A*24:02:147 |
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
      | A*24:02L          | G     | A*24:02:01G/A*24:02:34G/A*24:02:115G |
      | A*24:02:01L       | G     | A*24:02:01G |
      | A*24:02:01:02L    | G     | A*24:02:01G |
