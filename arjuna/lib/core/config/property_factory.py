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

from functools import partial
from arjuna.lib.core.config import config_utils
from arjuna.lib.core.config.builder import *
from arjuna.lib.core.types.descriptors import *


def is_same(input):
    return input


def create_string_property(code, prop_path, config_value, purpose, visible, formatter=is_same):
    return create_property(code, prop_path, formatter(config_value), purpose, visible, ValueTypeEnum.STRING)


def create_string_list_property(code, prop_path, config_value, purpose, visible, formatter=None):
    if config_utils.is_not_set(config_value):
        return create_property(code, prop_path, config_value, purpose, visible, ValueTypeEnum.STRING_LIST)
    else:
        return create_property(code, prop_path, StringList.force_convert(config_value), purpose, visible,
                               ValueTypeEnum.STRING_LIST)


def create_core_dir_path(code, prop_path, config_value, purpose, visible):
    return create_string_property(code, prop_path, config_value, purpose, visible, config_utils.path_to_core_absolute_path)


def create_project_dir_path(project_dir, code, prop_path, config_value, purpose, visible):
    return create_string_property(code, prop_path, config_value, purpose, visible,
                                  partial(config_utils.path_to_project_absolute_path,project_dir))


def create_directories_property(code, prop_path, config_value, purpose, visible):
    return create_string_list_property(code, prop_path, config_value, purpose, visible, config_utils.path_to_core_absolute_path)


def create_enum_property(code, prop_path, klass, config_value, purpose, visible):
    value = EnumConstant.convert(klass, config_value)
    return create_property(code, prop_path, value, purpose, visible, ValueTypeEnum.ENUM)


def create_enum_list_property(code, prop_path, klass, config_value, purpose, visible):
    if config_utils.is_not_set(config_value):
        return create_none_property(code, ValueTypeEnum.ENUM_LIST, prop_path, purpose, visible)
    value = EnumConstantList.convert(klass, config_value)
    return create_property(code, prop_path, value, purpose, visible, ValueTypeEnum.ENUM_LIST)


def create_boolean_property(code, prop_path, config_value, purpose, visible):
    if config_utils.is_not_set(config_value):
        return create_none_property(code, ValueTypeEnum.BOOLEAN, prop_path, purpose, visible)
    value = Bool.force_convert(config_value)
    return create_property(code, prop_path, value, purpose, visible, ValueTypeEnum.BOOLEAN)


def create_number_property(code, prop_path, config_value, purpose, visible, expected_type=ValueTypeEnum.NUMBER):
    if config_utils.is_not_set(config_value):
        return create_none_property(code, expected_type, prop_path, purpose, visible)
    value = value_factory.create_number_value(config_value)
    return create_property(code, prop_path, value, purpose, visible, expected_type)


def create_int_property(code, prop_path, config_value, purpose, visible):
    return create_number_property(code, prop_path, config_value, purpose, visible, ValueTypeEnum.INTEGER)


def create_double_property(code, prop_path, config_value, purpose, visible):
    return create_number_property(code, prop_path, config_value, purpose, visible, ValueTypeEnum.DOUBLE)


def create_property(code, prop_path, config_value, purpose, visible, expected_type):
    builder = ConfigPropertyBuilder()
    return builder.code(code).path(prop_path).text(purpose).value(config_value).visible(visible).value_type(
        expected_type).build()


def create_none_property(code, prop_path, purpose, visible, expected_type):
    builder = ConfigPropertyBuilder()
    return builder.code(code).path(prop_path).text(purpose).value(value_factory.create_none_value()).visible(
        visible).value_type(expected_type).build()


def create_simple_property(prop_path, value, purpose="-"):
    builder = ConfigPropertyBuilder()
    return builder.code(UserDefinedPropertyEnum.UNKNOWN).path(prop_path).text(purpose).value(value).build()
