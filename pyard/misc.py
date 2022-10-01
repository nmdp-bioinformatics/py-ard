# List of expression characters
expression_chars = ["N", "Q", "L", "S"]
# List of P and G characters
PandG_chars = ["P", "G"]


def get_n_field_allele(allele: str, n: int, preserve_expression=False) -> str:
    """
    Given an HLA allele of >= n field, return n field allele.
    Preserve the expression character if it exists

    :param allele: Original allele
    :param n: n number of fields to reduce to
    :return: trimmed to n fields of the original allele
    """
    last_char = allele[-1]
    fields = allele.split(":")
    if preserve_expression and last_char in expression_chars and len(fields) > n:
        return ":".join(fields[0:n]) + last_char
    else:
        return ":".join(fields[0:n])


def get_3field_allele(a: str) -> str:
    last_char = a[-1]
    if last_char in PandG_chars:
        a = a[:-1]

    return get_n_field_allele(a, 3)


def get_2field_allele(a: str) -> str:
    last_char = a[-1]
    if last_char in PandG_chars:
        a = a[:-1]
    return get_n_field_allele(a, 2)


def number_of_fields(allele: str) -> int:
    return len(allele.split(":"))


# computes a valid G name based on the ambiguity string
def get_G_name(a: str) -> str:
    a = a.split("/")[0]
    last_char = a[-1]
    if last_char in PandG_chars + expression_chars:
        a = a[:-1]
    if len(a.split(":")) == 2:
        return ":".join([a, "01"]) + "G"
    else:
        return ":".join(a.split(":")[0:3]) + "G"


# computes a valid P name based on the ambiguity string
def get_P_name(a: str) -> str:
    a = a.split("/")[0]
    last_char = a[-1]
    if last_char in PandG_chars + expression_chars:
        a = a[:-1]
    return ":".join(a.split(":")[0:2]) + "P"
