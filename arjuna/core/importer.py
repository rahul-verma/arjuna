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

import importlib

def import_module(mod_name, *, prefix="", optional=False):
    full_path = mod_name
    if prefix: 
        ".".join([prefix, full_path])
    try:
        mod = importlib.import_module(full_path)
    except ModuleNotFoundError:
        if not optional:
            raise
    else:
        return mod 

def import_name_in_module(*, mod_name, name, prefix="", optional=False):
    mod = import_module(mod_name, prefix=prefix, optional=optional)
    if mod is None:
        return None

    try:
        return getattr(mod, name)
    except AttributeError:
        if not optional:
            raise ImportError("{} is not defined in module: {}".format(name, mod))

def import_arj_hook_module(mod_name, optional=False):
    from arjuna import C
    return import_module(mod_name, prefix=C("hooks.package"), optional=optional)

def import_name_in_arj_hook_module(*, mod_name, name, optional=False):
    from arjuna import C
    mod = import_arj_hook_module(mod_name)
    return import_name_in_module(mod_name=mod_name, name=name, prefix=C("hooks.package"), optional=optional)

def import_arj_resouce_hook_package():
    from arjuna import C
    import_name_in_module(mod_name=C("hooks.config.package"), name='*', optional=True)

def import_arj_config_hook(name):
    from arjuna import C
    return import_name_in_module(mod_name=C("hooks.config.package"), name=name, optional=True)

def import_arj_entity(name):
    from arjuna import C
    return import_name_in_module(mod_name=C("hooks.entity.package"), name=name, optional=False)