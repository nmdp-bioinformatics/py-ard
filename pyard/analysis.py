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
"""HLA alignment analysis functions.

Standalone functions for mature-protein redux and AAMM (amino acid mismatch)
analysis using a HLAToolsBridge for alignment data. These are intentionally
separate from ARD (which handles nomenclature reduction) because they depend
on rpy2/HLAtools rather than the IMGT database.
"""
import itertools
from typing import Dict, List, Optional


def parse_gl_genotype(genotype: str, locus: str) -> List[List[str]]:
    """Split a GL diplotype string into a list of haplotype groups.

    '+' separates chromosomes; '/' separates ambiguous alternatives per chromosome.

    Args:
        genotype: GL string, e.g. ``"DPB1*04:01/04:02+DPB1*02:01"``.
        locus: Locus name used to expand bare field strings, e.g. ``"DPB1"``.

    Returns:
        List of lists, e.g. ``[["DPB1*04:01", "DPB1*04:02"], ["DPB1*02:01"]]``.
    """
    result = []
    for hap_str in genotype.replace("HLA-", "").strip().split("+"):
        alleles = []
        for raw in hap_str.split("/"):
            raw = raw.strip()
            if not raw:
                continue
            if "*" not in raw:
                raw = f"{locus}*{raw}"
            alleles.append(raw)
        if alleles:
            result.append(alleles)
    return result


def is_null_allele(allele: str) -> bool:
    """Return True if the allele has null expression (ends with 'N')."""
    return allele.upper().endswith("N")


def analyze_mismatches(bridge, donor_gt: str, recipient_gt: str, locus: str) -> Dict:
    """Return haplotype-level mismatch analysis for a transplant pair.

    Args:
        bridge: A :class:`~pyard.alignment_bridge.HLAToolsBridge` instance.
        donor_gt: Donor GL genotype string.
        recipient_gt: Recipient GL genotype string.
        locus: HLA locus (e.g. ``"DPB1"``).

    Returns:
        Dict with keys:

        - ``"haplotype_results"``: list of per-haplotype dicts, each with
          ``"alleles"``, ``"status"`` (``"match"``, ``"mismatch"``,
          ``"possible_match"``, or ``"null"``), and ``"is_mismatch"`` (bool).
        - ``"mismatch_count"``: number of haplotypes classified as mismatch.
    """
    donor_haps = parse_gl_genotype(donor_gt, locus)
    recip_haps = parse_gl_genotype(recipient_gt, locus)

    recip_seqs = set()
    for hap in recip_haps:
        for allele in hap:
            if not is_null_allele(allele):
                seq = bridge.get_sequence(allele)
                if seq is not None:
                    recip_seqs.add(seq)

    haplotype_results = []
    for hap in donor_haps:
        expressed = [a for a in hap if not is_null_allele(a)]

        if not expressed:
            haplotype_results.append(
                {
                    "alleles": hap,
                    "status": "null",
                    "is_mismatch": False,
                }
            )
            continue

        seq_map = {a: bridge.get_sequence(a) for a in expressed}
        matched = [a for a, s in seq_map.items() if s is not None and s in recip_seqs]
        unmatched = [a for a, s in seq_map.items() if s is None or s not in recip_seqs]

        if matched and unmatched:
            status = "possible_match"
        elif matched:
            status = "match"
        else:
            status = "mismatch"

        haplotype_results.append(
            {
                "alleles": hap,
                "status": status,
                "is_mismatch": status == "mismatch",
            }
        )

    return {
        "haplotype_results": haplotype_results,
        "mismatch_count": sum(r["is_mismatch"] for r in haplotype_results),
    }


def mature_protein_redux(bridge, alleles: List[str]) -> str:
    """Collapse alleles with identical mature protein sequences.

    Returns a ``'/'``-joined string of representatives. Groups with more than
    one member are annotated with ``[M]``.

    An allele is never collapsed if its mature sequence is ``None`` (no
    reference) or contains ``'*'`` (unsequenced positions — identity cannot be
    confirmed).

    Args:
        bridge: A :class:`~pyard.alignment_bridge.HLAToolsBridge` instance.
        alleles: List of allele names to consider.

    Returns:
        Reduced ``'/'``-delimited string, e.g. ``"DQA1*05:01[M]/DQA1*99:99"``.
    """
    seen_seqs = {}
    groups = {}
    for allele in alleles:
        seq = bridge.get_mature_sequence(allele)
        if seq is None or "*" in seq:
            groups[allele] = [allele]
            continue
        if seq not in seen_seqs:
            seen_seqs[seq] = allele
            groups[allele] = [allele]
        else:
            groups[seen_seqs[seq]].append(allele)

    representatives = []
    for rep, members in groups.items():
        representatives.append(f"{rep}[M]" if len(members) > 1 else rep)
    return "/".join(representatives)


def compute_aamm(
    bridge, donor_alleles: List[str], recip_alleles: List[str]
) -> Optional[frozenset]:
    """Return the frozenset of ``(1-based position, donor_aa)`` AAMM pairs.

    Args:
        bridge: A :class:`~pyard.alignment_bridge.HLAToolsBridge` instance.
        donor_alleles: List of donor allele names for one phasing combination.
        recip_alleles: List of recipient allele names for one phasing combination.

    Returns:
        Frozenset of ``(int position, str amino_acid)`` tuples, or ``None`` if
        any sequence is unavailable.
    """
    donor_seqs = [bridge.get_sequence(a) for a in donor_alleles]
    recip_seqs = [bridge.get_sequence(a) for a in recip_alleles]

    if any(s is None for s in donor_seqs + recip_seqs):
        return None

    seq_len = min(len(s) for s in donor_seqs + recip_seqs)
    aamm = set()
    for pos in range(seq_len):
        recip_aas = {s[pos] for s in recip_seqs}
        for d_seq in donor_seqs:
            if d_seq[pos] not in recip_aas:
                aamm.add((pos + 1, d_seq[pos]))
    return frozenset(aamm)


def check_identical_aamm(bridge, donor_gt: str, recip_gt: str, locus: str) -> Dict:
    """Enumerate all phasing combinations and check whether they all share the same AAMM.

    "Identical AAMM" means phasing uncertainty doesn't change the clinical
    assessment — not necessarily that there are zero mismatches.

    Args:
        bridge: A :class:`~pyard.alignment_bridge.HLAToolsBridge` instance.
        donor_gt: Donor GL genotype string.
        recip_gt: Recipient GL genotype string.
        locus: HLA locus (e.g. ``"DPB1"``).

    Returns:
        Dict with keys:

        - ``"identical_aamm"`` (bool): True if all phasing combos yield the same AAMM.
        - ``"unique_aamm_count"`` (int): Number of distinct AAMM sets observed.
        - ``"common_aamm"`` (frozenset | None): The shared AAMM set when identical,
          otherwise ``None``.
    """
    donor_haps = parse_gl_genotype(donor_gt, locus)
    recip_haps = parse_gl_genotype(recip_gt, locus)

    d_chr1 = [a for a in donor_haps[0] if not is_null_allele(a)]
    d_chr2 = [a for a in donor_haps[1] if not is_null_allele(a)]
    r_chr1 = [a for a in recip_haps[0] if not is_null_allele(a)]
    r_chr2 = [a for a in recip_haps[1] if not is_null_allele(a)]

    aamm_sets = []
    for d1, d2, r1, r2 in itertools.product(d_chr1, d_chr2, r_chr1, r_chr2):
        aamm = compute_aamm(bridge, [d1, d2], [r1, r2])
        aamm_sets.append(aamm)

    unique = {s for s in aamm_sets if s is not None}
    identical = len(unique) == 1
    return {
        "identical_aamm": identical,
        "unique_aamm_count": len(unique),
        "common_aamm": next(iter(unique)) if identical else None,
    }
