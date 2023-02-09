from behave import *
from hamcrest import assert_that, is_

import pyard


@given("the broad allele/serology is {broad}")
def step_impl(context, broad):
    context.broad = broad


@when("it is expanded to the splits")
def step_impl(context):
    mapping = pyard.find_broad_splits(context.broad)
    splits = mapping[1]
    context.splits = "/".join(splits)


@then("the splits are {splits}")
def step_impl(context, splits):
    assert_that(context.splits, is_(splits))


@given("the split allele/serology is {split}")
def step_impl(context, split):
    context.split = split


@when("split is searched in the mappings")
def step_impl(context):
    mapping = pyard.find_broad_splits(context.split)
    context.broad = mapping[0]
    splits = mapping[1]
    splits.remove(context.split)
    context.siblings = "/".join(splits)


@then("the sibling splits are {siblings}")
def step_impl(context, siblings):
    assert_that(context.siblings, is_(siblings))


@step("the corresponding broad is {broad}")
def step_impl(context, broad):
    assert_that(context.broad, is_(broad))
