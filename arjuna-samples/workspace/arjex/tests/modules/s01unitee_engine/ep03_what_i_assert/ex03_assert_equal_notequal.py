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
    # Integers
    my.steps.assert_equal("Business purpose", 1, 1)
    my.steps.assert_not_equal("Business purpose", 1, 2)

    # Strings
    my.steps.assert_equal("Business purpose", "testing", "testing")
    my.steps.assert_not_equal("Business purpose", "testing", "easy")

    # booleans -> Not suggested. Should use assert_true/assert_false instead
    my.steps.assert_equal("Business purpose", True, True)
    my.steps.assert_not_equal("Business purpose", True, False)


@test_function
def assert_equal_fails_for_nonequal_ints(my):
    my.steps.assert_equal("Should fail for Non equal ints", 1, 2)


@test_function
def assert_notequal_fails_for_equal_ints(my):
    my.steps.assert_not_equal("Should fail for equal ints", 1, 1)


@test_function
def assert_equal_fails_for_nonequal_strings(my):
    my.steps.assert_equal("Should fail for Non equal strings", "testing", "easy ")


@test_function
def assert_notequal_fails_for_equal_strings(my):
    my.steps.assert_not_equal("Should fail for equal strings", "testing", "testing")


@test_function
def assert_equal_fails_for_nonequal_booleans(my):
    my.steps.assert_equal("Should fail for Non equal booleans", True, False)


@test_function
def assert_notequal_fails_for_equal_booleans(my):
    my.steps.assert_not_equal("Should fail for equal booleans", False, False)


@test_function
def assert_equal_errs_for_incompatible_values(my):
    my.steps.assert_equal("Should err for int and string comparison", 1, "testing")


@test_function
def assert_notequal_errs_for_incompatible_values(my):
    my.steps.assert_not_equal("Should err for int and string comparison", 1, "testing")


@test_function
def assert_equal_with_expected_value_as_none(my):
    my.steps.assert_equal("Should fail.", None, 1)


@test_function
def assert_notequal_with_expected_value_as_none(my):
    my.steps.assert_equal("Should pass", None, None)