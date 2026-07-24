# -*- coding: utf-8 -*-

from .base_reducer import Reducer
from .. import db


class HATSReducer(Reducer):
    """
    Strategy for HATS (HLA Antigen Typing Specificity) reduction of HLA alleles.

    Reduces an allele to its HATS value by looking up the antigen_specifities
    table. Only available for IPD-IMGT/HLA version >= 3.64.0.

    If no HATS value is found (e.g. the allele is not in the table, or the
    database predates 3.64.0), an empty string is returned

    Examples:
        - A*01:01:01:01 -> A1   (mapped)
        - A*01:01       -> A1   (mapped)
        - B*44:450      -> 4402 (mapped)
        - B*44:458      -> ''   (not mapped)
    """

    def reduce(self, allele: str) -> str:
        result = db.find_hats(self.ard.db_connection, allele)
        return result if result is not None else ""
