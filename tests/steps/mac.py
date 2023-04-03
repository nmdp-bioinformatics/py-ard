from behave import *
from hamcrest import assert_that, is_


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
