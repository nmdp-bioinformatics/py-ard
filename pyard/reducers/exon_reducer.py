# -*- coding: utf-8 -*-
from typing import override

from .base_reducer import Reducer


class ExonReducer(Reducer):
    """Strategy for exon reduction"""

    @override
    def reduce(self, allele: str) -> str:
        if allele in self.ard.ars_mappings.exon_group:
            exon_group_allele = self.ard.ars_mappings.exon_group[allele]
            # Check if the 3 field exon allele has a 4 field alleles
            # that all have the same expression characters
            from ..constants import expression_chars

            last_char = allele[-1]
            if last_char in expression_chars:
                exon_short_null_allele = exon_group_allele + last_char
                if self.ard.is_shortnull(exon_short_null_allele):
                    return exon_short_null_allele
            return exon_group_allele
        else:
            # Expand to W level and then reduce to exon
            w_redux = self.ard.redux(allele, "W")
            # If the W redux produces 2 field allele or the same allele, don't recurse
            if w_redux == allele or len(w_redux.split(":")) == 2:
                return allele
            else:
                # recurse with the W fields
                return self.ard.redux(w_redux, "exon")
