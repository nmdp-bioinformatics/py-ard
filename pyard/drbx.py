#
#    py-ard
#    Copyright (c) 2023 Be The Match operated by National Marrow Donor Program. All Rights Reserved.
#
#    This library is free software; you can redistribute it and/or modify it
#    under the terms of the GNU Lesser General Public License as published
#    by the Free Software Foundation; either version 3 of the License, or (at
#    your option) any later version.
#
#    This library is distributed in the hope that it will be useful, but WITHOUT
#    ANY WARRANTY; with out even the implied warranty of MERCHANTABILITY or
#    FITNESS FOR A PARTICULAR PURPOSE.  See the GNU Lesser General Public
#    License for more details.
#
#    You should have received a copy of the GNU Lesser General Public License
#    along with this library;  if not, write to the Free Software Foundation,
#    Inc., 59 Temple Place, Suite 330, Boston, MA 02111-1307  USA.
#
#    > http://www.fsf.org/licensing/licenses/lgpl.html
#    > http://www.opensource.org/licenses/lgpl-license.php
#
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

    nnnn = "NNNN"
    if locus_in_allele_name:
        nnnn = "DRBX*NNNN"

    # Get the ones DRBs without NNNNs
    drbx_non_nns = list(
        filter(lambda x: x != "" and not x.endswith("NNNN"), drb_alleles)
    )
    if len(drbx_non_nns) == 0:
        return nnnn, nnnn

    # There can only be at most 2 DRBn loci present
    if len(drbx_non_nns) == 2:
        # If they are homozygous, return a single DRBn only
        if drbx_non_nns[0] == drbx_non_nns[1]:
            return drbx_non_nns[0], ""
        # Else return drbx_1 and drbx_2
        return tuple(drbx_non_nns)

    # If there's only a single DRBn, return NNNN as the second typing
    if len(drbx_non_nns) == 1:
        return drbx_non_nns[0], nnnn

    # Everything else is NNNNs
    return nnnn, nnnn
