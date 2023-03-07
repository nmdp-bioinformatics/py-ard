import re

DEFAULT_CACHE_SIZE = 1_000

HLA_regex = re.compile("^HLA-")

VALID_REDUCTION_TYPES = ["G", "P", "lg", "lgx", "W", "exon", "U2"]
expression_chars = ["N", "Q", "L", "S"]
# List of P and G characters
PandG_chars = ["P", "G"]
