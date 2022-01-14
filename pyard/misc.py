# List of expression characters
expression_chars = ['N', 'Q', 'L', 'S']


def get_n_field_allele(allele: str, n: int, preserve_expression=False) -> str:
    """
    Given an HLA allele of >= n field, return n field allele.
    Preserve the expression character if it exists

    :param allele: Original allele
    :param n: n number of fields to reduce to
    :return: trimmed to n fields of the original allele
    """
    last_char = allele[-1]
    fields = allele.split(':')
    if preserve_expression and \
            last_char in expression_chars and len(fields) > n:
        return ':'.join(fields[0:n]) + last_char
    else:
        return ':'.join(fields[0:n])


def get_3field_allele(a: str) -> str:
    return get_n_field_allele(a, 3)


def get_2field_allele(a: str) -> str:
    return get_n_field_allele(a, 2)


def number_of_fields(allele: str) -> int:
    return len(allele.split(':'))
