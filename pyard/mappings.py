from collections import namedtuple

ars_mapping_tables = [
    "dup_g",
    "dup_lgx",
    "g_group",
    "p_group",
    "lgx_group",
    "exon_group",
    "p_not_g",
]
code_mapping_tables = [
    "alleles",
    "exp_alleles",
    "xx_codes",
    "who_alleles",
    "who_group",
]

ARSMapping = namedtuple("ARSMapping", ars_mapping_tables)
