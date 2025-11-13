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

# drbx blender


def blender(drb1, drb3="", drb4="", drb5=""):
    """Blend DRB1 typing with DRB3/4/5 to determine expected DRBX expression

    The DRB locus region contains multiple genes (DRB1, DRB3, DRB4, DRB5) but
    only certain combinations are expressed based on DRB1 allele families.
    This function validates that the provided DRBX typing matches the expected
    pattern based on DRB1 and returns the appropriate DRBX expression.

    Args:
        drb1: DRB1 typing (e.g., 'DRB1*03:01+DRB1*04:01')
        drb3: DRB3 typing if present
        drb4: DRB4 typing if present
        drb5: DRB5 typing if present

    Returns:
        Expected DRBX expression based on DRB1 families, or empty string

    Raises:
        DRBXBlenderError: If provided DRBX doesn't match expected pattern
    """
    # Parse DRB1 typing to extract allele families
    try:
        drb1_1, drb1_2 = drb1.split("+")
        drb1_allele_1 = drb1_1.split("*")[1]
        drb1_allele_2 = drb1_2.split("*")[1]
        drb1_fam_1 = drb1_allele_1.split(":")[0]  # First field (family)
        drb1_fam_2 = drb1_allele_2.split(":")[0]  # First field (family)
    except Exception:
        return ""
    # Map DRB1 families to expected DRBX genes (3, 4, 5, or 0 for none)
    x1 = expdrbx(drb1_fam_1)
    x2 = expdrbx(drb1_fam_2)
    # Create sorted combination code (e.g., '34', '44', '00')
    xx = "".join(sorted([x1, x2]))

    # Handle case where no DRBX genes should be expressed
    if xx == "00":
        if drb3 != "":
            raise DRBXBlenderError("DRB3", "none")
        if drb4 != "":
            raise DRBXBlenderError("DRB4", "none")
        if drb5 != "":
            raise DRBXBlenderError("DRB5", "none")
        return ""

    # Handle heterozygous case: one allele expresses DRB3, other doesn't
    if xx == "03":
        if drb4 != "":
            raise DRBXBlenderError("DRB4", "none")
        if drb5 != "":
            raise DRBXBlenderError("DRB5", "none")
        if drb3 != "":
            # Check if DRB3 has two copies (homozygous DRB3-expressing alleles)
            drb3_g = drb3.split("+")
            if len(drb3_g) == 2:
                # If homozygous, return one copy
                if drb3_g[1] == drb3_g[0]:
                    return drb3_g[0]
                else:
                    raise DRBXBlenderError("DRB3 het", "hom")
            else:
                return drb3
        return ""

    # Handle heterozygous case: one allele expresses DRB4, other doesn't
    if xx == "04":
        if drb3 != "":
            raise DRBXBlenderError("DRB3", "none")
        if drb5 != "":
            raise DRBXBlenderError("DRB5", "none")
        if drb4 != "":
            # Check if DRB4 has two copies (homozygous DRB4-expressing alleles)
            drb4_g = drb4.split("+")
            if len(drb4_g) == 2:
                # If homozygous, return one copy
                if drb4_g[1] == drb4_g[0]:
                    return drb4_g[0]
                else:
                    raise DRBXBlenderError("DRB4 het", "hom")
            else:
                return drb4
        return ""

    # Handle heterozygous case: one allele expresses DRB5, other doesn't
    if xx == "05":
        if drb3 != "":
            raise DRBXBlenderError("DRB3", "none")
        if drb4 != "":
            raise DRBXBlenderError("DRB4", "none")
        if drb5 != "":
            # Check if DRB5 has two copies (homozygous DRB5-expressing alleles)
            drb5_g = drb5.split("+")
            if len(drb5_g) == 2:
                # If homozygous, return one copy
                if drb5_g[1] == drb5_g[0]:
                    return drb5_g[0]
                else:
                    raise DRBXBlenderError("DRB5 het", "hom")
            else:
                return drb5
        return ""
    # Handle homozygous DRB3-expressing case
    if xx == "33":
        if drb4 != "":
            raise DRBXBlenderError("DRB4", "none")
        if drb5 != "":
            raise DRBXBlenderError("DRB5", "none")
        if drb3 != "":
            return drb3
        return ""

    # Handle homozygous DRB4-expressing case
    if xx == "44":
        if drb3 != "":
            raise DRBXBlenderError("DRB3", "none")
        if drb5 != "":
            raise DRBXBlenderError("DRB5", "none")
        if drb4 != "":
            return drb4
        return ""

    # Handle homozygous DRB5-expressing case
    if xx == "55":
        if drb3 != "":
            raise DRBXBlenderError("DRB3", "none")
        if drb4 != "":
            raise DRBXBlenderError("DRB4", "none")
        if drb5 != "":
            return drb5
        return ""

    # Handle heterozygous case: one allele expresses DRB3, other expresses DRB4
    if xx == "34":
        if drb5 != "":
            raise DRBXBlenderError("DRB5", "none")
        retg = []

        if drb3 != "":
            # Process DRB3 typing
            drb3_g = drb3.split("+")
            if len(drb3_g) == 2:
                # If homozygous, return one copy
                if drb3_g[1] == drb3_g[0]:
                    retg.append(drb3_g[0])
                else:
                    raise DRBXBlenderError("DRB3 het", "hom")
            elif len(drb3_g) == 1:
                retg.append(drb3_g[0])
        if drb4 != "":
            # Process DRB4 typing
            drb4_g = drb4.split("+")
            if len(drb4_g) == 2:
                # If homozygous, return one copy
                if drb4_g[1] == drb4_g[0]:
                    retg.append(drb4_g[0])
                else:
                    raise DRBXBlenderError("DRB4 het", "hom")
            elif len(drb4_g) == 1:
                retg.append(drb4_g[0])

        return "+".join(retg)

    # Handle heterozygous case: one allele expresses DRB3, other expresses DRB5
    if xx == "35":
        if drb4 != "":
            raise DRBXBlenderError("DRB4", "none")
        retg = []

        if drb3 != "":
            # Process DRB3 typing
            drb3_g = drb3.split("+")
            if len(drb3_g) == 2:
                # If homozygous, return one copy
                if drb3_g[1] == drb3_g[0]:
                    retg.append(drb3_g[0])
                else:
                    raise DRBXBlenderError("DRB3 het", "hom")
            elif len(drb3_g) == 1:
                retg.append(drb3_g[0])
        if drb5 != "":
            # Process DRB5 typing
            drb5_g = drb5.split("+")
            if len(drb5_g) == 2:
                # If homozygous, return one copy
                if drb5_g[1] == drb5_g[0]:
                    retg.append(drb5_g[0])
                else:
                    raise DRBXBlenderError("DRB5 het", "hom")
            elif len(drb5_g) == 1:
                retg.append(drb5_g[0])

        return "+".join(retg)

    # Handle heterozygous case: one allele expresses DRB4, other expresses DRB5
    if xx == "45":
        if drb3 != "":
            raise DRBXBlenderError("DRB3", "none")
        retg = []

        if drb4 != "":
            # Process DRB4 typing
            drb4_g = drb4.split("+")
            if len(drb4_g) == 2:
                # If homozygous, return one copy
                if drb4_g[1] == drb4_g[0]:
                    retg.append(drb4_g[0])
                else:
                    raise DRBXBlenderError("DRB4 het", "hom")
            elif len(drb4_g) == 1:
                retg.append(drb4_g[0])
        if drb5 != "":
            # Process DRB5 typing
            drb5_g = drb5.split("+")
            if len(drb5_g) == 2:
                # If homozygous, return one copy
                if drb5_g[1] == drb5_g[0]:
                    retg.append(drb5_g[0])
                else:
                    raise DRBXBlenderError("DRB5 het", "hom")
            elif len(drb5_g) == 1:
                retg.append(drb5_g[0])

        return "+".join(retg)

    print("blender fail", xx, drb1_fam_1, drb1_fam_2)
    return ""


def expdrbx(drb1_fam):
    """Map DRB1 allele family to expected DRBX gene expression

    Different DRB1 allele families are associated with expression of
    different DRBX genes based on linkage disequilibrium patterns.

    Args:
        drb1_fam: DRB1 allele family (first field, e.g., '03', '04', '15')

    Returns:
        String indicating expected DRBX gene:
        '3' for DRB3, '4' for DRB4, '5' for DRB5, '0' for none
    """
    # DRB1 families associated with DRB3 expression
    if drb1_fam in ["03", "05", "06", "11", "12", "13", "14"]:
        return "3"
    # DRB1 families associated with DRB4 expression
    if drb1_fam in ["04", "07", "09"]:
        return "4"
    # DRB1 families associated with DRB5 expression
    if drb1_fam in ["02", "15", "16"]:
        return "5"
    # DRB1 families with no associated DRBX expression
    return "0"


class DRBXBlenderError(Exception):
    """Exception raised when DRBX typing doesn't match expected pattern

    This error occurs when the provided DRB3/4/5 typing is inconsistent
    with what should be expressed based on the DRB1 allele families.
    """

    def __init__(self, found, expected):
        """Initialize the error with found and expected values

        Args:
            found: What was actually provided in the typing
            expected: What should have been provided based on DRB1
        """
        self.found = found
        self.expected = expected

    def __str__(self):
        return f"{self.found} where {self.expected} expected"
