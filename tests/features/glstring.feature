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