from behave import *
from hamcrest import assert_that, is_, calling, raises

import pyard
from pyard.blender import DRBXBlenderError


@given("a subject has {drb1_slug} DRB1 SLUG")
def step_impl(context, drb1_slug):
    context.drb1_slug = drb1_slug


@given("a subject has {drb3} DRB3 allele")
def step_impl(context, drb3):
    context.drb3 = drb3 if drb3 != "no" else ""


@step("a subject has {drb4} DRB4 allele")
def step_impl(context, drb4):
    context.drb4 = drb4 if drb4 != "no" else ""


@step("a subject has {drb5} DRB5 allele")
def step_impl(context, drb5):
    context.drb5 = drb5 if drb5 != "no" else ""


@when("I blend the DRBX alleles with DRB1 allele")
def step_impl(context):
    context.blended_drbx = pyard.dr_blender(
        context.drb1_slug, context.drb3, context.drb4, context.drb5
    )


@then("it should blend as {drbx_blend}")
def step_impl(context, drbx_blend):
    drbx_blend = drbx_blend if drbx_blend != "nothing" else ""
    assert_that(context.blended_drbx, is_(drbx_blend))


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
