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
        - A*01:01:01:01 -> A1     (mapped)
        - A*01:01       -> A1     (mapped)
        - B*44:450      -> B4402  (mapped)
        - B*35:570      -> Cw0408 (mapped)
        - B*44:458      -> ''     (not mapped)
    """

    def reduce(self, allele: str) -> str:
        result = db.find_hats(self.ard.db_connection, allele)
        if result:
            locus, _ = allele.split("*")
            # For those that already have an assigned locus e.g. Cw0408
            if result[0].isalpha():
                return result
            if locus == "C":
                return f"Cw{result}"
            if locus in ("DRB1", "DRB3", "DRB4", "DRB5"):
                return f"DR{result}"
            if locus in ("DQA1", "DQA2"):
                return f"DQA{result}"
            if locus in ("DQB1", "DQB2"):
                return f"DQ{result}"
            if locus in ("DPA1", "DPA2"):
                return f"DPA{result}"
            if locus in ("DPB1", "DPB2"):
                return f"DPB{result}"
            return f"{locus}{result}"
        return ""
