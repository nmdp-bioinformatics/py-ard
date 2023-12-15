Feature: CWD Reduction

  Version 2 of the Common and Well-Documented (CWD) alleles
  https://onlinelibrary.wiley.com/doi/full/10.1111/tan.12093

  lgx reduced version of allele list can be used to compare against
  CWD catalogue and produce a sublist that's contained in CWD.

  Scenario: Using A*26:CBJTR MAC Code

    Given the MAC Code we want to find CWD of is "A*26:CBJTR"
    When we reduce MAC code to lgx and find CWD alleles in the expansion
    Then the CWD alleles should be "A*25:01/A*26:01/A*26:02/A*26:09/A*26:15/A*26:17/A*26:20"


  Scenario: Using Allele list GL String of 1 CWD allele

    Given the GL String we want to find CWD of is "B*08:01/B*08:05/B*08:08N/B*08:10/B*08:15/B*08:18/B*08:19N/B*08:22/B*08:24/B*08:27/B*08:30N"
    When we find CWD alleles for the GL String
    Then the CWD alleles should be "B*08:01/B*08:18"

  Scenario: Using Allele list GL String of 2 CWD allele

    Given the GL String we want to find CWD of is "B*15:01:01/B*15:01:03/B*15:04/B*15:07/B*15:26N/B*15:27"
    When we find CWD alleles for the GL String
    Then the CWD alleles should be "B*15:01/B*15:04/B*15:07/B*15:27"

  Scenario: Using Allele list GL String that also has a MAC mapping

    Given the GL String we want to find CWD of is "A*01:01:01/A*01:02:01/A*01:03:01"
    When we find CWD alleles for the GL String
    Then the CWD alleles should be "A*01:01/A*01:02/A*01:03"
    And the MAC Code for CWD alleles should be "A*01:MN"

  Scenario Outline: CWD Alleles with Nulls

    Given the GL String we want to find CWD of is "<gl_string>"
    When we find CWD alleles for the GL String
    Then the CWD alleles should be "<cwd_list>"
    Examples:
      | gl_string                          | cwd_list         |
      | A*03:01/A*03:01N                   | A*03:01          |
      | C*04:09N                           | C*04:09N         |
      | C*04:01:01                         | C*04:01          |
      | C*04:KBG                           | C*04:01/C*04:09N |
      | C*04:01:01G/C*04:09N               | C*04:01/C*04:09N |
      | B*15:01/B*15:01N/B*15:102/B*15:104 | B*15:01/B*15:01N |
