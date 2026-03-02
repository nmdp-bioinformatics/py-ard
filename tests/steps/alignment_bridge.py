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
import itertools

from behave import given, when, then
from hamcrest import assert_that, is_, none, not_none, less_than


# ---------------------------------------------------------------------------
# Helper functions (mirror the notebook implementations)
# ---------------------------------------------------------------------------


def _parse_gl_genotype(genotype, locus):
    """Split a GL diplotype string into a list of haplotype groups.

    '+' separates chromosomes; '/' separates ambiguous alternatives per chromosome.
    Returns a list of lists, e.g. [["DPB1*04:01", "DPB1*04:02"], ["DPB1*02:01"]].
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


def _is_null(allele):
    return allele.upper().endswith("N")


def _analyze_mismatches(bridge, donor_gt, recipient_gt, locus):
    """Return haplotype-level mismatch analysis for a transplant pair."""
    donor_haps = _parse_gl_genotype(donor_gt, locus)
    recip_haps = _parse_gl_genotype(recipient_gt, locus)

    recip_seqs = set()
    for hap in recip_haps:
        for allele in hap:
            if not _is_null(allele):
                seq = bridge.get_sequence(allele)
                if seq is not None:
                    recip_seqs.add(seq)

    haplotype_results = []
    for hap in donor_haps:
        expressed = [a for a in hap if not _is_null(a)]

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


def _mature_redux(bridge, alleles, locus):
    """Collapse alleles with identical mature protein sequences.

    Returns a '/'-joined string of representatives. Groups with >1 member are
    annotated with '[M]'.

    An allele is never collapsed if its mature sequence is None (no reference)
    or contains '*' (unsequenced positions — identity cannot be confirmed).
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


def _compute_aamm(bridge, donor_alleles, recip_alleles):
    """Return the frozenset of (1-based position, donor_aa) AAMM pairs."""
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


def _check_identical_aamm(bridge, donor_gt, recip_gt, locus):
    """Enumerate all phasing combinations and check whether they all share the same AAMM."""
    donor_haps = _parse_gl_genotype(donor_gt, locus)
    recip_haps = _parse_gl_genotype(recip_gt, locus)

    d_chr1 = [a for a in donor_haps[0] if not _is_null(a)]
    d_chr2 = [a for a in donor_haps[1] if not _is_null(a)]
    r_chr1 = [a for a in recip_haps[0] if not _is_null(a)]
    r_chr2 = [a for a in recip_haps[1] if not _is_null(a)]

    aamm_sets = []
    for d1, d2, r1, r2 in itertools.product(d_chr1, d_chr2, r_chr1, r_chr2):
        aamm = _compute_aamm(bridge, [d1, d2], [r1, r2])
        aamm_sets.append(aamm)

    unique = {s for s in aamm_sets if s is not None}
    identical = len(unique) == 1
    return {
        "identical_aamm": identical,
        "unique_aamm_count": len(unique),
        "common_aamm": next(iter(unique)) if identical else None,
    }


# ---------------------------------------------------------------------------
# Given steps
# ---------------------------------------------------------------------------


@given("the HLAtools bridge is initialised")
def step_impl(context):
    pass  # bridge is set up in environment.before_all


@given("the HLA allele {allele}")
def step_impl(context, allele):
    context.hla_allele = allele.strip()


@given("the second HLA allele {allele}")
def step_impl(context, allele):
    context.hla_allele2 = allele.strip()


@given("the donor genotype {genotype}")
def step_impl(context, genotype):
    context.donor_genotype = genotype.strip()


@given("the recipient genotype {genotype}")
def step_impl(context, genotype):
    context.recipient_genotype = genotype.strip()


@given("the locus is {locus}")
def step_impl(context, locus):
    context.locus = locus.strip()


@given("the ambiguous allele group {group}")
def step_impl(context, group):
    context.allele_group = group.strip()


# ---------------------------------------------------------------------------
# When steps
# ---------------------------------------------------------------------------


@when("looking up the full protein sequence")
def step_impl(context):
    context.full_sequence = context.bridge.get_sequence(context.hla_allele)


@when("looking up full and mature protein sequences")
def step_impl(context):
    context.full_sequence = context.bridge.get_sequence(context.hla_allele)
    context.mature_sequence = context.bridge.get_mature_sequence(context.hla_allele)


@when("comparing the two allele sequences")
def step_impl(context):
    seq1 = context.bridge.get_sequence(context.hla_allele)
    seq2 = context.bridge.get_sequence(context.hla_allele2)
    if seq1 is None or seq2 is None:
        context.mismatch_count = None
        return
    context.mismatch_count = sum(1 for a, b in zip(seq1, seq2) if a != b)


@when("building the position mapping")
def step_impl(context):
    mapping = context.bridge.get_position_mapping(context.locus)
    context.leader_count = sum(1 for pos in mapping.values() if pos < 1)
    context.mature_count = sum(1 for pos in mapping.values() if pos >= 1)


@when("analyzing transplant mismatches")
def step_impl(context):
    context.mismatch_result = _analyze_mismatches(
        context.bridge,
        context.donor_genotype,
        context.recipient_genotype,
        context.locus,
    )


@when("applying M redux for locus {locus}")
def step_impl(context, locus):
    alleles = [a.strip() for a in context.allele_group.split("/")]
    context.redux_result = _mature_redux(context.bridge, alleles, locus.strip())


@when("checking for identical AAMM")
def step_impl(context):
    context.aamm_result = _check_identical_aamm(
        context.bridge,
        context.donor_genotype,
        context.recipient_genotype,
        context.locus,
    )


# ---------------------------------------------------------------------------
# Then steps
# ---------------------------------------------------------------------------


@then("the bridge is available")
def step_impl(context):
    assert_that(context.hlatools_available, is_(True))


@then("the full sequence length is {length}")
def step_impl(context, length):
    assert_that(context.full_sequence, not_none())
    assert_that(len(context.full_sequence), is_(int(length)))


@then("the mature sequence is {leader} amino acids shorter than the full sequence")
def step_impl(context, leader):
    assert_that(context.full_sequence, not_none())
    assert_that(context.mature_sequence, not_none())
    assert_that(context.mature_sequence, not_none())
    delta = len(context.full_sequence) - len(context.mature_sequence)
    assert_that(delta, is_(int(leader)))


@then("no sequence is found")
def step_impl(context):
    assert_that(context.full_sequence, none())


@then("the comparison yields {n} amino acid mismatches")
def step_impl(context, n):
    assert_that(context.mismatch_count, is_(int(n)))


@then(
    "the position mapping has {leader} leader positions and {mature} mature positions"
)
def step_impl(context, leader, mature):
    assert_that(context.leader_count, is_(int(leader)))
    assert_that(context.mature_count, is_(int(mature)))


@then("the mismatch count is {n}")
def step_impl(context, n):
    assert_that(context.mismatch_result["mismatch_count"], is_(int(n)))


@then("the haplotype {allele_str} has status {status}")
def step_impl(context, allele_str, status):
    allele_str = allele_str.strip()
    for result in context.mismatch_result["haplotype_results"]:
        candidate = "/".join(result["alleles"])
        if candidate == allele_str:
            assert_that(result["status"], is_(status))
            return
    raise AssertionError(
        f"No haplotype matching '{allele_str}' found in results. "
        f"Available: {['/'.join(r['alleles']) for r in context.mismatch_result['haplotype_results']]}"
    )


@then("the M redux result is {result}")
def step_impl(context, result):
    assert_that(context.redux_result, is_(result.strip()))


@then("the AAMM is identical: {identical}")
def step_impl(context, identical):
    expected = identical.strip() == "True"
    assert_that(context.aamm_result["identical_aamm"], is_(expected))


@then("the number of distinct AAMM sets is {n}")
def step_impl(context, n):
    assert_that(context.aamm_result["unique_aamm_count"], is_(int(n)))


@then("the number of common AAMM positions is {n}")
def step_impl(context, n):
    common = context.aamm_result["common_aamm"]
    assert_that(common, not_none())
    assert_that(len(common), is_(int(n)))
