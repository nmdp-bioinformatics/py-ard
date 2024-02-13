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

import pyard


@given("the broad allele/serology is {broad}")
def step_impl(context, broad):
    context.broad = broad


@when("it is expanded to the splits")
def step_impl(context):
    mapping = context.ard.find_broad_splits(context.broad)
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
    mapping = context.ard.find_broad_splits(context.split)
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


@given("the serology antigen is {serology}")
def step_impl(context, serology):
    context.serology = serology


@when("looking for associated serology")
def step_impl(context):
    context.associated_antigen = context.ard.find_associated_antigen(context.serology)


@then("the associated serology is found to be {associated_antigen}")
def step_impl(context, associated_antigen):
    assert_that(context.associated_antigen, is_(associated_antigen))
