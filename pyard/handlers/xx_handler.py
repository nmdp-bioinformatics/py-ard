# -*- coding: utf-8 -*-

from typing import TYPE_CHECKING

from ..constants import HLA_regex

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
        if code == "XX":
            if HLA_regex.search(loc_antigen):
                loc_antigen = loc_antigen.split("-")[1]
            return loc_antigen in self.ard.code_mappings.xx_codes
        return False

    def expand_xx(self, xx_code: str) -> str:
        """Expand XX code to its constituent alleles

        Takes an XX code (e.g., 'A*74:XX') and returns a slash-delimited
        string of all alleles that match the 1-field pattern (e.g., 'A*74:01/A*74:02/...').

        Args:
            xx_code: XX code to expand (e.g., 'A*74:XX')

        Returns:
            Slash-delimited string of expanded alleles, or empty string if invalid
        """
        # Remove HLA- prefix for processing the XX code
        is_hla_prefix = HLA_regex.search(xx_code)
        if is_hla_prefix:
            xx_code = xx_code.split("-")[1]

        if not self.is_xx(xx_code):
            return ""

        # Extract the 1-field part (e.g., 'A*74' from 'A*74:XX')
        allele_1d = xx_code.split(":")[0]

        # Get the list of alleles from the xx_codes mapping
        if allele_1d in self.ard.code_mappings.xx_codes:
            alleles = self.ard.code_mappings.xx_codes[allele_1d]
            # alleles are already a list, so join them
            if is_hla_prefix:
                return "/".join(["HLA-" + a for a in alleles])
            return "/".join(alleles)

        return ""
