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
    from arjuna import Arjuna
    from arjuna.tpi.engine.data.markup import record

    if hasattr(metafunc.function, '_delegate') and metafunc.function._delegate is True:
        delegated_fix_names = [f for f in metafunc.fixturenames if f not in {'request', 'data'}]
        run_configs = Arjuna.get_run_configs()
        ids = ["RunConfig: {} ".format(c.name) for c in run_configs]

        if len(delegated_fix_names) == 1:
            argvalues = [record(run_config=c).build().all_records[0] for c in run_configs]
            try:
                metafunc.parametrize(",".join(delegated_fix_names), argvalues=argvalues, ids=ids, indirect=True)
            except ValueError as e:
                raise Exception("Exception in delegation logic. Most likely you have an already parameterized fixture. You can not use a data driven fixture in an auto-delegated test. Test Function: {}.".format(metafunc.function))

        else:
            argvalues = []
            for c in run_configs:
                argvalues.append([record(run_config=c).build().all_records[0] for i in delegated_fix_names])
            try:
                metafunc.parametrize(",".join(delegated_fix_names), argvalues=argvalues, ids=ids, indirect=True)
            except ValueError as e:
                raise Exception("Exception in delegation logic. Most likely you have an already parameterized fixture. You can not use a data driven fixture in an auto-delegated test. Test Function: {}.".format(metafunc.function))
        # import sys
        # sys.exit(1)
        # metafunc.parametrize('config', Arjuna.get_run_configs())