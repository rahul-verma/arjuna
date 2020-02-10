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
import functools
import pytest

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

class Resources:

    def __init__(self, pytest_request):
        vars(self)['_request'] = pytest_request

    def __getitem__(self, name):
        scopes = LOOKUP_ORDER[self._request.scope]
        for scope in scopes:
            try:
                container = getattr(self._request, SCOPE_MAP[scope])
                return getattr(container, name)
            except Exception as e:
                continue
        raise Exception("Attribute with name >>{}<< does not exist in request scope for {}".format(name, scopes))

    def __setitem__(self, name, value):
        container = getattr(self._request, SCOPE_MAP[self._request.scope])
        setattr(container, name, value)

    def __getattr__(self, name):
        if type(name) is str and not name.startswith("__"):
            return self[name]

    def __setattr__(self, name, value):
        container = getattr(self._request, SCOPE_MAP[self._request.scope])
        setattr(container, name, value)

    @property
    def raw_request(self):
        return self._request

class My:

    def __init__(self):
        self.__data = None
        self.__info = None
        self.__resources = None
        self.__handler = None
        self.__qual_name = None
        self.__request =  None
        self.__shared_objects = None

    @property
    def data(self):
        return self.__data

    @property
    def module_shared_space(self):
        return self.__request.module.shared_space

    @data.setter
    def data(self, record):
        self.__data = record

    def set_req_obj(self, pytest_request):
        self.__request = pytest_request
        self.__info = Info(pytest_request)
        self.__resources = Resources(pytest_request)
        if pytest_request.scope in {"session", "module", "class"}:
            try:
                getattr(pytest_request.module, "shared_space")
                print("old", pytest_request)
            except:
                print("new", pytest_request)
                pytest_request.module.shared_space = SharedObjects()

    @property
    def info(self):
        return self.__info

    @property
    def resources(self):
        return self.__resources

    @property
    def raw_request(self):
        return self.__request

def tc(cls):
    setattr(cls, 'get_test_qual_name', get_test_qual_name)
    return cls

def call_func(func, my, request, *args, **kwargs):
    from arjuna import Arjuna
    my.set_req_obj(request) 
    qual_name = my.info.qual_name_with_data
    Arjuna.get_logger().info("Begin test function: {}".format(qual_name))        
    func(my, request, *args, **kwargs)
    Arjuna.get_logger().info("End test function: {}".format(qual_name))

def simple_dec(func):
    @functools.wraps(func)
    def wrapper(my, request, *args, **kwargs):
        my.handler = request
        call_func(func, my, request, *args, **kwargs)
    return wrapper

def test(f=None, *, id=None, resources=None, drive_with=None, exclude_if=None):

    # Check if @test is provided without arguments
    if f is not None:
        my = My()
        my.data = DummyDataRecord()
        func = pytest.mark.parametrize('my', [my])(f) 
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
            func = pytest.mark.parametrize('my', my_objects)(func) 
        else:
            my = My()
            my.data = DummyDataRecord()
            func = pytest.mark.parametrize('my', [my])(func) 

        @functools.wraps(orig_func)
        def wrapper(my, request, *args, **kwargs):
            my.handler = request
            call_func(func, my, request, *args, **kwargs)
        return wrapper
    
    return format_test_func

    

