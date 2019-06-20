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

from arjuna.unitee.enums import *

def is_test_module(test_object):
    return test_object.type == TestObjectTypeEnum.Module


def is_test_function(test_object):
    return test_object.type == TestObjectTypeEnum.Function

def none(value):
    if type(value) is str:
        return value.lower() == "none" and None or value
    else:
        return value is None and None or value

def custom_bool(value):
    from .ref import BOOL_MAP
    if type(value) is bool:
        return value
    elif value.lower() in BOOL_MAP:
        return BOOL_MAP[value.lower()]
    else:
        raise Exception("Provided unexpected value for boolean context in rule. Allowed: [true/false/on/off/yes/no/0/1]")