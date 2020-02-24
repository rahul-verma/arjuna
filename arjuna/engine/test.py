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
from arjuna.engine.hook import PytestHooks
from arjuna.engine.data.record import DummyDataRecord
from arjuna.engine.data.store import SharedObjects
from arjuna.engine.asserter import Asserter
import functools
import pytest
import unittest

class Info:

    def __init__(self, pytest_request):
        self.__request = pytest_request
        self.__mod_name = pytest_request.module.__name__
        rnode = self.__request.node
        if self.__request.scope == "module":
            self.__orig_name = rnode.name
            self.__node_name = rnode.name
        elif self.__request.scope == "function":
            self.__orig_name = rnode.originalname and rnode.originalname or rnode.name
            self.__node_name = rnode.name

    def get_qual_name(self, with_params=False):
        # if pytest name has params only then originalname is set else it is None
        if self.__request.scope == "module":
            return self.__node_name
        else:
            name = with_params and self.__node_name or self.__orig_name
            return self.__mod_name + "." + name

    @property
    def qual_name(self):
        return self.get_qual_name()

    @property
    def qual_name_with_data(self):
        qname = self.get_qual_name(with_params=True)
        if self.__request.fixturename:
            return qname + ":" + self.__request.fixturename
        else:
            return qname

    def __getattr__(self, name):
        return getattr(self.__request, name)

LOOKUP_ORDER = {
    "session" : ("session", ),
    "module" : ("session", "module"),
    "class" : ("function", "cls", "module"),
    "function" : ("function", "cls", "module", "session")
}

SCOPE_MAP = {
    "function" : "function",
    "class"    : "cls",
    "module"   : "module",
    "session"  : "session"
}

class Space:

    def __init__(self, pytest_request):
        vars(self)['_request'] = pytest_request

    def __getitem__(self, name):
        scopes = LOOKUP_ORDER[self._request.scope]
        from arjuna import Arjuna
        for scope in scopes:
            Arjuna.get_logger().debug("Space: Getting value for {} from {} scope".format(name, scope))
            try:
                container = getattr(self._request, SCOPE_MAP[scope])
                return getattr(container, name)
            except Exception as e:
                Arjuna.get_logger().debug("Space: No value for {} in {} scope".format(name, scope))
                continue
        raise Exception("Attribute with name >>{}<< does not exist in request scope for {}".format(name, scopes))

    def _get_container_for_scope(self):
        return getattr(self._request, SCOPE_MAP[self._request.scope])

    def __setitem__(self, name, value):
        container = self._get_container_for_scope()
        setattr(container, name, value)

    def __getattr__(self, name):
        if type(name) is str and not name.startswith("__"):
            return self[name]

    def __setattr__(self, name, value):
        container = self._get_container_for_scope()
        from arjuna import Arjuna
        Arjuna.get_logger().debug("Space: Setting {}={} in {} scope".format(name, value, self._request.scope))
        setattr(container, name, value)

    @property
    def raw_request(self):
        return self._request

class ModuleSpace(Space):

    def __init__(self, pytest_request):
        super().__init__(pytest_request)

    def _get_container_for_scope(self):
        return getattr(self._request, "module")

class Module:

    def __init__(self, py_request):
        self._space = ModuleSpace(py_request)

    @property
    def space(self):
        return self._space

class My:

    def __init__(self):
        self._data = None
        self._info = None
        self._handler = None
        self._qual_name = None
        self._request =  None
        self._shared_objects = None
        self._asserter = Asserter() #unittest.TestCase('__init__')
        self._space = None
        self._module = None

    @property
    def module(self):
        return self._module

    @property
    def data(self):
        return self._data

    @property
    def asserter(self):
        return self._asserter

    @data.setter
    def data(self, record):
        self._data = record

    @property
    def space(self):
        return self._space

    def set_req_obj(self, pytest_request):
        self._request = pytest_request
        self._info = Info(pytest_request)
        self._space = Space(pytest_request)
        if pytest_request.scope in {"function"}:
            if not self._module:
                self._module = Module(pytest_request)
                

    @property
    def info(self):
        return self._info

    @property
    def resources(self):
        return self._resources

    @property
    def raw_request(self):
        return self._request

def tc(cls):
    setattr(cls, 'get_test_qual_name', get_test_qual_name)
    return cls

def call_func(func, request, data=None, *args, **kwargs):
    from arjuna import Arjuna
    request_wrapper = My()
    request_wrapper.set_req_obj(request)
    qual_name = request_wrapper.info.qual_name_with_data
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
            my.handler = request
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

    

