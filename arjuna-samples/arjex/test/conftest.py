import pytest
import sys

from arjuna import *
sys.path.append(C("project.root.dir") + "/..")

from arjex.lib.fixture.group import *
from arjex.lib.fixture.module import *
from arjex.lib.fixture.test import *

@pytest.mark.hookwrapper
def pytest_runtest_makereport(item, call):
    result = yield
    PytestHooks.add_screenshot_for_result(item, result)

def pytest_generate_tests(metafunc):
    PytestHooks.configure_group_for_test(metafunc)

def pytest_collection_modifyitems(items, config):
    PytestHooks.select_tests(items, config)