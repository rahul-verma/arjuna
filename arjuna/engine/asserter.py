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
