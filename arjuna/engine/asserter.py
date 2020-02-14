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

    def __msg(self, msg):
        return msg and " {}".format(msg) or ""

    def __equality_msg(self, context, msg, expected, relation=""):
        if relation:
            relation = relation + " "
        return "{} was {}expected to be {}".format(context, relation, expected, self.__msg(msg))

    def __format_bool_msg(self, context, msg, expected):
        return "{} was expected to be {}.{}".format(context, expected, self.__msg(msg))

    def assert_equal(self, actual, expected, context, msg=None):
        self.__asserter.assertEqual(actual, expected, self.__equality_msg(context, msg, expected))

    def assert_not_equal(self, actual, expected, context, msg=None):
        self.__asserter.assertNotEqual(actual, expected, self.__equality_msg(context, msg, expected, "NOT"))

    def assert_true(self, actual, context, msg=None):
        self.__asserter.assertTrue(actual, self.__format_bool_msg(context, msg, True))

    def assert_false(self, actual, context, msg=None):
        self.__asserter.assertFalse(actual, self.__format_bool_msg(context, msg, False))

    def fail(self, msg):
        self.__asserter.fail(msg)
