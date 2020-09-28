import pytest

from arjuna.engine.pytest import PytestHooks


def get_import_lenient_set(context):
    return set(["arjex_minimal.lib", "arjex_minimal.lib.resource", f"arjex_minimal.lib.resource." + context])

try:
    from arjex_minimal.lib.resource.group import *
except ModuleNotFoundError as e:
    print("Found")
    if e.name not in get_import_lenient_set("group"):
        raise Exception(e.name)

try:
    from arjex_minimal.lib.resource.module import *
except ModuleNotFoundError as e:
    if e.name not in get_import_lenient_set("module"):
        raise Exception(e.name)

try:
    from arjex_minimal.lib.resource.test import *
except ModuleNotFoundError as e:
    if e.name not in get_import_lenient_set("test"):
        raise Exception(e.name)


@pytest.mark.hookwrapper
def pytest_runtest_makereport(item, call):
    result = yield
    PytestHooks.prepare_result(result)
    PytestHooks.enhance_reports(item, result)


def pytest_generate_tests(metafunc):
    PytestHooks.configure_group_for_test(metafunc)


def pytest_collection_modifyitems(items, config):
    PytestHooks.select_tests(items, config)


def pytest_html_results_summary(prefix, summary, postfix):
    PytestHooks.inject_arjuna_js(prefix)