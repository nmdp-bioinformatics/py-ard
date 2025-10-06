# -*- coding: utf-8 -*-

import functools
from typing import List, TYPE_CHECKING

from ..constants import VALID_REDUCTION_TYPE
from ..misc import validate_reduction_type

if TYPE_CHECKING:
    from ..ard import ARD


class GLStringProcessor:
    """Handles GL string parsing, validation and processing"""

    def __init__(self, ard_instance: "ARD"):
        self.ard = ard_instance

    def process_gl_string(
        self, glstring: str, redux_type: VALID_REDUCTION_TYPE = "lgx"
    ) -> str:
        """Main GL string processing logic extracted from redux method"""
        validate_reduction_type(redux_type)

        if self.ard._config["strict"]:
            self.validate_gl_string(glstring)

        # Handle GL string delimiters
        if "^" in glstring:
            return self._sorted_unique_gl(
                [self.ard.redux(a, redux_type) for a in glstring.split("^")], "^"
            )

        if "|" in glstring:
            return self._sorted_unique_gl(
                [self.ard.redux(a, redux_type) for a in glstring.split("|")], "|"
            )

        if "+" in glstring:
            return self._sorted_unique_gl(
                [self.ard.redux(a, redux_type) for a in glstring.split("+")], "+"
            )

        if "~" in glstring:
            return self._sorted_unique_gl(
                [self.ard.redux(a, redux_type) for a in glstring.split("~")], "~"
            )

        if "/" in glstring:
            return self._sorted_unique_gl(
                [self.ard.redux(a, redux_type) for a in glstring.split("/")], "/"
            )

        return glstring

    def _sorted_unique_gl(self, gls: List[str], delim: str) -> str:
        """Make a list of sorted unique GL Strings separated by delim"""
        if delim == "~":
            return delim.join(gls)

        if delim == "+":
            non_empty_gls = filter(lambda s: s != "", gls)
            return delim.join(
                sorted(
                    non_empty_gls,
                    key=functools.cmp_to_key(
                        lambda a, b: self.ard.smart_sort_comparator(
                            a, b, self.ard._config["ignore_allele_with_suffixes"]
                        )
                    ),
                )
            )

        all_gls = []
        for gl in gls:
            all_gls += gl.split(delim)
        unique_gls = filter(lambda s: s != "", set(all_gls))
        return delim.join(
            sorted(
                unique_gls,
                key=functools.cmp_to_key(
                    lambda a, b: self.ard.smart_sort_comparator(
                        a, b, self.ard._config["ignore_allele_with_suffixes"]
                    )
                ),
            )
        )

    def validate_gl_string(self, glstring: str) -> bool:
        """Validate GL string structure and components"""
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

        # what falls through here is an allele
        is_valid_allele = self.ard._is_valid(glstring)
        if not is_valid_allele:
            from ..exceptions import InvalidAlleleError

            raise InvalidAlleleError(f"{glstring} is not a valid Allele")
        return is_valid_allele
