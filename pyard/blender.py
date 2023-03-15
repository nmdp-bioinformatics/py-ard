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
    try:
        drb1_1, drb1_2 = drb1.split("+")
        drb1_allele_1 = drb1_1.split("*")[1]
        drb1_allele_2 = drb1_2.split("*")[1]
        drb1_fam_1 = drb1_allele_1.split(":")[0]
        drb1_fam_2 = drb1_allele_2.split(":")[0]
    except Exception:
        return ""
    x1 = expdrbx(drb1_fam_1)
    x2 = expdrbx(drb1_fam_2)
    xx = "".join(sorted([x1, x2]))

    if xx == "00":
        if drb3 != "":
            raise DRBXBlenderError("DRB3", "none")
        if drb4 != "":
            raise DRBXBlenderError("DRB4", "none")
        if drb5 != "":
            raise DRBXBlenderError("DRB5", "none")
        return ""

    # handle 03
    if xx == "03":
        if drb4 != "":
            raise DRBXBlenderError("DRB4", "none")
        if drb5 != "":
            raise DRBXBlenderError("DRB5", "none")
        if drb3 != "":
            # if 2 copies
            drb3_g = drb3.split("+")
            if len(drb3_g) == 2:
                # homozygous, return one copy
                if drb3_g[1] == drb3_g[0]:
                    return drb3_g[0]
                else:
                    raise DRBXBlenderError("DRB3 het", "hom")
            else:
                return drb3
        return ""

    # handle 04
    if xx == "04":
        if drb3 != "":
            raise DRBXBlenderError("DRB3", "none")
        if drb5 != "":
            raise DRBXBlenderError("DRB5", "none")
        if drb4 != "":
            # if 2 copies
            drb4_g = drb4.split("+")
            if len(drb4_g) == 2:
                # homozygous, return one copy
                if drb4_g[1] == drb4_g[0]:
                    return drb4_g[0]
                else:
                    raise DRBXBlenderError("DRB4 het", "hom")
            else:
                return drb4
        return ""

    # handle 05
    if xx == "05":
        if drb3 != "":
            raise DRBXBlenderError("DRB3", "none")
        if drb4 != "":
            raise DRBXBlenderError("DRB4", "none")
        if drb5 != "":
            # if 2 copies
            drb5_g = drb5.split("+")
            if len(drb5_g) == 2:
                # homozygous, return one copy
                if drb5_g[1] == drb5_g[0]:
                    return drb5_g[0]
                else:
                    raise DRBXBlenderError("DRB5 het", "hom")
            else:
                return drb5
        return ""
    # handle 33
    if xx == "33":
        if drb4 != "":
            raise DRBXBlenderError("DRB4", "none")
        if drb5 != "":
            raise DRBXBlenderError("DRB5", "none")
        if drb3 != "":
            return drb3
        return ""

    # handle 44
    if xx == "44":
        if drb3 != "":
            raise DRBXBlenderError("DRB3", "none")
        if drb5 != "":
            raise DRBXBlenderError("DRB5", "none")
        if drb4 != "":
            return drb4
        return ""

    # handle 55
    if xx == "55":
        if drb3 != "":
            raise DRBXBlenderError("DRB3", "none")
        if drb4 != "":
            raise DRBXBlenderError("DRB4", "none")
        if drb5 != "":
            return drb5
        return ""

    # handle 34
    if xx == "34":
        if drb5 != "":
            raise DRBXBlenderError("DRB5", "none")
        retg = []

        if drb3 != "":
            # if 2 copies
            drb3_g = drb3.split("+")
            if len(drb3_g) == 2:
                # homozygous, return one copy
                if drb3_g[1] == drb3_g[0]:
                    retg.append(drb3_g[0])
                else:
                    raise DRBXBlenderError("DRB3 het", "hom")
            elif len(drb3_g) == 1:
                retg.append(drb3_g[0])
        if drb4 != "":
            # if 2 copies
            drb4_g = drb4.split("+")
            if len(drb4_g) == 2:
                # homozygous, return one copy
                if drb4_g[1] == drb4_g[0]:
                    retg.append(drb4_g[0])
                else:
                    raise DRBXBlenderError("DRB4 het", "hom")
            elif len(drb4_g) == 1:
                retg.append(drb4_g[0])

        return "+".join(retg)

    # handle 35
    if xx == "35":
        if drb4 != "":
            raise DRBXBlenderError("DRB4", "none")
        retg = []

        if drb3 != "":
            # if 2 copies
            drb3_g = drb3.split("+")
            if len(drb3_g) == 2:
                # homozygous, return one copy
                if drb3_g[1] == drb3_g[0]:
                    retg.append(drb3_g[0])
                else:
                    raise DRBXBlenderError("DRB3 het", "hom")
            elif len(drb3_g) == 1:
                retg.append(drb3_g[0])
        if drb5 != "":
            # if 2 copies
            drb5_g = drb5.split("+")
            if len(drb5_g) == 2:
                # homozygous, return one copy
                if drb5_g[1] == drb5_g[0]:
                    retg.append(drb5_g[0])
                else:
                    raise DRBXBlenderError("DRB5 het", "hom")
            elif len(drb5_g) == 1:
                retg.append(drb5_g[0])

        return "+".join(retg)

    # handle 45
    if xx == "45":
        if drb3 != "":
            raise DRBXBlenderError("DRB3", "none")
        retg = []

        if drb4 != "":
            # if 2 copies
            drb4_g = drb4.split("+")
            if len(drb4_g) == 2:
                # homozygous, return one copy
                if drb4_g[1] == drb4_g[0]:
                    retg.append(drb4_g[0])
                else:
                    raise DRBXBlenderError("DRB4 het", "hom")
            elif len(drb4_g) == 1:
                retg.append(drb4_g[0])
        if drb5 != "":
            # if 2 copies
            drb5_g = drb5.split("+")
            if len(drb5_g) == 2:
                # homozygous, return one copy
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
    if drb1_fam in ["03", "05", "06", "11", "12", "13", "14"]:
        return "3"
    if drb1_fam in ["04", "07", "09"]:
        return "4"
    if drb1_fam in ["02", "15", "16"]:
        return "5"
    return "0"


class DRBXBlenderError(Exception):
    def __init__(self, found, expected):
        self.found = found
        self.expected = expected

    def __str__(self):
        return f"{self.found} where {self.expected} expected"
