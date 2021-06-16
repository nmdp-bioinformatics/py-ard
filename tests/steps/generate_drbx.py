from behave import *
from hamcrest import assert_that, is_

from pyard.drbx import map_drbx


@given("a subject has {arg0} and {arg1} DRB3 alleles")
def step_impl(context, arg0, arg1):
    context.drb3_1 = '' if arg0 == 'x' else arg0
    context.drb3_2 = '' if arg1 == 'x' else arg1


@step("a subject has {arg0} and {arg1} DRB4 alleles")
def step_impl(context, arg0, arg1):
    context.drb4_1 = '' if arg0 == 'x' else arg0
    context.drb4_2 = '' if arg1 == 'x' else arg1


@step("a subject has {arg0} and {arg1} DRB5 alleles")
def step_impl(context, arg0, arg1):
    context.drb5_1 = '' if arg0 == 'x' else arg0
    context.drb5_2 = '' if arg1 == 'x' else arg1


@when("I create a DRBX genotype")
def step_impl(context):
    drbs = [
        context.drb3_1, context.drb3_2,
        context.drb4_1, context.drb4_2,
        context.drb5_1, context.drb5_2
    ]
    context.drbx = map_drbx(drbs, True)


@then("it should be {drbx1} and {drbx2}")
def step_impl(context, drbx1, drbx2):
    expected_drbx_1 = '' if drbx1 == 'x' else drbx1
    expected_drbx_2 = '' if drbx2 == 'x' else drbx2
    expected_drbx = (expected_drbx_1, expected_drbx_2)
    assert_that(context.drbx, is_(expected_drbx))
