import functools
import re

expr_regex = re.compile('[NQLS]')

@functools.lru_cache(maxsize=None)
def smart_sort_comparator(a1, a2):
    """
    Natural sort 2 given alleles.

    Python sorts strings lexographically but HLA alleles need
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
    # Extract and Compare first fields first
    a1_f1 = int(a1[a1.find('*')+1:a1.find(':')])
    a2_f1 = int(a2[a2.find('*')+1:a2.find(':')])

    if a1_f1 < a2_f1:
        return -1
    if a1_f1 > a2_f1:
        return 1

    # If the first fields are equal, try the 2nd fields
    a1_f2 = int(a1[a1.find(':')+1:])
    a2_f2 = int(a2[a2.find(':')+1:])

    if a1_f2 < a2_f2:
        return -1
    if a1_f2 > a2_f2:
        return 1

    # All fields are equal
    return 0

def smart_sort_alleles(a1, a2):
    """
    Natural sort 2 given alleles.

    Python sorts strings lexographically but HLA alleles need
    to be sorted by numerical values in each field of the HLA nomenclature.

    :param a1: first allele
    :param a2: second allele
    """
    # Check to see if they are the same alleles
    if a1 == a2:
        return [a1, a2]

    # Extract and Compare first fields first
    a1_f1 = int(a1[a1.find('*')+1:a1.find(':')])
    a2_f1 = int(a2[a2.find('*')+1:a2.find(':')])

    if a1_f1 < a2_f1:
        return [a1, a2]
    if a1_f1 > a2_f1:
        return [a2, a1]

    # If the first fields are equal, try the 2nd fields
    a1_f2 = int(a1[a1.find(':')+1:])
    a2_f2 = int(a2[a2.find(':')+1:])

    if a1_f2 < a2_f2:
        return [a1, a2]
    if a1_f2 > a2_f2:
        return [a2, a1]

    # All fields are equal
    return [a1, a2]
