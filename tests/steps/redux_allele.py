from behave import given, when, then
from hamcrest import assert_that, is_


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
    context.redux_allele = context.ard.redux_gl(context.allele, level)


@then('the reduced allele is found to be {redux_allele}')
def step_impl(context, redux_allele):
    assert_that(context.redux_allele, is_(redux_allele))


@given("the serology typing is {serology}")
def step_impl(context, serology):
    context.allele = serology


@given("the version 2 typing is {v2_allele}")
def step_impl(context, v2_allele):
    context.allele = v2_allele
