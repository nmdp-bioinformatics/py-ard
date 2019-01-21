# glstring
# module for working with glstrings

import re


# convert genotype ambiguity into allele ambiguity

# TODO: need to handle "^" character

def flatten (gls):
    # if gls contains ^
    if re.search("\^", gls):
        # loop over all loci
        return "^".join(flatten_loc(g) for g in gls.split("^"))
    else:
        return flatten_loc(gls)
        

def flatten_loc (gls):
    # if gls contains |
    if re.search("\|", gls):
        # loop over all genos
        typ1 = dict()
        typ2 = dict()
        for geno in gls.split("|"):
            # split on +
            if not re.search("\+", geno):
                print("geno ", geno, " has no +")
            t1, t2 = geno.split("+")
            # add to hash1, hash2
            typ1[t1]=1
            typ2[t2]=1

        # join keys by /
        newt1 = "/".join(sorted(typ1.keys()))
        newt2 = "/".join(sorted(typ2.keys()))
        # join these by +
        newgeno = "+".join([newt1, newt2])
        return(newgeno)
    else: 
        return (gls)
