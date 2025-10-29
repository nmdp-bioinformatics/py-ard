# -*- coding: utf-8 -*-

import functools
from typing import override

from .base_reducer import Reducer
from .. import db
from ..misc import is_2_field_allele


class SReducer(Reducer):
    """Strategy for serology reduction"""

    # @override
    def reduce(self, allele: str) -> str:
        # find serology equivalent in serology_mapping
        if is_2_field_allele(allele):
            allele = self.ard._redux_allele(allele, "lgx")
            serology_mapping = db.find_serology_for_allele(
                self.ard.db_connection, allele, "lgx_allele_list"
            )
        else:
            serology_mapping = db.find_serology_for_allele(
                self.ard.db_connection, allele
            )

        serology_set = set()
        for serology, allele_list in serology_mapping.items():
            if allele in allele_list.split("/"):
                serology_set.add(serology)

        if not serology_set and is_2_field_allele(allele):
            for serology, allele_list in serology_mapping.items():
                allele_list_lgx = self.ard.redux(allele_list, "lgx")
                if allele in allele_list_lgx.split("/"):
                    serology_set.add(serology)

        return "/".join(
            sorted(
                serology_set, key=functools.cmp_to_key(self.ard.smart_sort_comparator)
            )
        )
