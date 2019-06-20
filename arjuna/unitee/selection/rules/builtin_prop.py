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

from .common.rule import *
from .common.utils import *
from arjuna.unitee.markup import mrules

def get_container(test_object):
    if is_test_module(test_object):
        return test_object.tvars.info.module.props
    elif is_test_function(test_object):
        return test_object.tvars.info.function.props


class BuiltInPropsDefinedRule(DictKeyPresenceRule):

    def __init__(self, totype, is_inclusion_rule, robject, condition, expression):
        super().__init__(totype, is_inclusion_rule, robject, condition, expression)

    def _get_container(self, test_object):
        return get_container(test_object)


class BuiltInPropValueRule(DictKeyValueRule):

    def __init__(self, totype, is_inclusion_rule, robject, condition, expression):
        super().__init__(totype, is_inclusion_rule, robject, condition, expression)

    def _act_on_incompatible_converter(self, provided_value, name=None):
        try:
            self._convert_provided_value(provided_value, name=name)
        except Exception as e:
            raise Exception("Incpomatible value >>{}<< supplied for built-in property >>{}<< of type >>{}<<".format(
                provided_value,
                name,
                mrules.get_value_type(name)
            ))

    def _get_container(self, test_object):
        return get_container(test_object)

    def _convert_provided_value(self, provided_value, name=None, target_object_value=None):
        target_type = mrules.get_value_type(name)
        if target_type == bool:
            target_type = custom_bool
        return target_type(provided_value)