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
from arjuna.engine.data.record import DummyDataRecord
from arjuna.engine.data.store import SharedObjects
from arjuna.engine.meta import *
from typing import Callable
from arjuna.tpi.arjuna_types import ListOrTuple
from arjuna.tpi.helper.arjtype import CIStringDict
from arjuna.core.utils.obj_utils import get_function_meta_data

def _tc(cls):
    setattr(cls, 'get_test_qual_name', get_test_qual_name)
    return cls

def _call_func(func, request_wrapper, data=None, *args, **kwargs):
    from arjuna import Arjuna
    qual_name = request_wrapper.info.get_qual_name_with_data()
    Arjuna.get_logger().info("Begin test function: {}".format(qual_name))  
    if data:      
        func(request=request_wrapper, data=data, *args, **kwargs)
    else:
        func(request=request_wrapper, *args, **kwargs)
    Arjuna.get_logger().info("End test function: {}".format(qual_name))

def _simple_dec(func, test_meta_data):
    test_meta_data['info'].update(get_function_meta_data(func))
    from arjuna import Arjuna
    Arjuna.register_test_meta_data(test_meta_data['info']['qual_name'], CIStringDict(test_meta_data))
    func.__name__ = "check_" + func.__name__

    @functools.wraps(func)
    def wrapper(request, *args, **kwargs):
        request_wrapper = My(test_meta_data)
        request_wrapper.set_req_obj(request)
        _call_func(func, request_wrapper, *args, **kwargs)
    return wrapper

def _repr_record(record):
    return str(record)

def test(
            f:Callable=None, *, 
            id: str=None, 
            resources: ListOrTuple=None, 
            drive_with: 'DataSource'=None, 
            exclude_if: 'Relation'=None,
            priority: int=5,
            author: str=None,
            idea: str=None,
            component: str=None,
            app_version: str='0.0.0',
            level: str=None,
            reviewed: bool= False,
            unstable: bool= False,
            tags: set=set(),
            bugs: set=set(),
            envs: set=set(),
            **test_attrs):
    '''
        Decorator for marking a function as a test function.

        Args:
            func: A Function with signature **f(request)**. The name request is mandatory and enforced.

        Keyword Arguments:
            id: (Optional) Alnum string representing an ID which you want to associate with the test.
            resources: (Optional) Fixtures/Resources that you want to associate this test with. Wraps pytest.mark.usefixtures. Instead of using this, you can also pass the names as direct arguments in the function signature.
            drive_with: (Optional) Used for data driven testing. Argument can be Arjuna Data Source. Wraps **pytest.mark.parametrize**. If you use this argument, the test function signature must include a **data** argument e.g. 

                .. code-block:: python
                
                    @test(drive_with=<DS>)
                    def check_sample(request, data):
                        pass

            exclude_if: (Optional) Define exclusion condition. Argument can be an Arjuna Relation. Wraps **pytest.mark.dependency**.
        Note:
            The test function name must start with the prefix **check_**

            The test function must have the minimum signature as **check_<some_name>(request)** with **request** as the first argument.
    '''

    info_dict = CIStringDict()
    info_dict.update({
        'id': id,
        'priority': priority,
        'author': author,
        'idea': idea,
        'component': component,
        'app_version': app_version,
        'level': level,
        'reviewed': reviewed,
        'unstable': unstable,
    })
    info_dict.update(test_attrs)

    test_meta_data = {
        'tags': tags,
        'bugs': bugs,
        'envs': envs,
        'info': info_dict
    }

    # Check if @test is provided without arguments
    if f is not None:
        return _simple_dec(f, test_meta_data)

    if resources:
        if type(resources) is str:
            resources = (resources)
        elif type(resources) is list:
            resources = tuple(resources)
        else:
            raise Exception("resources value must be a string or list/tuple of strings")

    def format_test_func(func):
        test_meta_data['info'].update(get_function_meta_data(func))
        from arjuna import Arjuna
        Arjuna.register_test_meta_data(test_meta_data['info']['qual_name'], CIStringDict(test_meta_data))
        orig_func = func
        if exclude_if:
            func = pytest.mark.dependency(name=id, depends=exclude_if())(func)
        else:
            func = pytest.mark.dependency(name=id)(func)

        if resources:
            func = pytest.mark.usefixtures(*resources)(func)

        if drive_with:
            records = drive_with.build().all_records
            func = pytest.mark.parametrize('data', records, ids=_repr_record)(func) 

        my = My(test_meta_data)

        @functools.wraps(orig_func)
        def wrapper_without_data(request, *args, **kwargs):
            my.set_req_obj(request)
            _call_func(func, my, *args, **kwargs)

        @functools.wraps(orig_func)
        def wrapper_with_data(request, data, *args, **kwargs):
            my.set_req_obj(request)
            _call_func(func, my, data, *args, **kwargs)

        if drive_with:
            return wrapper_with_data
        else:
            return wrapper_without_data
    
    return format_test_func

    

