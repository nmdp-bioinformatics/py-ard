from behave import *
from hamcrest import assert_that, is_

from pyard.exceptions import InvalidAlleleError


@given("the MAC code is {mac_code}")
def step_impl(context, mac_code):
    context.mac_code = mac_code


@when("expanding the MAC")
def step_impl(context):
    context.mac_expansion = context.ard.expand_mac(context.mac_code)


@then("the expanded MAC is {mac_expanded}")
def step_impl(context, mac_expanded):
    assert_that(context.mac_expansion, is_(mac_expanded))


@given("the allele list is {allele_list}")
def step_impl(context, allele_list):
    context.allele_list = allele_list


@when("decoding to a MAC")
def step_impl(context):
    context.mac_code = context.ard.lookup_mac(context.allele_list)


@then("the decoded MAC is {mac_code}")
def step_impl(context, mac_code):
    assert_that(context.mac_code, is_(mac_code))


@when("checking for validity of the MAC")
def step_impl(context):
    try:
        context.is_valid = context.ard.validate(context.mac_code)
    except InvalidAlleleError:
        context.is_valid = False


@then("the validness of MAC is {validity}")
def step_impl(context, validity):
    valid = validity == "Valid"
    assert_that(context.is_valid, is_(valid))
