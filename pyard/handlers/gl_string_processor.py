# -*- coding: utf-8 -*-

import functools
from typing import List, TYPE_CHECKING

from ..constants import VALID_REDUCTION_TYPE
from ..misc import validate_reduction_type

if TYPE_CHECKING:
    from ..ard import ARD


class GLStringHandler:
    """Handles GL string parsing, validation and processing

    GL (Genotype List) strings represent HLA typing data using standardized
    delimiters to express ambiguity and relationships between alleles.
    This class processes these complex strings by parsing delimiters and
    applying reductions to individual components.
    """

    def __init__(self, ard_instance: "ARD"):
        """Initialize the GLStringHandler with an ARD instance

        Args:
            ard_instance: The main ARD object for database access and configuration
        """
        self.ard = ard_instance

    def process_gl_string(
        self, glstring: str, redux_type: VALID_REDUCTION_TYPE = "lgx"
    ) -> str:
        """Main GL string processing logic extracted from redux method

        Processes GL strings by parsing delimiters in order of precedence
        and applying reductions to individual components. GL string delimiters:
        ^ = unphased genotype list
        | = phased genotype list
        + = allele list (multiple alleles at same locus)
        ~ = possible allele list
        / = ambiguous allele list

        Args:
            glstring: GL string to process (e.g., "A*01:01+A*02:01^B*07:02")
            redux_type: Type of reduction to apply to each component

        Returns:
            Processed GL string with reductions applied
        """
        validate_reduction_type(redux_type)

        # Validate GL string structure if strict mode is enabled
        if self.ard.config.strict_enabled:
            self.validate_gl_string(glstring)

        # Handle GL string delimiters in order of precedence
        # Unphased genotype list (highest precedence)
        if "^" in glstring:
            return self._sorted_unique_gl(
                [self.ard.redux(a, redux_type) for a in glstring.split("^")], "^"
            )

        # Phased genotype list
        if "|" in glstring:
            return self._sorted_unique_gl(
                [self.ard.redux(a, redux_type) for a in glstring.split("|")], "|"
            )

        # Allele list (multiple alleles at same locus)
        if "+" in glstring:
            return self._sorted_unique_gl(
                [self.ard.redux(a, redux_type) for a in glstring.split("+")], "+"
            )

        # Possible allele list
        if "~" in glstring:
            return self._sorted_unique_gl(
                [self.ard.redux(a, redux_type) for a in glstring.split("~")], "~"
            )

        # Ambiguous allele list (lowest precedence)
        if "/" in glstring:
            return self._sorted_unique_gl(
                [self.ard.redux(a, redux_type) for a in glstring.split("/")], "/"
            )

        # Single allele - return as-is for further processing
        return glstring

    def _sorted_unique_gl(self, gls: List[str], delim: str) -> str:
        """Make a list of sorted unique GL Strings separated by delim

        Creates a sorted, deduplicated list of GL string components.
        Different delimiters have different sorting behaviors:
        - '~' preserves original order (no sorting/deduplication)
        - '+' sorts but keeps structure intact
        - Others flatten, deduplicate, and sort

        Args:
            gls: List of GL string components to process
            delim: Delimiter to use for joining results

        Returns:
            Sorted and deduplicated GL string components joined by delimiter
        """
        # Possible allele list (~) preserves original order
        if delim == "~":
            return delim.join(gls)

        # Allele list (+) sorts but maintains structure
        if delim == "+":
            non_empty_gls = filter(lambda s: s != "", gls)
            return delim.join(
                sorted(
                    non_empty_gls,
                    key=functools.cmp_to_key(
                        lambda a, b: self.ard.smart_sort_comparator(
                            a, b, self.ard.config.ignore_allele_with_suffixes
                        )
                    ),
                )
            )

        # Other delimiters: flatten, deduplicate, and sort
        all_gls = []
        for gl in gls:
            all_gls += gl.split(delim)
        unique_gls = filter(lambda s: s != "", set(all_gls))
        return delim.join(
            sorted(
                unique_gls,
                key=functools.cmp_to_key(
                    lambda a, b: self.ard.smart_sort_comparator(
                        a, b, self.ard.config.ignore_allele_with_suffixes
                    )
                ),
            )
        )

    def validate_gl_string(self, glstring: str) -> bool:
        """Validate GL string structure and components

        Recursively validates GL string by parsing delimiters and checking
        that all leaf components (individual alleles) are valid according
        to the ARD database.

        Args:
            glstring: GL string to validate

        Returns:
            True if all components are valid

        Raises:
            InvalidAlleleError: If any component allele is invalid
        """
        # Recursively validate components separated by each delimiter type
        if "^" in glstring:
            return all(map(self.validate_gl_string, glstring.split("^")))
        if "|" in glstring:
            return all(map(self.validate_gl_string, glstring.split("|")))
        if "+" in glstring:
            return all(map(self.validate_gl_string, glstring.split("+")))
        if "~" in glstring:
            return all(map(self.validate_gl_string, glstring.split("~")))
        if "/" in glstring:
            return all(map(self.validate_gl_string, glstring.split("/")))

        # Base case: validate individual allele against database
        is_valid_allele = self.ard._is_valid(glstring)
        if not is_valid_allele:
            from ..exceptions import InvalidAlleleError

            raise InvalidAlleleError(f"{glstring} is not a valid Allele")
        return is_valid_allele
