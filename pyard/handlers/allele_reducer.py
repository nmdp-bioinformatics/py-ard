# -*- coding: utf-8 -*-

import functools
from typing import TYPE_CHECKING

from ..constants import VALID_REDUCTION_TYPES, expression_chars
from ..exceptions import InvalidAlleleError
from ..misc import get_n_field_allele

if TYPE_CHECKING:
    from ..ard import ARD


class AlleleReducer:
    """Handles core allele reduction logic"""

    def __init__(self, ard_instance: "ARD"):
        self.ard = ard_instance

    def reduce_allele(
        self, allele: str, redux_type: VALID_REDUCTION_TYPES, re_ping=True
    ) -> str:
        """Core allele reduction logic extracted from _redux_allele"""

        if redux_type == "G" and allele in self.ard.ars_mappings.g_group:
            if allele in self.ard.ars_mappings.dup_g:
                return self.ard.ars_mappings.dup_g[allele]
            else:
                return self.ard.ars_mappings.g_group[allele]

        elif redux_type == "P" and allele in self.ard.ars_mappings.p_group:
            return self.ard.ars_mappings.p_group[allele]

        elif redux_type in ["lgx", "lg"]:
            if allele in self.ard.ars_mappings.lgx_group:
                redux_allele = self.ard.ars_mappings.lgx_group[allele]
            else:
                redux_allele = ":".join(allele.split(":")[0:2])
            if redux_type == "lg":
                return self._add_lg_suffix(redux_allele)
            return redux_allele

        elif redux_type == "W":
            if self.ard._is_who_allele(allele):
                return allele
            if allele in self.ard.code_mappings.who_group:
                return self.ard.redux(
                    "/".join(self.ard.code_mappings.who_group[allele]), redux_type
                )
            else:
                return allele

        elif redux_type == "exon":
            return self._handle_exon_reduction(allele)

        elif redux_type == "U2":
            return self._handle_u2_reduction(allele)

        elif redux_type == "S":
            return self._handle_serology_reduction(allele)

        else:
            return self._handle_default_reduction(allele)

    def _add_lg_suffix(self, redux_allele):
        """Add lg suffix to reduced allele"""
        if "/" in redux_allele:
            return "/".join(
                [self._add_lg_suffix(allele) for allele in redux_allele.split("/")]
            )
        if self.ard._config["ARS_as_lg"]:
            return redux_allele + "ARS"
        return redux_allele + "g"

    def _handle_exon_reduction(self, allele):
        """Handle exon reduction type"""
        if allele in self.ard.ars_mappings.exon_group:
            exon_group_allele = self.ard.ars_mappings.exon_group[allele]
            last_char = allele[-1]
            if last_char in expression_chars:
                exon_short_null_allele = exon_group_allele + last_char
                if self.ard.is_shortnull(exon_short_null_allele):
                    return exon_short_null_allele
            return exon_group_allele
        else:
            w_redux = self.ard.redux(allele, "W")
            if w_redux == allele or len(w_redux.split(":")) == 2:
                return allele
            else:
                return self.ard.redux(w_redux, "exon")

    def _handle_u2_reduction(self, allele):
        """Handle U2 reduction type"""
        allele_fields = allele.split(":")
        if len(allele_fields) == 2:
            return allele
        allele_2_fields = get_n_field_allele(allele, 2, preserve_expression=True)
        if self.ard._is_allele_in_db(allele_2_fields):
            return allele_2_fields
        else:
            return self.reduce_allele(allele, "lgx")

    def _handle_serology_reduction(self, allele):
        """Handle serology reduction type"""
        from .. import db
        from ..misc import is_2_field_allele

        if is_2_field_allele(allele):
            allele = self.reduce_allele(allele, "lgx")
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

    def _handle_default_reduction(self, allele):
        """Handle default reduction cases"""
        if allele.endswith("P"):
            if allele in self.ard.ars_mappings.p_group.values():
                return allele
        elif allele.endswith("G"):
            if allele in self.ard.ars_mappings.g_group.values():
                return allele

        if self.ard._is_allele_in_db(allele):
            return allele
        else:
            raise InvalidAlleleError(f"{allele} is an invalid allele.")
