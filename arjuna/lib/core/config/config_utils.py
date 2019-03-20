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

import os

from arjuna.lib.core.utils import file_utils
from arjuna.lib.core import ARJUNA_ROOT

def get_same(input):
    return input


def path_to_core_absolute_path(configured_dir):
    from arjuna.lib.core import ArjunaCore
    ret_path = None
    if configured_dir.startswith("*"):
        if configured_dir.startswith("*/") or configured_dir.startswith("*\\"):
            ret_path = file_utils.get_canonical_path(ARJUNA_ROOT + configured_dir[1:])
        else:
            ret_path = file_utils.get_canonical_path(ARJUNA_ROOT + os.path.sep + configured_dir[1:])
    else:
        ret_path = configured_dir
    return file_utils.normalize_path(ret_path)


def path_to_project_absolute_path(project_dir, configured_dir):
    from arjuna.lib.core import ArjunaCore
    ret_path = None
    if file_utils.is_absolute_path(configured_dir):
        ret_path = configured_dir
    else:
        ret_path = file_utils.get_canonical_path(project_dir + os.path.sep + configured_dir)
    return file_utils.normalize_path(ret_path)

def enum_to_prop_path(enum_obj):
    return str(enum_obj.name).lower().replace("_", ".")

def is_set(config_value):
    return not is_not_set(config_value)

def is_not_set(config_value):
    return config_value is None or config_value == "-"
