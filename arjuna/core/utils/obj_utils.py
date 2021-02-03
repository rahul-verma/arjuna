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

import inspect
import types


def get_class_name(obj):
    o = isinstance(obj, type) and obj or type(obj)
    return o.__name__


def get_class_qual_name(obj):
    o = isinstance(obj, type) and obj or type(obj)
    return o.__module__ + "." + o.__name__


def callable(obj):
    return not is_object(obj)


def is_module(obj):
    return type(obj) is types.ModuleType


def is_object(obj):
    return not isinstance(obj, type) and not type(obj) is types.FunctionType


def is_class(obj):
    return isinstance(obj, type)


def is_function(obj):
    return type(obj) is types.FunctionType and obj.__qualname__ == obj.__name__


def is_method(obj):
    return type(obj) is types.FunctionType and obj.__qualname__ != obj.__name__


def is_private(obj):
    return obj.__name__.startswith('__')


def is_protected(obj):
    return obj.__name__.startswith('_')


def is_public(obj):
    return not is_private(obj) and not is_protected(obj)


class IterItemOp:
    def __init__(self, i):
        self._i = i

    def __eq__(self, obj):
        if type(obj) is bool:
            for i in self._i:
                if bool(i) != obj:
                    return False
            return True
        else:
            for i in self._i:
                if i != obj:
                    return False
            return True


def is_my_sig(obj):
    args, *rest = inspect.getfullargspec(obj)
    if args == ['my'] and IterItemOp(rest) == False:
        return True
    else:
        return False

def get_class_for_method(meth):
    '''
        Based on https://stackoverflow.com/a/3589335 by Alex Martelli
    '''
    if inspect.ismethod(meth):
        for cls in inspect.getmro(meth.__self__.__class__):
            if cls.__dict__.get(meth.__name__) is meth:
                return cls.__name__
        meth = meth.__func__
    if inspect.isfunction(meth):
        return meth.__qualname__.rsplit('.', 1)[0]

def get_function_meta_data(func):
    meta = dict()
    module_full_name = inspect.getmodule(func).__name__
    mod_parts = module_full_name.split('.')
    package = ".".join(mod_parts[0:-1])
    module = mod_parts[-1]
    meta['package'] = package
    meta['module'] = module
    meta['name'] = func.__name__
    meta['qual_name'] = "{}.{}".format(module_full_name, func.__name__)
    return meta
