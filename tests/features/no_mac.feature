Feature: Reduce alleles (no MAC)

        Scenario Outline:

                Given the allele as <Allele>
                When reducing on the <Level> level
                Then the reduced allele is found to be <Redux Allele>

                Examples:
                        | Allele         | Level | Redux Allele    |
                        | A*01:01:01     | G     | A*01:01:01G     | 
                        | A*01:01:01     | lg    | A*01:01g        |
                        | A*01:01:01     | lgx   | A*01:01         |
                        | HLA-A*01:01:01 | G     | HLA-A*01:01:01G |
                        | HLA-A*01:01:01 | lg    | HLA-A*01:01g    |
                        | HLA-A*01:01:01 | lgx   | HLA-A*01:01     |