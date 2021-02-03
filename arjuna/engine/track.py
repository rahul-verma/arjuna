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

import os
import sys
import types
import inspect
import functools

from arjuna.core.utils.obj_utils import get_class_for_method

prop_dict_msg = {
    "fget": ("(Getting Property)","", " Returning: {}"),
    "fset": ("(Setting Property)", ":: Args: {}, Kwargs: {}.", ""),
    "fdel": ("(Deleting Property)","", ""),
}

def trim_arg(arg, max_len=300):
    arg = str(arg)
    return len(arg) > max_len and arg[0:max_len] + "<SNIP>" or arg

def trim_args(args):
    return [trim_arg(arg) for arg in args]

def trim_kwargs(kwargs):
    return {k:trim_arg(v) for k,v in kwargs.items()}

def trim_ret_value(ret):
    return trim_arg(ret, max_len=200)

def func_wrapper(func, level, *vargs, static=False, prop=False, prop_type="fget", **kwargs):
    import arjuna
    from arjuna import log_error
    name = func.__name__
    qualname = func.__qualname__
    if name not in {"__init__", "__getattr__"}:
        level = name.startswith("_") and "trace" or level
    log_call = getattr(arjuna, "log_{}".format(level.strip().lower()))
    if name != qualname and not static:
        pvargs = vargs[1:]
    else:
        pvargs = vargs

    if prop:
        msg_1 = prop_dict_msg[prop_type][0]
        msg_2 = prop_dict_msg[prop_type][1].format(pvargs, kwargs)
        log_call("{} {}{}".format(qualname, msg_1, msg_2))
    elif name == "__getattr__":
        log_call("{} Dynamic attr retrieval.".format(qualname.replace("__getattr__", pvargs[0])))
    else:
        log_call("{}:: Started with args {} and kwargs {}.".format(qualname, trim_args(pvargs), trim_kwargs(kwargs)))
    ret = None
    try:
        ret = func(*vargs, **kwargs)
    except Exception as e:
        import traceback
        log_call("{}:: Exception: {}.".format(qualname, e))

        # Same exception should be raised else it WILL cause error-dependent-logic error
        raise e
    else:
        if prop:
            msg_1 = prop_dict_msg[prop_type][0]
            msg_3 = prop_dict_msg[prop_type][2].format(ret)
            log_call("{}:: Finished.{}".format(qualname, msg_3, msg_3))
        elif name == "__getattr__":
            log_call("{} Dynamic attr value: {}.".format(qualname.replace("__getattr__", pvargs[0]), trim_ret_value(ret)))
        else:
            log_call("{}:: Finished. Returning: {}".format(qualname, trim_ret_value(ret)))
        return ret

def track_func(level="debug", static=False, prop=False, prop_type="fget"):

    def dec(func):
        fname = func.__name__
        if prop is True:
            if not hasattr(func, "_wrapped"):
                func._wrapped = True
            elif func._wrapped:
                return func
        @functools.wraps(func)
        def inner(*vargs, **kwargs):
            return func_wrapper(func, level, *vargs, static=static, prop=prop, prop_type=prop_type, **kwargs)
        return inner

    return dec

def wrap_methods(cls, level): #, *args, **kwargs):
    for attr_name, attr in vars(cls).items():
        if type(attr) is types.FunctionType:
            setattr(cls, attr_name, track_func(level)(attr))
        elif isinstance(attr, classmethod):
            setattr(cls, attr_name, classmethod(track_func(level)(attr.__func__)))
        elif isinstance(attr, staticmethod):
            setattr(cls, attr_name, staticmethod(track_func(level, static=True)(attr.__func__)))
    # return cls(*args, **kwargs)

# def track_class(level):

#     def deco(cls):
#         @functools.wraps(cls)
#         def class_wrapper(*args, **kwargs):
#             return wrap_methods(cls, level, *args, **kwargs)
#         return class_wrapper

#     return deco


def track_class(cls, level):
    wrap_methods(cls, level)
    return cls