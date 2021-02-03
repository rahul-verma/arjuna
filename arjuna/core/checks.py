# This file is a part of Arjuna
# Copyright 2015-2021 Rahul Verma

# Website: www.RahulVerma.net

# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at

#   http://www.apache.org/licenses/LICENSE-2.0

# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import re

def is_true(input):
    if type(input) is not bool:
        raise Exception("Not a boolean")
    return input is True


def is_false(input):
    if type(input) is not bool:
        raise Exception("Not a boolean")
    return input is False

def throw_exception_for_incompt_equal_same(context, actual, expected):
    if actual is None or expected is None:
        return

    if type(actual) != type(expected):
        msg = 'Checking for {} objects does not work for objects of different types.'.format(context)
        raise Exception(msg)

def are_equal(actual, expected):
    throw_exception_for_incompt_equal_same("equal/non-equal", actual, expected)
    return expected == actual

def are_not_equal(actual, expected):
    throw_exception_for_incompt_equal_same("equal/non-equal", actual, expected)
    return not are_equal(actual, expected)

def are_almost_equal(actual, expected, delta):
    diff = abs(expected - actual)
    delta2 = abs(delta)
    return diff <= delta2


def are_same(actual, expected):
    throw_exception_for_incompt_equal_same("same/different", actual, expected)
    return expected is actual


def are_different(actual, expected):
    throw_exception_for_incompt_equal_same("same/different", actual, expected)
    return expected is not actual

def match(target, pattern):
    if target is None: return False
    if re.match('^' + pattern + '$', target):
        return True
    else:
        return False

def partially_match(target, pattern):
    if target is None: return False
    if re.search(pattern, target):
        return True
    else:
        return False

def match_with_ignore_case(target, pattern):
    if target is None: return False
    if re.match('^' + pattern + '$', target, re.IGNORECASE):
        return True
    else:
        return False

def does_not_match_with_ignore_case(target, pattern):
    if target is None: return True
    if re.match('^' + pattern + '$', target, re.IGNORECASE):
        return False
    else:
        return True

def partially_match_with_ignore_case(target, pattern):
    if target is None: return False
    if re.search(pattern, target, re.IGNORECASE) is not None:
        return True
    else:
        return False

def does_not_partially_match_with_ignore_case(target, pattern):
    if target is None: return True
    if re.search(pattern, target, re.IGNORECASE) is not None:
        return False
    else:
        return True

are_not_same = are_different

def is_none(obj):
    return obj is None


def is_not_none(obj):
    return obj is not None


def contains(parent, child):
    return child in parent

def is_subset(left, right):
    return left.issubset(right)

def has_intersection(left, right):
    return bool(left.intersection(right))

def has_no_intersection(left, right):
    return bool(not left.intersection(right))

def does_not_contain(parent, child):
    return child not in parent

numbers = {int, float}

def __validate_args_as_numbers(func, left, right):
    if type(left) not in numbers or type(right) not in numbers:
        raise Exception("{} relation check is allowed only for numbers. Received >>{}<< of type: {} and >>{}<< of type {}.".format(
            func,
            left,
            type(left),
            right,
            type(right)
        ))


def less_than(left, right):
    return left < right

def less_or_equal(left, right):
    return left <= right

def greater_than(left, right):
    return left > right

def greater_or_equal(left, right):
    return left >= right
