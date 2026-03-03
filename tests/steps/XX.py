from behave import *
from hamcrest import assert_that, is_


@given("the XX code is {xx_code}")
def step_impl(context, xx_code):
    context.xx_code = xx_code


@when("expanding the XX code")
def step_impl(context):
    context.expanded_alleles = context.ard.expand_xx(context.xx_code)


@then("the expanded XX code is {expanded_alleles}")
def step_impl(context, expanded_alleles):
    assert_that(context.expanded_alleles, is_(expanded_alleles))
