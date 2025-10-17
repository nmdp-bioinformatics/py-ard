# -*- coding: utf-8 -*-

import re
from typing import TYPE_CHECKING

from .. import db

if TYPE_CHECKING:
    from ..ard import ARD


class V2Handler:
    """Handles V2 to V3 nomenclature conversion"""

    def __init__(self, ard_instance: "ARD"):
        self.ard = ard_instance

    def is_v2(self, allele: str) -> bool:
        """Check if allele is V2 nomenclature"""
        matches_v2_format = (
            self.ard._config["reduce_v2"]
            and "*" in allele
            and ":" not in allele
            and allele.split("*")[0] not in ["MICA", "MICB", "HFE"]
        )

        if matches_v2_format:
            v3_format_allele = self.map_v2_to_v3(allele)
            if v3_format_allele != allele:
                if v3_format_allele.split(":").pop().isalpha():
                    return self.ard.is_mac(v3_format_allele)
                return self.ard._is_allele_in_db(v3_format_allele)

        return False

    def map_v2_to_v3(self, v2_allele: str) -> str:
        """Convert V2 allele to V3 format"""
        v3_allele = db.v2_to_v3_allele(self.ard.db_connection, v2_allele)
        if not v3_allele:
            v3_allele = self._predict_v3(v2_allele)
        return v3_allele

    def _predict_v3(self, v2_allele: str) -> str:
        """Use heuristic to predict V3 from V2"""
        locus, allele_name = v2_allele.split("*")
        components = re.findall(r"^(\d+)(.*)", allele_name)
        if not components:
            return v2_allele

        digits_field, non_digits_field = components.pop()
        final_allele = digits_field
        num_of_digits = len(digits_field)

        if num_of_digits == 1:
            return v2_allele

        if num_of_digits > 2:
            if locus.startswith("DP") and num_of_digits == 5:
                final_allele = (
                    digits_field[:3] + ":" + (digits_field[3:]) + non_digits_field
                )
            elif num_of_digits % 2 == 0:
                final_allele = self._combine_with_colon(digits_field) + non_digits_field
            else:
                final_allele = (
                    digits_field[:2] + ":" + (digits_field[2:]) + non_digits_field
                )
        else:
            if non_digits_field:
                final_allele = digits_field + ":" + non_digits_field

        return locus + "*" + final_allele

    @staticmethod
    def _combine_with_colon(digits_field: str) -> str:
        """Combine digits with colon separator"""
        num_of_digits = len(digits_field)
        return ":".join(digits_field[i : i + 2] for i in range(0, num_of_digits, 2))
