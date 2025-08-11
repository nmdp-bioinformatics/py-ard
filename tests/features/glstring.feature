Feature: GL (Genotype List) Strings

  Scenario Outline:

    Given the allele as <Allele>
    When reducing on the <Level> level (ambiguous)
    Then the reduced allele is found to be <Redux Allele>

    Examples:
      | Allele                                                           | Level | Redux Allele                                                             |
      | A*01:01:01:01+A*01:01:01:01                                      | G     | A*01:01:01G+A*01:01:01G                                                  |
      | HLA-A*01:01:01:01+HLA-A*01:01:01:01                              | G     | HLA-A*01:01:01G+HLA-A*01:01:01G                                          |
      | A*01:01:01:01+A*01:01:01:01                                      | lg    | A*01:01g+A*01:01g                                                        |
      | HLA-A*01:01:01:01+HLA-A*01:01:01:01                              | lg    | HLA-A*01:01g+HLA-A*01:01g                                                |
      | A*01:01:01:01+A*01:01:01:01                                      | lgx   | A*01:01+A*01:01                                                          |
      | HLA-A*01:01:01:01+HLA-A*01:01:01:01                              | lgx   | HLA-A*01:01+HLA-A*01:01                                                  |
      | A*01:01+A*01:01^B*07:02+B*07:02                                  | G     | A*01:01:01G+A*01:01:01G^B*07:02:01G+B*07:02:01G                          |
      | A*01:01+A*01:01^B*07:02+B*07:02                                  | lg    | A*01:01g+A*01:01g^B*07:02g+B*07:02g                                      |
      | A*01:01~B*07:02+A*01:01~B*07:02                                  | G     | A*01:01:01G~B*07:02:01G+A*01:01:01G~B*07:02:01G                          |
      | A*01:01~B*07:02+A*01:01~B*07:02                                  | lg    | A*01:01g~B*07:02g+A*01:01g~B*07:02g                                      |
      | A*01:01~B*07:02+A*01:01~B*07:02\|A*02:01~B*07:02+A*02:01~B*07:02 | lg    | A*01:01g~B*07:02g+A*01:01g~B*07:02g\|A*02:01g~B*07:02g+A*02:01g~B*07:02g |


  Scenario Outline: Ignore reduction of DRBX*NNNN in GL String
    Given the allele as <GL String>
    When reducing on the <Level> level in ignore_suffix mode
    Then the reduced allele is found to be <Redux GL String>

    Examples:
      | GL String               | Level | Redux GL String                         |
      | DRBX*NNNN+DRB3*03:ECXMH | lgx   | DRB3*03:01+DRBX*NNNN                    |
      | DRB3*03:ECXMH+DRBX*NNNN | lgx   | DRB3*03:01+DRBX*NNNN                    |
      | DRB1*UUUU+DRB1*12:02    | G     | DRB1*12:02:01G/DRB1*12:02:02G+DRB1*UUUU |
