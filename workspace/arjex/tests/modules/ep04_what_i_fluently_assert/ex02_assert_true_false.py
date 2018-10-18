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


@test_function
def assert_truth(my):
    my.steps.validate("Truth Check").assert_that(True).is_true()
    my.steps.validate("Truth Check").assert_that(False).is_false()

    # Using Fluent assertions allows you create a multi-asserter object with a single purpose
    # This is a better way when for the same business context, you need to execute multiple assertions
    # In subsequent examples, when multiple asserts exist, we'll use the following construct
    validator = my.steps.validate("Higher purpose")
    validator.assert_that(True).is_true()
    validator.assert_that(False).is_false()


@test_function
def assert_true_fail_for_false(my):
    my.steps.validate("Truth Check").assert_that(False).is_true()

@test_function
def assert_false_fail_for_true(my):
    my.steps.validate("Truth Check").assert_that(True).is_false()

@test_function
def assert_true_non_boolean_raises_exception(my):
    my.steps.validate("Truth Check").assert_that("testing").is_true()

@test_function
def assert_false_non_boolean_raises_exception(my):
    my.steps.validate("Truth Check").assert_that("testing").is_false()

@test_function
def assert_true_errs_for_none(my):
    my.steps.validate("Truth Check").assert_that(None).is_true()

@test_function
def assert_false_errs_for_none(my):
    my.steps.validate("Truth Check").assert_that(None).is_false()