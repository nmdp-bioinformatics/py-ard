from behave import *
from hamcrest import is_, assert_that


@given('the MAC Code we want to find CWD of is "{mac_code}"')
def step_impl(context, mac_code):
    context.mac_code = mac_code


@when("we reduce MAC code to lgx and find CWD alleles in the expansion")
def step_impl(context):
    context.cwd = context.ard.cwd_redux(context.mac_code)


@then('the CWD alleles should be "{cwd_list}"')
def step_impl(context, cwd_list):
    assert_that(context.cwd, is_(cwd_list))


@step('the MAC Code for CWD alleles should be "{cwd_mac}"')
def step_impl(context, cwd_mac):
    mac = context.ard.lookup_mac(context.cwd)
    assert_that(mac, is_(cwd_mac))


@given('the GL String we want to find CWD of is "{gl_string}"')
def step_impl(context, gl_string):
    context.gl_string = gl_string


@when("we find CWD alleles for the GL String")
def step_impl(context):
    context.cwd = context.ard_non_strict.cwd_redux(context.gl_string)
