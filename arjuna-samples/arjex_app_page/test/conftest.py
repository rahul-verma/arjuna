import pytest

from arjuna import *
from arjex_app_page.lib.fixture.session import *
from arjex_app_page.lib.fixture.module import *
from arjex_app_page.lib.fixture.test import *

@pytest.mark.hookwrapper
def pytest_runtest_makereport(item, call):
    result = yield
    PytestHooks.add_screenshot_for_result(item, result)