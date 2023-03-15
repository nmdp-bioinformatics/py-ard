#
#    py-ard
#    Copyright (c) 2023 Be The Match operated by National Marrow Donor Program. All Rights Reserved.
#
#    This library is free software; you can redistribute it and/or modify it
#    under the terms of the GNU Lesser General Public License as published
#    by the Free Software Foundation; either version 3 of the License, or (at
#    your option) any later version.
#
#    This library is distributed in the hope that it will be useful, but WITHOUT
#    ANY WARRANTY; with out even the implied warranty of MERCHANTABILITY or
#    FITNESS FOR A PARTICULAR PURPOSE.  See the GNU Lesser General Public
#    License for more details.
#
#    You should have received a copy of the GNU Lesser General Public License
#    along with this library;  if not, write to the Free Software Foundation,
#    Inc., 59 Temple Place, Suite 330, Boston, MA 02111-1307  USA.
#
#    > http://www.fsf.org/licensing/licenses/lgpl.html
#    > http://www.opensource.org/licenses/lgpl-license.php
#
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
