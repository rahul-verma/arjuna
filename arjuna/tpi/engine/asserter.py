# This file is a part of Arjuna
# Copyright 2015-2020 Rahul Verma

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


import unittest

class AsserterMixIn:

    def __init__(self):
        # Trick to use assertions outside of a unittest test
        self.__asserter = Asserter()

    @property
    def asserter(self):
        return self.__asserter

class Asserter:

    def __init__(self):
        self.__asserter = unittest.TestCase('__init__')

    @classmethod
    def format_msg(cls, msg):
        return msg and " {}.".format(msg) or ""

    def assert_equal(self, actual, expected, msg):
        self.__asserter.assertEqual(actual, expected, msg)

    def assert_lesser(self, left, right, msg):
        self.__asserter.assertLess(left, right, msg)

    def assert_greater(self, left, right, msg):
        self.__asserter.assertGreater(left, right, msg)

    def assert_min(self, left, right, msg):
        self.__asserter.assertGreaterEqual(left, right, msg)

    def assert_max(self, left, right, msg):
        self.__asserter.assertLessEqual(left, right, msg)

    def assert_not_equal(self, left, right, msg):
        self.__asserter.assertNotEqual(actual, expected, msg)

    def assert_true(self, actual, msg):
        self.__asserter.assertTrue(actual, msg)

    def assert_false(self, actual, msg):
        self.__asserter.assertFalse(actual, msg)

    def fail(self, msg):
        self.__asserter.fail(msg)
