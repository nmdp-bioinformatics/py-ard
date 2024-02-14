Feature: Broad Splits for DNA/Serology

  Broad to Split mappings for serology is described here
  https://hla.alleles.org/antigens/broads_splits.html

  Scenario Outline: Broad allele and serology

    Given the broad allele/serology is <Broad>
    When it is expanded to the splits
    Then the splits are <Splits>

    Examples:
      | Broad    | Splits            |
      | A*09     | A*23/A*24         |
      | HLA-B*05 | HLA-B*51/HLA-B*52 |
      | DQB1*01  | DQB1*05/DQB1*06   |
      | B5       | B51/B52           |
      | B14      | B64/B65           |

  Scenario Outline: Broad and Sibling Splits

    Given the split allele/serology is <Split>
    When split is searched in the mappings
    Then the sibling splits are <Siblings>
    And the corresponding broad is <Broad>

    Examples:
      | Split    | Siblings    | Broad    |
      | A*23     | A*24        | A*09     |
      | HLA-B*51 | HLA-B*52    | HLA-B*05 |
      | DQB1*05  | DQB1*06     | DQB1*01  |
      | B*55     | B*54/B*56   | B*22     |
      | A25      | A26/A34/A66 | A10      |


  Scenario Outline: Associated Serology

    Given the serology antigen is <Serology>
    When looking for associated serology
    Then the associated serology is found to be <Associated Serology>

    Examples: Alleles to Serology
      | Serology | Associated Serology |
      | A23      | A23                 |
      | A24      | A24                 |
      | A2403    | A24                 |
      | DR1403   | DR14                |
      | DR1404   | DR14                |
      | B5       | B5                  |
