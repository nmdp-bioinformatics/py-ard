# -*- coding: utf-8 -*-

import functools
from typing import TYPE_CHECKING


from .. import db
from ..misc import is_2_field_allele

if TYPE_CHECKING:
    from ..ard import ARD


class HATSHandler:
    def __init__(self, ard_instance: "ARD"):
        self.ard = ard_instance

    def expand_to_hats_alleles(self, alleles_gl: str) -> str:
        alleles = alleles_gl.split("/")
        locus = alleles[0].split("*")[0]
        hats_alleles = db.find_common_hats_alleles(self.ard.db_connection, alleles)
        # MAC expanded alleles should only be 2 field level alleles
        hats_alleles_2fields = filter(is_2_field_allele, hats_alleles)
        hats_alleles_same_locus = filter(
            lambda a: a.split("*")[0] == locus, hats_alleles_2fields
        )
        return "/".join(
            sorted(
                hats_alleles_same_locus,
                key=functools.cmp_to_key(self.ard.smart_sort_comparator),
            )
        )
