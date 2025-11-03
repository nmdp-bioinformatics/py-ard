# -*- coding: utf-8 -*-

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from ..ard import ARD


class XXHandler:
    """Handles XX code operations

    XX codes are special HLA nomenclature designations that represent
    groups of alleles sharing common serological or functional properties.
    The 'XX' suffix indicates a broad grouping at the antigen level.
    This class provides functionality to identify and validate XX codes.
    """

    def __init__(self, ard_instance: "ARD"):
        """Initialize the XXHandler with an ARD instance

        Args:
            ard_instance: The main ARD object for accessing code mappings
        """
        self.ard = ard_instance

    def is_xx(self, glstring: str, loc_antigen: str = None, code: str = None) -> bool:
        """Check if string is a valid XX code

        XX codes have the format 'LOCUS*ANTIGEN:XX' where XX is the literal
        string 'XX'. Validates that the code suffix is 'XX' and that the
        locus/antigen combination exists in the XX code mappings.

        Args:
            glstring: String to check (e.g., 'A*01:XX', 'B*27:XX')
            loc_antigen: Optional pre-parsed locus*antigen part
            code: Optional pre-parsed code suffix

        Returns:
            True if the string is a valid XX code, False otherwise
        """
        # Parse the glstring if components not provided
        if loc_antigen is None or code is None:
            if ":" in glstring:
                loc_allele = glstring.split(":")
                loc_antigen, code = loc_allele[0], loc_allele[1]
            else:
                return False

        # Validate XX code: suffix must be 'XX' and locus*antigen must be in mappings
        return code == "XX" and loc_antigen in self.ard.code_mappings.xx_codes
