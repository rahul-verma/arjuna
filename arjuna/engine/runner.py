import unittest

class TestRunner:
    import sys
    import os
    import unittest
    
    def __init__(self):
        from arjuna import Arjuna
        from arjuna.core.enums import ArjunaOption
        self.__project_dir = Arjuna.get_ref_config().get_arjuna_option_value(ArjunaOption.PROJECT_ROOT_DIR).as_str()
        self.__tests_dir = Arjuna.get_ref_config().get_arjuna_option_value(ArjunaOption.PROJECT_TESTS_DIR).as_str()
        self.__suite = unittest.TestSuite()

    @property
    def tests_dir(self):
        return self.__tests_dir

    @property
    def test_suite(self):
        return self.__suite
    
    def load_all_tests(self):
        test_loader = unittest.TestLoader()
        suite = test_loader.discover(self.tests_dir)
        self.test_suite.addTest(suite)
        # from tests import fleet
        # suite.addTest(loader.loadTestsFromModule(fleet))
    
    def run(self):
        runner = unittest.TextTestRunner(verbosity=3)
        runner.run(self.test_suite)