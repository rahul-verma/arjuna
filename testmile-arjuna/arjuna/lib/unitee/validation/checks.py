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

def is_true(input):
    if type(input) is not bool:
        raise Exception("Not a boolean")
    return input is True


def is_false(input):
    if type(input) is not bool:
        raise Exception("Not a boolean")
    return input is False

def __throw_exception_for_incompt_equal_same(context, actual, expected):
    if type(actual) != type(expected):
        msg = 'Checking for {} objects does not work for objects of different types.'.format(context)
        raise Exception(msg)

def is_equal(actual, expected):
    __throw_exception_for_incompt_equal_same("equal/non-equal", actual, expected)
    return expected == actual

def is_not_equal(actual, expected):
    __throw_exception_for_incompt_equal_same("equal/non-equal", actual, expected)
    return not is_equal(actual, expected)

def is_almost_equal(actual, expected, delta):
    diff = abs(expected - actual)
    delta2 = abs(delta)
    return diff <= delta2


def is_same(actual, expected):
    __throw_exception_for_incompt_equal_same("same/different", actual, expected)
    return expected is actual


def is_different(actual, expected):
    __throw_exception_for_incompt_equal_same("same/different", actual, expected)
    return expected is not actual


is_not_same = is_different

def is_none(obj):
    return obj is None


def is_not_none(obj):
    return obj is not None


def contains(parent, child):
    return child in parent

def does_not_contain(parent, child):
    return child not in parent
