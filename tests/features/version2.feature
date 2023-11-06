Feature: Version 2 Nomenclature

  py-ard is able to reduce version 2 HLA nomenclature.

  Scenario Outline: Redux V2 Alleles

    Given the version 2 typing is <Version2>
    When reducing on the <Level> level (ambiguous)
    Then the reduced allele is found to be <Redux Allele>


    Examples: Reduce V2 Alleles
      | Version2  | Level | Redux Allele                                                   |
      | A*0105N   | G     | A*01:01:01G                                                    |
      | A*0111    | G     | A*01:11N                                                       |
      | DRB5*02ZB | G     | DRB5*01:02:01G/DRB5*01:03/DRB5*02:02:01G/DRB5*02:03/DRB5*02:04 |


  Scenario Outline: Invalid V2

  Alleles that have valid V2 format but when converted to V3 format,
  is not a valid allele.

    Given the version 2 typing is <Version2>
    When validating the V2 typing
    Then the validness of V2 typing is <Validity>

    Examples: Validate
      | Version2  | Validity |
      | A*0105N   | Valid    |
      | DQB1*0804 | Invalid  |
      | A*01:AB   | Valid    |
      | A*01:NOAB | Invalid  |
