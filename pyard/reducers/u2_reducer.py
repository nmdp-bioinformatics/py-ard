# -*- coding: utf-8 -*-

from .base_reducer import Reducer
from ..misc import get_n_field_allele


class U2Reducer(Reducer):
    """Strategy for U2 reduction"""

    # @override
    def reduce(self, allele: str) -> str:
        allele_fields = allele.split(":")
        # If resolved out to second field leave alone
        if len(allele_fields) == 2:
            return allele
        # If the 2 field reduction is unambiguous, reduce to 2 field level

        allele_2_fields = get_n_field_allele(allele, 2, preserve_expression=True)
        if self.ard._is_allele_in_db(allele_2_fields):
            return allele_2_fields
        else:
            # If ambiguous, reduce to G group level
            return self.ard._redux_allele(allele, "lgx")
