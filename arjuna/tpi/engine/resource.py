# This file is a part of Arjuna
# Copyright 2015-2021 Rahul Verma

# Website: www.RahulVerma.net

# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at

#   http://www.apache.org/licenses/LICENSE-2.0

# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

'''
Arjuna Test Resources

The test resources markup provided by Arjuna includes easy-to-use decorators which wrap **pytest.fixture** decorator.

Note:
    For using any of the decorators in this module, the resource function must have the signature as **f(request)** with **request** as the first argument.
'''

import pytest
import itertools
import functools

from .test import My
from typing import Callable


def _simple_dec(func):
    @functools.wraps(func)
    def call_func(request, *args, **kwargs):
        from arjuna import log_info
        request_wrapper = My()
        request_wrapper.set_req_obj(request)
        request_wrapper.data = hasattr(request, "param") and request.param or None
        qual_name = request_wrapper.info.get_qual_name_with_data()
        if func.__name__ != 'group':
            log_info("(Setup) Begin fixture function: {}".format(qual_name))   
        yield from func(request_wrapper, *args, **kwargs)
        if func.__name__ != 'group':
            log_info("(Teardown) End fixture function: {}".format(qual_name))
        
    return call_func

def _repr_record(record):
    return str(record)

def __pytestfix(scope, drive_with=None, default=False):
    records = None
    ids = None
    if drive_with:
        records = drive_with.build("Fixture").all_records
        ids = [_repr_record(record) for record in records]

    def wrapper(func):
        orig_func = func
        if drive_with:
            return pytest.fixture(scope=scope, params=records, ids=ids, autouse=default)(_simple_dec(func))
        else:
            return pytest.fixture(scope=scope, autouse=default)(_simple_dec(func))
    return wrapper


def for_group(func: Callable=None, *, drive_with: 'DataSource'=None, default: bool=False) -> Callable:
    '''
        Decorator for session level test resource.

        Wraps **pytest.fixture** to create a fixture with scope=session and provides an Arjuna's decorated version of the function that is marked with **for_group** decorator.

        Args:
            func: A Function with signature **f(request)**. The name request is mandatory and enforced.

        Keyword Arguments:
            drive_with: (Optional) Used for data driven testing. Argument can be Arjuna Data Source.

                .. code-block:: python
                
                    @for_group(drive_with=<DS>)
                    def fix(request, data):
                        pass

            default: Should it be auto-applied?
    '''
    from arjuna import Arjuna

    if func is not None:
        return pytest.fixture(scope="session", autouse=default)(_simple_dec(func))
    else:
        return __pytestfix("session", drive_with=drive_with, default=default)


def for_module(func: Callable=None, *, drive_with: 'DataSource'=None, default: bool=False) -> Callable:
    '''
        Decorator for module level test fixture/resource.

        Wraps **pytest.fixture** to create a fixture with scope=module and provides an Arjuna's decorated version of the function that is marked with **for_module** decorator.

        Args:
            func: A Function with signature **f(request)**. The name request is mandatory and enforced.

        Keyword Arguments:
            drive_with: (Optional) Used for data driven testing. Argument can be Arjuna Data Source.

                .. code-block:: python
                
                    @for_module(drive_with=<DS>)
                    def fix(request, data):
                        pass

            default: Should it be auto-applied?
    '''
    from arjuna import Arjuna

    if func is not None:
        return pytest.fixture(scope="module", autouse=default)(_simple_dec(func))
    else:
        return __pytestfix("module", drive_with=drive_with, default=default)


def for_test(func: Callable=None, *, drive_with: 'DataSource'=None, default: bool=False) -> Callable:
    '''
        Decorator for test function level test fixture/resource.

        Wraps **pytest.fixture** to create a fixture with scope=function and provides an Arjuna's decorated version of the function that is marked with **for_test** decorator.

        Args:
            func: A Function with signature **f(request)**. The name request is mandatory and enforced.

        Keyword Arguments:
            drive_with: (Optional) Used for data driven testing. Argument can be Arjuna Data Source.

                .. code-block:: python
                
                    @for_test(drive_with=<DS>)
                    def fix(request):
                        pass

            default: Should it be auto-applied?
    '''
    from arjuna import Arjuna

    if func is not None:
        return pytest.fixture(scope="function", autouse=default)(_simple_dec(func))
    else:
        return __pytestfix("function", drive_with=drive_with, default=default)


@for_group(default=True)
def group(request):
    getattr(request.raw_request, "session").group_info = request.raw_request.param
    yield

@for_test(default=True)
def test_resources(request):
    from arjuna import Arjuna
    thread_container = Arjuna.get_report_metadata()
    set_node_id = thread_container.current_test_node_id  
    thread_container.current_test_node_id = request.raw_request.node.nodeid
    getattr(request.raw_request, "function").report_metadata = thread_container
    yield
    try:
        network_recorder = request.space.network_recorder
        network_recorder.register()
    except:
        pass
    thread_container.clear()