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
from hamcrest import assert_that, is_

from pyard.exceptions import PyArdError, InvalidAlleleError


@given("the allele as {allele}")
def step_impl(context, allele):
    context.allele = allele


@when("reducing on the {level} level")
def step_impl(context, level):
    context.level = level
    context.redux_allele = context.ard.redux(context.allele, level)


@when("reducing on the {level} level with ping")
def step_impl(context, level):
    context.level = level
    redux_allele = context.ard_ping.redux(context.allele, level)
    if not redux_allele:
        context.redux_allele = "X"
    else:
        context.redux_allele = redux_allele


@when("reducing on the {level} level with ARS suffix enabled")
def step_impl(context, level):
    context.level = level
    context.redux_allele = context.ard_ars.redux(context.allele, level)


@when("reducing on the {level} level (ambiguous)")
def step_impl(context, level):
    context.level = level
    try:
        context.redux_allele = context.ard.redux(context.allele, level)
    except PyArdError:
        context.redux_allele = "X"


@then("the reduced allele is found to be {redux_allele}")
def step_impl(context, redux_allele):
    assert_that(context.redux_allele, is_(redux_allele))


@given("the serology typing is {serology}")
def step_impl(context, serology):
    context.allele = serology


@given("the version 2 typing is {v2_allele}")
def step_impl(context, v2_allele):
    context.allele = v2_allele


@when("validating the V2 typing")
def step_impl(context):
    try:
        context.is_valid = context.ard.validate(context.allele)
    except InvalidAlleleError:
        context.is_valid = False


@then("the validness of V2 typing is {validity}")
def step_impl(context, validity):
    valid = validity == "Valid"
    assert_that(context.is_valid, is_(valid))


@given("the typing is {allele}")
def step_impl(context, allele):
    context.allele = allele


@when("expanding at the {level} level")
def step_impl(context, level):
    context.expanded_alleles = context.ard.redux(context.allele, level)


@when("expanding to WHO then reducing to the {level} level")
def step_impl(context, level):
    context.expanded_alleles = context.ard.redux(
        context.ard.redux(context.allele, "W"), level
    )


@then("the expanded allele is found to be {expanded_alleles}")
def step_impl(context, expanded_alleles):
    assert_that(context.expanded_alleles, is_(expanded_alleles))


@when("reducing on the {level} level in non-strict mode")
def step_impl(context, level):
    context.level = level
    context.redux_allele = context.ard_non_strict.redux(context.allele, level)


@when("checking for validity of the allele in non-strict mode")
def step_impl(context):
    try:
        context.is_valid = context.ard_non_strict.validate(context.allele)
    except InvalidAlleleError:
        context.is_valid = False


@then("the validness of the allele is {validity}")
def step_impl(context, validity):
    valid = validity == "Valid"
    assert_that(context.is_valid, is_(valid))
