'''
This file is a part of Test Mile Arjuna
Copyright 2018 Test Mile Software Testing Pvt Ltd

Website: www.TestMile.com
Email: support [at] testmile.com
Creator: Rahul Verma

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

import inspect
from copy import deepcopy

from arjuna.lib.unitee.state.loader import *
from arjuna.lib.core.utils import obj_utils
from arjuna.lib.unitee import Unitee

def init_module(id=None, *,
                priority=5,
                threads=1,
                evars=None,
                tags=None,
                drive_with=None,
                data_ref=None,
                exclude_if=None,

                name=None, author=None, bugs=None, idea=None, unstable=False,
                component=None, app_version=None,

                **kwargs):
    clocals = {i:j for i,j in locals().items()}
    if obj_utils.callable(id):
        kallable = id
        del clocals['id']
        return Unitee.test_loader.register_tmodule(kallable, **clocals)
    else:
        def wrapper(kallable):
            return Unitee.test_loader.register_tmodule(kallable, **clocals)
        return wrapper

def test_function(id=None, *,
                  priority=5,
                  threads=1,
                  evars=None,
                  tags=None,
                  drive_with=None,
                  data_ref=None,
                  exclude_if=None,

                  name=None, author=None, bugs=None, idea=None, unstable=False,
                  component=None, app_version=None,

                  **kwargs):
    clocals = {i:j for i,j in locals().items()}
    if obj_utils.callable(id):
        kallable = id
        del clocals['name']
        return Unitee.test_loader.register_tfunc(kallable, **clocals)
    else:
        def wrapper(kallable):
            return Unitee.test_loader.register_tfunc(kallable, **clocals)
        return wrapper

def fixture(dec_name, kallable):
    if obj_utils.callable(kallable):
        return Unitee.test_loader.register_fixture(dec_name, kallable)
    else:
        def wrapper(actual_kallable):
            msg = "You are decorating {} in {} module with @{} by providing one or more arguments."
            msg += "Remove the arguments and proceed."
            ArjunaCore.console.display_error(msg.format(
                    actual_kallable.__qualname__,
                    actual_kallable.__module__,
                    dec_name
                ))
            sys_utils.fexit()
        return wrapper


def skip_me(kallable):
    if obj_utils.callable(kallable):
        return Unitee.test_loader.register_skip_func(kallable)
    else:
        def wrapper(actual_kallable):
            msg = "You are decorating {} in {} module with @skip by providing one or more arguments."
            msg += "Remove the arguments and proceed."
            ArjunaCore.console.display_error(msg.format(
                    actual_kallable.__qualname__,
                    actual_kallable.__module__
                ))
            sys_utils.fexit()
        return wrapper
    
