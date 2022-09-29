from behave import *
from hamcrest import assert_that, is_, calling, raises

import pyard
from pyard.blender import DRBXBlenderError


@given("a subject has {DRB1_SLUG} DRB1 SLUG")
def step_impl(context, DRB1_SLUG):
    context.drb1_slug = DRB1_SLUG


@given("a subject has {DRB3} DRB3 allele")
def step_impl(context, DRB3):
    context.drb3 = DRB3 if DRB3 != "no" else ""


@step("a subject has {DRB4} DRB4 allele")
def step_impl(context, DRB4):
    context.drb4 = DRB4 if DRB4 != "no" else ""


@step("a subject has {DRB5} DRB5 allele")
def step_impl(context, DRB5):
    context.drb5 = DRB5 if DRB5 != "no" else ""


@when("I blend the DRBX alleles with DRB1 allele")
def step_impl(context):
    context.blended_drbx = pyard.dr_blender(
        context.drb1_slug, context.drb3, context.drb4, context.drb5
    )


@then("it should blend as {DRBX_BLEND}")
def step_impl(context, DRBX_BLEND):
    DRBX_BLEND = DRBX_BLEND if DRBX_BLEND != "nothing" else ""
    assert_that(context.blended_drbx, is_(DRBX_BLEND))


@when("I blend the DRBX alleles with DRB1 allele, it shouldn't blend")
def step_impl(context):
    pass


@then("{expected} was expected, but found {found}")
def step_impl(context, expected, found):
    assert_that(
        calling(pyard.dr_blender).with_args(
            context.drb1_slug, context.drb3, context.drb4, context.drb5
        ),
        raises(DRBXBlenderError, f"{found} where {expected} expected"),
    )
