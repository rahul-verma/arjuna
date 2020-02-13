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
        self._asserter = unittest.TestCase('__init__')

    def assert_equal(self, actual, expected, context, msg=None):
        msg = msg and " {}".format(msg) or ""
        self._asserter.assertEqual(actual, expected, "{} has unexpected value. {}".format(context, msg))

