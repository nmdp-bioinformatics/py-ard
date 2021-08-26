Feature: WHO expansion and Exon reduction

  Redux Type of `W` supports WHO expansion
  Redux Type of `exon` supports Exon level reduction

  `W` is an expanding type (like MAC and XX) in that finds all WHO alleles consistent with the input.
  `exon` is a reducing type, it expects input that is already exon (3field) resolution or higher (4 field) and reduces it to 3 field.

  To covert 2-field/MAC/XX to exon/3-field resolution it requires calling redux_gl twice: once at W level to expand and then at exon level to reduce the output to exon/3-field

  Scenario Outline: WHO expansion

    Given the typing is <Allele>
    When expanding at the <Level> level
    Then the expanded allele is found to be <Expanded Alleles>

    Examples:
      | Allele     | Level | Expanded Alleles                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                   |
      | DRB1*11:02 | W     | DRB1*11:02:01:01/DRB1*11:02:01:02/DRB1*11:02:01:03/DRB1*11:02:02/DRB1*11:02:03/DRB1*11:02:04/DRB1*11:02:05/DRB1*11:02:06/DRB1*11:02:07                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                             |
      | DRB1*11:01 | W     | DRB1*11:01:01:01/DRB1*11:01:01:03/DRB1*11:01:01:04/DRB1*11:01:02:01/DRB1*11:01:02:02/DRB1*11:01:03/DRB1*11:01:04/DRB1*11:01:05/DRB1*11:01:06/DRB1*11:01:07/DRB1*11:01:08/DRB1*11:01:09/DRB1*11:01:10/DRB1*11:01:11/DRB1*11:01:12/DRB1*11:01:13/DRB1*11:01:14/DRB1*11:01:15/DRB1*11:01:16/DRB1*11:01:17/DRB1*11:01:18/DRB1*11:01:19/DRB1*11:01:20/DRB1*11:01:21/DRB1*11:01:22/DRB1*11:01:23/DRB1*11:01:24/DRB1*11:01:25/DRB1*11:01:26/DRB1*11:01:27/DRB1*11:01:28/DRB1*11:01:29/DRB1*11:01:30/DRB1*11:01:31/DRB1*11:01:32/DRB1*11:01:33/DRB1*11:01:34/DRB1*11:01:35/DRB1*11:01:36/DRB1*11:01:37/DRB1*11:01:38/DRB1*11:01:39/DRB1*11:01:40/DRB1*11:01:41/DRB1*11:01:42/DRB1*11:01:43 |


  Scenario Outline: Exon reduction

    Given the typing is <Allele>
    When expanding at the <Level> level
    Then the expanded allele is found to be <Expanded Alleles>
    Examples:
      | Allele        | Level | Expanded Alleles |
      | DRB1*11:01    | exon  | DRB1*11:01       |
      | A*01:01:01:03 | exon  | A*01:01:01       |