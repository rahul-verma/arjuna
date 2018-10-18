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
    my.steps.assert_true("Should Pass for True value.", True)
    my.steps.assert_false("Should Pass for False value.", False)


@test_function
def assert_truth_fail_for_true(my):
    my.steps.assert_true("Should Fail for False value.", False)


@test_function
def assert_truth_fail_for_false(my):
    my.steps.assert_false("Should Fail for True value.", True)


@test_function
def assert_truth_non_boolean_raises_exception(my):
    my.steps.assert_true("Should throw error for non-boolean value", 1)


@test_function
def assert_true_errs_for_None_value(my):
    my.steps.assert_true("Should throw error for non-boolean value.", None)


@test_function
def assert_false_errs_for_None_value(my):
    my.steps.assert_false("Should throw error for non-boolean value.", None)