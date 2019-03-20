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


class Sample:
    pass

s1 = Sample()
s2 = Sample()


@test_function
def assert_sameness(my):
    my.steps.assert_same("Should pass for same objects", s1, s1)
    my.steps.assert_different("Should pass for different objects", s1, s2)

    # You can also use the following instead of assert_different
    my.steps.assert_not_same("Should pass for different objects", s1, s2)


@test_function
def assert_same_fails_for_different_objects(my):
    my.steps.assert_same("Should fail for different objects.", s1, s2)


@test_function
def assert_different_fails_for_same_objects(my):
    my.steps.assert_different("Should fail for same objects.", s1, s1)


@test_function
def assert_same_errs_for_incompatible_values(my):
    my.steps.assert_same("Should err for int and string comparison", s1, 1)


@test_function
def assert_different_errs_for_incompatible_values(my):
    my.steps.assert_different("Should err for int and string comparison", s1, 1)





