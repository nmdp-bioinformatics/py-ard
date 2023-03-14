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
from hamcrest import assert_that, is_

from pyard.drbx import map_drbx


@given("a subject has {arg0} and {arg1} DRB3 alleles")
def step_impl(context, arg0, arg1):
    context.drb3_1 = "" if arg0 == "x" else arg0
    context.drb3_2 = "" if arg1 == "x" else arg1


@step("a subject has {arg0} and {arg1} DRB4 alleles")
def step_impl(context, arg0, arg1):
    context.drb4_1 = "" if arg0 == "x" else arg0
    context.drb4_2 = "" if arg1 == "x" else arg1


@step("a subject has {arg0} and {arg1} DRB5 alleles")
def step_impl(context, arg0, arg1):
    context.drb5_1 = "" if arg0 == "x" else arg0
    context.drb5_2 = "" if arg1 == "x" else arg1


@when("I create a DRBX genotype")
def step_impl(context):
    drbs = [
        context.drb3_1,
        context.drb3_2,
        context.drb4_1,
        context.drb4_2,
        context.drb5_1,
        context.drb5_2,
    ]
    context.drbx = map_drbx(drbs, True)


@then("it should be {drbx1} and {drbx2}")
def step_impl(context, drbx1, drbx2):
    expected_drbx_1 = "" if drbx1 == "x" else drbx1
    expected_drbx_2 = "" if drbx2 == "x" else drbx2
    expected_drbx = (expected_drbx_1, expected_drbx_2)
    assert_that(context.drbx, is_(expected_drbx))
