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

import functools
import pytest
import unittest
from arjuna.core.utils import obj_utils
from arjuna.tpi.engine.hook import PytestHooks
from arjuna.tpi.engine.data.record import DummyDataRecord
from arjuna.engine.data.store import SharedObjects
from arjuna.engine.meta import *

def tc(cls):
    setattr(cls, 'get_test_qual_name', get_test_qual_name)
    return cls

def call_func(func, request, data=None, *args, **kwargs):
    from arjuna import Arjuna
    request_wrapper = My()
    request_wrapper.set_req_obj(request)
    qual_name = request_wrapper.info.get_qual_name_with_data()
    Arjuna.get_logger().info("Begin test function: {}".format(qual_name))  
    if data:      
        func(request=request_wrapper, data=data, *args, **kwargs)
    else:
        func(request=request_wrapper, *args, **kwargs)
    Arjuna.get_logger().info("End test function: {}".format(qual_name))

def simple_dec(func):
    func.__name__ = "check_" + func.__name__

    @functools.wraps(func)
    def wrapper(request, *args, **kwargs):
        call_func(func, request, *args, **kwargs)
    return wrapper

def repr_record(record):
    return str(record)

def test(f=None, *, id=None, resources=None, drive_with=None, exclude_if=None):

    # Check if @test is provided without arguments
    if f is not None:
        return simple_dec(f)

    if resources:
        if type(resources) is str:
            resources = (resources)
        elif type(resources) is list:
            resources = tuple(resources)
        else:
            raise Exception("resources value must be a string or list/tuple of strings")

    def format_test_func(func):
        orig_func = func
        if exclude_if:
            func = pytest.mark.dependency(name=id, depends=exclude_if())(func)
        else:
            func = pytest.mark.dependency(name=id)(func)

        if resources:
            func = pytest.mark.usefixtures(*resources)(func)

        if drive_with:
            records = drive_with.build().all_records
            my_objects = []
            for record in records:
                my = My()
                my.data = record
                my_objects.append(my)
            func = pytest.mark.parametrize('data', records, ids=repr_record)(func) 
        # else:
        #     my = My()
        #     my.data = DummyDataRecord()
        #     func = pytest.mark.parametrize('my', [my], ids=My.repr)(func) 

        @functools.wraps(orig_func)
        def wrapper_without_data(request, *args, **kwargs):
            request.handler = request
            call_func(func, request, *args, **kwargs)

        @functools.wraps(orig_func)
        def wrapper_with_data(request, data, *args, **kwargs):
            my.handler = request
            call_func(func, request, data, *args, **kwargs)

        if drive_with:
            return wrapper_with_data
        else:
            return wrapper_without_data
    
    return format_test_func

    

