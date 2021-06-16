from typing import Tuple, List


def map_drbx(drb_alleles: List, locus_in_allele_name: bool) -> Tuple:
    """
    Generates a pair of DRBX Typings based on DRB3, DRB4 and DRB5 typings.
    Expects Type1 and Type2 DRB3, DRB4 and DRB5 typings in that order
    in `drb_alleles` list.

    Reference:
    World Marrow Donor Association guidelines for use of HLA nomenclature
    and its validation in the data exchange among hematopoietic
    stem cell donor registries and cord blood banks
    https://www.nature.com/articles/1705672

    :param drb_alleles: Type1/Type2 DRB3, DRB4 and DRB5 typings.
    :param locus_in_allele_name: Does typing include DRBn prefix?
    :return: Tuple of DRBX type1/type2
    """

    nnnn = 'NNNN'
    if locus_in_allele_name:
        nnnn = 'DRBX*NNNN'

    # Get the ones DRBs without NNNNs
    drbx_non_nns = list(filter(lambda x: x != '' and not x.endswith('NNNN'), drb_alleles))
    if len(drbx_non_nns) == 0:
        return nnnn, nnnn

    # There can only be at most 2 DRBn loci present
    if len(drbx_non_nns) == 2:
        # If they are homozygous, return a single DRBn only
        if drbx_non_nns[0] == drbx_non_nns[1]:
            return drbx_non_nns[0], ''
        # Else return drbx_1 and drbx_2
        return tuple(drbx_non_nns)

    # If there's only a single DRBn, return NNNN as the second typing
    if len(drbx_non_nns) == 1:
        return drbx_non_nns[0], nnnn

    # Everything else is NNNNs
    return nnnn, nnnn
