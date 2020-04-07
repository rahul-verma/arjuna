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
        from arjuna import Arjuna
        request_wrapper = My()
        request_wrapper.set_req_obj(request)
        qual_name = request_wrapper.info.get_qual_name_with_data()
        Arjuna.get_logger().info("(Setup) Begin fixture function: {}".format(qual_name))   
        yield from func(request_wrapper, *args, **kwargs)
        Arjuna.get_logger().info("(Teardown) End fixture function: {}".format(qual_name))
    return call_func

def for_session(func: Callable) -> Callable:
    '''
        Decorator for session level test fixture/resource.

        Wraps `pytest.fixture` to create a fixture with scope=session and provides an Arjuna's decorated version of the function that is marked with `for_session` decorator.

        Args:
            func: A Function with signature `f(request)`. The name request is mandatory and enforced.
    '''
    from arjuna import Arjuna
    return pytest.fixture(scope="session")(_simple_dec(func))

def for_module(func: Callable) -> Callable:
    '''
        Decorator for module level test fixture/resource.

        Wraps `pytest.fixture` to create a fixture with scope=module and provides an Arjuna's decorated version of the function that is marked with `for_module` decorator.

        Args:
            func: Function
    '''
    from arjuna import Arjuna
    return pytest.fixture(scope="module")(_simple_dec(func))

def for_test(func: Callable) -> Callable:
    '''
        Decorator for test function level test fixture/resource.

        Wraps `pytest.fixture` to create a fixture with scope=function and provides an Arjuna's decorated version of the function that is marked with `for_test` decorator.

        Args:
            func: A Function with signature `f(request)`. The name request is mandatory and enforced.
    '''
    from arjuna import Arjuna
    return pytest.fixture(scope="function")(_simple_dec(func))