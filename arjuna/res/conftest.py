import pytest

from arjuna import *
from sltest.lib.fixture.session import *
from sltest.lib.fixture.module import *
from sltest.lib.fixture.test import *

@pytest.mark.hookwrapper
def pytest_runtest_makereport(item, call):
    result = yield
    PytestHooks.add_screenshot_for_result(item, result)