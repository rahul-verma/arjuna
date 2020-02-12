import pytest
import datetime

import os

# from arjuna import PytestHooks
#
# @pytest.mark.hookwrapper
# def pytest_runtest_makereport(item, call):
#     result = yield
#     app = PytestHooks.get_request_attr(item, 'app')
#     html_plugin = PytestHooks.get_html_report_plugin(item)
#     PytestHooks.add_screenshot_for_failed_result(html_plugin, result, screenshoter=app)
