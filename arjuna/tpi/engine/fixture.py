# This file is a part of Arjuna
# Copyright 2015-2020 Rahul Verma

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
Arjuna Test Fixtures

The test fixtures provided by Arjuna are easy to use decorators which wrap `pytest.fixture` decorator.

Note:
    For using any of the decorators in this module, the fixture function must have the signature as `f(request)` with `request` as the first argument.
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
        log_info("(Setup) Begin fixture function: {}".format(qual_name))   
        yield from func(request_wrapper, *args, **kwargs)
        log_info("(Teardown) End fixture function: {}".format(qual_name))
        
    return call_func

def _repr_record(record):
    return str(record)

def __pytestfix(scope, drive_with=None):
    records = None
    ids = None
    if drive_with:
        records = drive_with.build("Fixture").all_records
        ids = [_repr_record(record) for record in records]

    def wrapper(func):
        orig_func = func

        # @functools.wraps(orig_func)
        # def wrapper_without_data(request, *args, **kwargs):
        #     request.handler = request
        #     yield from _call_func(func, request, *args, **kwargs)

        # @functools.wraps(orig_func)
        # def wrapper_with_data(request, data, *args, **kwargs):
        #     my.handler = request
        #     yield from _call_func(func, request, data=(params, ids), *args, **kwargs)

        # else:
        #     my = My()
        #     my.data = DummyDataRecord()
        #     func = pytest.mark.parametrize('my', [my], ids=My.repr)(func) 

        if drive_with:
            return pytest.fixture(scope=scope, params=records, ids=ids)(_simple_dec(func))
        else:
            return pytest.fixture(scope=scope)(_simple_dec(func))
    return wrapper

def for_group(func: Callable=None, *, drive_with: 'DataSource'=None) -> Callable:
    '''
        Decorator for session level test fixture/resource.

        Wraps `pytest.fixture` to create a fixture with scope=session and provides an Arjuna's decorated version of the function that is marked with `for_group` decorator.

        Args:
            func: A Function with signature `f(request)`. The name request is mandatory and enforced.

        Keyword Arguments:
            drive_with: (Optional) Used for data driven testing. Argument can be Arjuna Data Source.

                .. code-block:: python
                
                    @test(drive_with=<DS>)
                    def check_sample(request, data):
                        pass
    '''
    from arjuna import Arjuna

    if func is not None:
        return pytest.fixture(scope="session")(_simple_dec(func))
    else:
        return __pytestfix("session", drive_with=drive_with)


def for_module(func: Callable=None, *, drive_with: 'DataSource'=None) -> Callable:
    '''
        Decorator for module level test fixture/resource.

        Wraps `pytest.fixture` to create a fixture with scope=module and provides an Arjuna's decorated version of the function that is marked with `for_module` decorator.

        Args:
            func: Function

        Keyword Arguments:
            drive_with: (Optional) Used for data driven testing. Argument can be Arjuna Data Source.

                .. code-block:: python
                
                    @test(drive_with=<DS>)
                    def check_sample(request, data):
                        pass
    '''
    from arjuna import Arjuna

    if func is not None:
        return pytest.fixture(scope="module")(_simple_dec(func))
    else:
        return __pytestfix("module", drive_with=drive_with)


def for_test(func: Callable=None, *, drive_with: 'DataSource'=None) -> Callable:
    '''
        Decorator for test function level test fixture/resource.

        Wraps `pytest.fixture` to create a fixture with scope=function and provides an Arjuna's decorated version of the function that is marked with `for_test` decorator.

        Args:
            func: A Function with signature `f(request)`. The name request is mandatory and enforced.

        Keyword Arguments:
            drive_with: (Optional) Used for data driven testing. Argument can be Arjuna Data Source.

                .. code-block:: python
                
                    @test(drive_with=<DS>)
                    def check_sample(request, data):
                        pass
    '''
    from arjuna import Arjuna

    if func is not None:
        return pytest.fixture(scope="function")(_simple_dec(func))
    else:
        return __pytestfix("function", drive_with=drive_with)

@for_group
def group(request):
    yield request.data
