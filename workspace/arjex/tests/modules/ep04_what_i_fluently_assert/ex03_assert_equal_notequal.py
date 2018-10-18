'''
This file is a part of Test Mile Arjuna
Copyright 2018 Test Mile Software Testing Pvt Ltd

Website: www.TestMile.com
Email: support [at] testmile.com
Creator: Rahul Verma

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

  http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
'''

from arjuna.tpi.markup import *
from arjuna.tpi.markup_helpers import *

'''
Explore more situations for this.
'''

@test_function
def assert_equality(my):
    validator = my.steps.validate("Higher purpose")

    #Integers
    validator.assert_that(1).is_equal_to(1)
    validator.assert_that(1).is_not_equal_to(2)

    #Strings
    validator.assert_that("testing").is_equal_to("testing")
    validator.assert_that("testing").is_not_equal_to("easy")

    # booleans -> Not suggested. Should use assert_true/assert_false instead
    validator.assert_that(True).is_equal_to(True)
    validator.assert_that(True).is_not_equal_to(False)

@test_function
def assert_equal_fails_for_unequal_ints(my):
    my.steps.validate("Objects should be equal").assert_that(1).is_equal_to(2)


@test_function
def assert_notequal_fails_for_equal_ints(my):
    my.steps.validate("Objects should not be equal").assert_that(1).is_not_equal_to(1)

@test_function
def assert_equal_fails_for_unequal_strings(my):
    my.steps.validate("Objects should be equal").assert_that("testing").is_equal_to("easy")


@test_function
def assert_notequal_fails_for_equal_strings(my):
    my.steps.validate("Objects should not be equal").assert_that("testing").is_not_equal_to("testing")

@test_function
def assert_equal_fails_for_unequal_booleans(my):
    my.steps.validate("Objects should be equal").assert_that(True).is_equal_to(False)


@test_function
def assert_notequal_fails_for_equal_booleans(my):
    my.steps.validate("Objects should not be equal").assert_that(True).is_not_equal_to(True)


@test_function
def assert_equal_errs_for_incompatible_values(my):
    my.steps.validate("Objects should of same type.").assert_that(True).is_equal_to("testing")


@test_function
def assert_unequal_errs_for_incompatible_values(my):
    my.steps.validate("Objects should of same type.").assert_that(True).is_not_equal_to("testing")


@test_function
def assert_equal_with_expected_value_as_none(my):
    my.steps.validate("Objects None not comapred for type.").assert_that(None).is_equal_to(1)

@test_function
def assert_notequal_with_expected_value_as_none(my):
    my.steps.validate("Two Nones are equal").assert_that(None).is_equal_to(None)