import unittest

class AsserterMixIn:

    def __init__(self):
        # Trick to use assertions outside of a unittest test
        self._asserter = unittest.TestCase('__init__')