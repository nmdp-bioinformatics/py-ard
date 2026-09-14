from ..misc import get_1field_allele
from .base_reducer import Reducer


class FirstFieldReducer(Reducer):
    """
    Strategy for 1F (First Field) reduction of HLA alleles.

    Reduces an allele to its first field only (locus + allele group).

    Examples:
        - A*01:01:01:01 -> A*01
        - B*07:02:01    -> B*07
        - DRB1*15:01    -> DRB1*15
    """

    def reduce(self, allele: str) -> str:
        return get_1field_allele(allele)
