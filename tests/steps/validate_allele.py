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
from behave import when, then
from hamcrest import assert_that, is_


@when("checking if the allele is valid in strict mode")
def step_impl(context):
    context.is_valid_allele = context.ard.is_valid_allele(context.allele)


@when("checking if the allele is valid in non-strict mode")
def step_impl(context):
    context.is_valid_allele = context.ard_non_strict.is_valid_allele(context.allele)


@then("the allele validity is {validity}")
def step_impl(context, validity):
    expected = validity == "Valid"
    assert_that(context.is_valid_allele, is_(expected))
