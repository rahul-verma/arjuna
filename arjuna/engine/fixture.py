'''
This file is a part of Arjuna
Copyright 2015-2020 Rahul Verma

Website: www.RahulVerma.net

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

  http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
'''

import pytest
import itertools
import functools

from .test import My
from .test import My

def wraps_safely(obj, attr_names=functools.WRAPPER_ASSIGNMENTS):
    return functools.wraps(obj, assigned=itertools.ifilter(functools.partial(hasattr, obj), attr_names))

def simple_dec(func):
    @functools.wraps(func)
    def call_func(request, *args, **kwargs):
        from arjuna import Arjuna
        request_wrapper = My()
        request_wrapper.set_req_obj(request)
        qual_name = request_wrapper.info.qual_name_with_data
        Arjuna.get_logger().info("Begin fixture function: {}".format(qual_name))   
        yield from func(request_wrapper, *args, **kwargs)
        Arjuna.get_logger().info("End fixture function: {}".format(qual_name))
    return call_func

def for_module(func):
    from arjuna import Arjuna
    return pytest.yield_fixture(scope="module")(simple_dec(func))

def for_test(func):
    from arjuna import Arjuna
    return pytest.yield_fixture(scope="function")(simple_dec(func))