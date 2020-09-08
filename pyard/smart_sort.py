import functools
import re

expr_regex = re.compile('[NQLSGg]')


@functools.lru_cache(maxsize=None)
def smart_sort_comparator(a1, a2):
    """
    Natural sort 2 given alleles.

    Python sorts strings lexicographically but HLA alleles need
    to be sorted by numerical values in each field of the HLA nomenclature.

    :param a1: first allele
    :param a2: second allele
    """

    # Check to see if they are the same alleles
    if a1 == a2:
        return 0

    # remove any non-numerics
    a1 = re.sub(expr_regex, '', a1)
    a2 = re.sub(expr_regex, '', a2)

    # Check to see if they are still the same alleles
    if a1 == a2:
        return 0

    # Extract and Compare first fields first
    a1_f1 = int(a1[a1.find('*') + 1:a1.find(':')])
    a2_f1 = int(a2[a2.find('*') + 1:a2.find(':')])

    if a1_f1 < a2_f1:
        return -1
    if a1_f1 > a2_f1:
        return 1

    a1_fields = a1.split(':')
    a2_fields = a2.split(':')

    # If the first fields are equal, try the 2nd fields
    a1_f2 = int(a1_fields[1])
    a2_f2 = int(a2_fields[1])

    if a1_f2 < a2_f2:
        return -1
    if a1_f2 > a2_f2:
        return 1

    # If the second fields are equal, try the 3rd fields
    a1_f3 = int(a1_fields[2])
    a2_f3 = int(a2_fields[2])

    if a1_f3 < a2_f3:
        return -1
    if a1_f3 > a2_f3:
        return 1

    # If the third fields are equal, try the 4th fields
    a1_f4 = int(a1_fields[3])
    a2_f4 = int(a2_fields[3])

    if a1_f4 < a2_f4:
        return -1
    if a1_f4 > a2_f4:
        return 1

    # All fields are considered equal after 4th field
    return 0

