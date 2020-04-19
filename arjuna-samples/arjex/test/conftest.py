import pytest

from arjuna import *
from arjex.lib.fixture.session import *
from arjex.lib.fixture.module import *
from arjex.lib.fixture.test import *

@pytest.mark.hookwrapper
def pytest_runtest_makereport(item, call):
    result = yield
    PytestHooks.add_screenshot_for_result(item, result)

def pytest_generate_tests(metafunc):
    PytestHooks.dist(metafunc)