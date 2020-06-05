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

class Asserter:
    '''
        Arjuna's asserter class.

        It can be used directly. It is already included as an attribute for request fixture in test functions and all Guis and Gui Templates.
    '''

    def __init__(self):
        self.__asserter = unittest.TestCase('__init__')

    @classmethod
    def _format_msg(cls, msg):
        return msg and " {}.".format(msg) or ""

    def assert_equal(self, obj1, obj2, msg):
        '''
            Assert obj1 == obj2

            Wrapper on unittest's assertEqual

            Args:
                obj1: Object of any type which supports == operator for obj2 type
                obj2: Object meeting the above constraint
                msg: A context string explaining why this assertion was done.
        '''
        self.__asserter.assertEqual(obj1, obj2, msg)

    def assert_lesser(self, obj1, obj2, msg):
        '''
            Assert obj1 < obj2

            Wrapper on unittest's assertLess

            Args:
                obj1: Object of any type which supports < operator for obj2 type
                obj2: Object meeting the above constraint
                msg: A context string explaining why this assertion was done.
        '''
        self.__asserter.assertLess(obj1, obj2, msg)

    def assert_greater(self, obj1, obj2, msg):
        '''
            Assert obj1 > obj2

            Wrapper on unittest's assertLess

            Args:
                obj1: Object of any type which supports > operator for obj2 type
                obj2: Object meeting the above constraint
                msg: A context string explaining why this assertion was done.
        '''
        self.__asserter.assertGreater(obj1, obj2, msg)

    def assert_min(self, obj, min_value, msg):
        '''
            Asserts a minimum value for an object i.e. obj >= min_value

            Wrapper on unittest's assertGreaterEqual

            Args:
                obj: Object of any type which supports >= operator for min_value
                min_value: Object meeting the above constraint
                msg: A context string explaining why this assertion was done.
        '''
        self.__asserter.assertGreaterEqual(obj, min_value, msg)

    def assert_max(self, obj, max_value, msg):
        '''
            Asserts a maximum value for an object i.e. obj <= max_value

            Wrapper on unittest's assertLessEqual

            Args:
                obj: Object of any type which supports <= operator for min_value
                max_value: Object meeting the above constraint
                msg: A context string explaining why this assertion was done.
        '''
        self.__asserter.assertLessEqual(obj, max_value, msg)

    def assert_not_equal(self, obj1, obj2, msg):
        '''
            Assert obj1 != obj2

            Wrapper on unittest's assertNotEqual

            Args:
                obj1: Object of any type which supports != operator for obj2 type
                obj2: Object meeting the above constraint
                msg: A context string explaining why this assertion was done.
        '''
        self.__asserter.assertNotEqual(obj1, obj2, msg)

    def assert_true(self, obj, msg):
        '''
            Assert obj is True.

            Wrapper on unittest's assertTrue

            Args:
                obj: Object of any type
                msg: A context string explaining why this assertion was done.
        '''
        self.__asserter.assertTrue(obj, msg)

    def assert_false(self, obj, msg):
        '''
            Assert obj is False.

            Wrapper on unittest's assertFalse

            Args:
                obj: Object of any type
                msg: A context string explaining why this assertion was done.
        '''
        self.__asserter.assertFalse(obj, msg)

    def fail(self, msg):
        '''
            Raises AssertionError with the provided message.

            Args:
                msg: A context string explaining the failure.
        '''
        self.__asserter.fail(msg)


class AsserterMixIn:
    '''
        Base class to add **asserter** property to any class which inherits from it.
    '''

    def __init__(self):
        # Trick to use assertions outside of a unittest test
        self.__asserter = Asserter()

    @property
    def asserter(self) -> Asserter:
        '''
            Arjuna's Asserter object for executing assertions.
        '''
        return self.__asserter

class IterableAsserterMixin:

    '''
        Base class for adding assertions to iterables.

        Note:
            Use it in combination with AsserterMixIn.
            The child class should have `_container` as its attribute or property.
    '''

    def __init__(self):
        self.__klass_name = self.__class__.__name__

    def __len__(self):
        return len(self._container)

    def is_empty(self):
        '''
            Returns True if this iterable has no objects.
        '''
        return len(self) == 0

    def assert_empty(self, *, msg):
        '''
            Assert that there should not be any object in this iterable.

            Keyword Arguments:
                msg: Purpose of this assertion.
        '''
        if not self.is_empty():
            raise AssertionError("{} is not empty. Length: {}. {}".format(self.__klass_name, len(self), msg))

    def assert_not_empty(self, *, msg):
        '''
            Assert that there should be atleast one object in this iterable.

            Keyword Arguments:
                msg: Purpose of this assertion.
        '''
        if self.is_empty():
            raise AssertionError(f"{self.__klass_name} is empty. {msg}")

    def assert_size(self, size, *, msg):
        '''
            Assert that the number of objects in this iterable should match provided size.

            Arguments:
                size: Expected number of objects.
            
            Keyword Arguments:
                msg: Purpose of this assertion.
        '''
        length = len(self)
        if length != size:
            raise AssertionError(f"{self.__klass_name} is not of expected size. Expected: {size}. Actual: {length}. {msg}")

    def assert_min_size(self, size, *, msg):
        '''
            Assert that the number of objects in this iterable >= provided size.

            Arguments:
                size: Expected minimum number of objects.
            
            Keyword Arguments:
                msg: Purpose of this assertion.
        '''
        length = len(self)
        if length < size:
            raise AssertionError(f"{self.__klass_name} is not of minimum expected size. Expected minimum size is {size}. Actual: {length}. {msg}")

    def assert_max_size(self, size, *, msg):
        '''
            Assert that the number of objects in this iterable <= provided size.

            Arguments:
                size: Expected maximum number of objects.
            
            Keyword Arguments:
                msg: Purpose of this assertion.
        '''
        if size <0 :
            raise TypeError("Negative number aren't allowed")
        length = len(self)
        if length > size:
            raise AssertionError(f"{self.__klass_name} is not of maximum expected size. Expected maximum size is {size}. Actual: {length}. {msg}")

    def assert_size_range(self, min_size, max_size, *, msg):
        '''
            Assert that the number of objects in this iterable should be in the provided size range.

            Arguments:
                min_size: Expected minimum number of objects.
                max_size: Expected maximum number of objects.
            
            Keyword Arguments:
                msg: Purpose of this assertion.
        '''
        length = len(self)
        if length < min_size or length > max_size:
            raise AssertionError(f"{self.__klass_name} is not in expected size range. Expected maximum size is {size}. Actual: {length}. {msg}")




