Feature: Version 2 Nomenclature

  py-ard is able to reduce version 2 HLA nomenclature.

  Scenario Outline:

    Given the version 2 typing is <Version2>
    When reducing on the <Level> level (ambiguous)
    Then the reduced allele is found to be <Redux Allele>


    Examples: Valid A serology typings
      | Version2  | Level | Redux Allele                                                   |
      | A*0105N   | G     | A*01:01:01G                                                    |
      | A*0111    | G     | A*01:11N                                                       |
      | DRB5*02ZB | G     | DRB5*01:02:01G/DRB5*01:03/DRB5*02:02:01G/DRB5*02:03/DRB5*02:04 |
