Feature: shortnull

  Scenario Outline:

    Given the allele as <Allele>
    When reducing on the <Level> level (ambiguous)
    Then the reduced allele is found to be <Redux Allele>


    Examples: shortnulls
      | Allele         | Level | Redux Allele                |
      | DRB4*01:03N    | lgx   | DRB4*01:01                  |
      | DRB4*01:03N    | exon  | DRB4*01:03:01               |
      | DRB4*01:03N    | W     | DRB4*01:03:01:02N/DRB4*01:03:01:13N |
      | DRB4*01:03:01N | lgx   | DRB4*01:01                  |
      | DRB4*01:03:01N | exon  | DRB4*01:03:01               |
      | DRB4*01:03:01N | W     | DRB4*01:03:01:02N/DRB4*01:03:01:13N |
      | DRB5*01:08N    | lgx   | DRB5*01:02/DRB5*01:08 |
      | DRB5*01:08N    | exon  | DRB5*01:08:01N/DRB5*01:08:02N |
      | DRB5*01:08N    | W     | DRB5*01:08:01N/DRB5*01:08:02N |
