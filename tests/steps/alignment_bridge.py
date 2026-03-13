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
from behave import given, when, then
from hamcrest import assert_that, is_, none, not_none

from pyard.analysis import (
    parse_gl_genotype as _parse_gl_genotype,
    is_null_allele as _is_null,
    analyze_mismatches as _analyze_mismatches,
    mature_protein_redux as _mature_redux,
    compute_aamm as _compute_aamm,
    check_identical_aamm as _check_identical_aamm,
)


# ---------------------------------------------------------------------------
# Given steps
# ---------------------------------------------------------------------------


@given("the HLAtools bridge is initialised")
def step_impl(context):
    pass  # bridge is set up in environment.before_all


@given("the HLA allele {allele}")
def step_impl(context, allele):
    value = allele.strip()
    context.hla_allele = "" if value == "(empty)" else value


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
    context.redux_result = _mature_redux(context.bridge, alleles)


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
