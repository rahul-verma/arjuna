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


from arjuna.core.utils import obj_utils
import functools
import pytest

class Info:

    def __init__(self, func, pytest_request):
        self.__request = pytest_request
        self.__func = func
        self.__mod_name = func.__module__
        rnode = self.__request.node
        self.__orig_name = rnode.originalname and rnode.originalname or rnode.name
        self.__node_name = rnode.name

    def get_qual_name(self, with_params=False):
        # if pytest name has params only then originalname is set else it is None
        name = with_params and self.__node_name or self.__orig_name
        return self.__mod_name + "." + name

    @property
    def qual_name(self):
        return self.get_qual_name()

    @property
    def qual_name_with_data(self):
        return self.get_qual_name(with_params=True)

class My:

    def __init__(self, func):
        self.__func = func
        self.__data = None
        self.__info = None
        self.__handler = None
        self.__qual_name = None

    @property
    def data(self):
        return self.__data

    @data.setter
    def data(self, record):
        self.__data = record

    def set_req_obj(self, pytest_request):
        self.__info = Info(self.__func, pytest_request)

    @property
    def info(self):
        return self.__info

def tc(cls):
    setattr(cls, 'get_test_qual_name', get_test_qual_name)
    return cls

def call_func(func, my, request):
    from arjuna import Arjuna
    my.set_req_obj(request) 
    qual_name = my.info.qual_name_with_data
    Arjuna.get_logger().info("Begin test function: {}".format(qual_name))        
    func(my, request)
    Arjuna.get_logger().info("End test function: {}".format(qual_name))

def simple_dec(func):
    @functools.wraps(func)
    def wrapper(my, request):
        my.handler = request
        call_func(func, self, my, request)
    return wrapper

def tf(f=None, *, id=None, drive_with=None, exclude_if=None):
    if f is not None:
        return simple_dec(f)

    def format_test_func(func):
        orig_func = func
        if exclude_if:
            func = pytest.mark.dependency(name=id, depends=exclude_if())(func)
        else:
            func = pytest.mark.dependency(name=id)(func)

        if drive_with:
            records = drive_with.build().all_records
            my_objects = []
            for record in records:
                my = My(func)
                my.data = record
                my_objects.append(my)
            func = pytest.mark.parametrize('my', my_objects)(func) 

        @functools.wraps(orig_func)
        def wrapper(my, request):
            my.handler = request
            call_func(func, my, request)
        return wrapper
    
    return format_test_func

    

