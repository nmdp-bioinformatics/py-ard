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
    "xx_codes",
    "who_group",
]

allele_tables = [
    "alleles",
    "exp_alleles",
    "who_alleles",
]

ARSMapping = namedtuple("ARSMapping", ars_mapping_tables)
CodeMappings = namedtuple("CodeMappings", code_mapping_tables)
AlleleGroups = namedtuple("AlleleGroups", allele_tables)
