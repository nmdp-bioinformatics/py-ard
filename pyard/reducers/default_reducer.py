# -*- coding: utf-8 -*-
from typing_extensions import override

from .base_reducer import Reducer
from ..exceptions import InvalidAlleleError


class DefaultReducer(Reducer):
    """Default strategy for handling P/G suffixes and validation"""

    @override
    def reduce(self, allele: str) -> str:
        # Make this an explicit lookup to the g_group or p_group table
        # for stringent validation
        if allele.endswith("P"):
            if allele in self.ard.ars_mappings.p_group.values():
                return allele
        elif allele.endswith("G"):
            if allele in self.ard.ars_mappings.g_group.values():
                return allele

        if self.ard.is_valid_allele(allele):
            return allele
        else:
            raise InvalidAlleleError(f"{allele} is an invalid allele.")
