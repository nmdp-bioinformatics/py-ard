# -*- coding: utf-8 -*-

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from ..ard import ARD


class XXHandler:
    """Handles XX code operations"""

    def __init__(self, ard_instance: "ARD"):
        self.ard = ard_instance

    def is_xx(self, glstring: str, loc_antigen: str = None, code: str = None) -> bool:
        """Check if string is a valid XX code"""
        if loc_antigen is None or code is None:
            if ":" in glstring:
                loc_allele = glstring.split(":")
                loc_antigen, code = loc_allele[0], loc_allele[1]
            else:
                return False
        return code == "XX" and loc_antigen in self.ard.code_mappings.xx_codes
