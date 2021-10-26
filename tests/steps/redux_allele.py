from behave import given, when, then
from hamcrest import assert_that, is_

from pyard.exceptions import PyArdError


@given('the allele as {allele}')
def step_impl(context, allele):
    context.allele = allele


@when('reducing on the {level} level')
def step_impl(context, level):
    context.level = level
    context.redux_allele = context.ard.redux(context.allele, level)


@when('reducing on the {level} level (ambiguous)')
def step_impl(context, level):
    context.level = level
    try:
        context.redux_allele = context.ard.redux_gl(context.allele, level)
    except PyArdError:
        context.redux_allele = 'X'


@then('the reduced allele is found to be {redux_allele}')
def step_impl(context, redux_allele):
    assert_that(context.redux_allele, is_(redux_allele))


@given("the serology typing is {serology}")
def step_impl(context, serology):
    context.allele = serology


@given("the version 2 typing is {v2_allele}")
def step_impl(context, v2_allele):
    context.allele = v2_allele


@given("the typing is {allele}")
def step_impl(context, allele):
    context.allele = allele


@when("expanding at the {level} level")
def step_impl(context, level):
    context.expanded_alleles = context.ard.redux_gl(context.allele, level)


@when("expanding to WHO then reducing to the {level} level")
def step_impl(context, level):
    context.expanded_alleles = context.ard.redux_gl(context.ard.redux_gl(context.allele, "W"), level)


@then("the expanded allele is found to be {expanded_alleles}")
def step_impl(context, expanded_alleles):
    assert_that(context.expanded_alleles, is_(expanded_alleles))
