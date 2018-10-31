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


class BugsDefinedRule(SetEntryPresenceRule):

    def __init__(self, totype, is_inclusion_rule, robject, condition, expression):
        super().__init__(totype, is_inclusion_rule, robject, condition, expression)

    def _get_container(self, test_object):
        return test_object.tvars.bugs

    def _convert_target_value(self, name, provided_value, target_object_value):
        return (str(i).lower() for i in provided_value)


