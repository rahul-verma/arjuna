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

import xml.etree.ElementTree as ETree

from arjuna.unitee.markup import mrules
from arjuna.unitee.enums import *

from .common.enums import *
from .common.rule import *
from .common.ref import *
from .bugs import *
from .tags import *
from .builtin_prop import *
from .user_prop import *
from .evars import *


class RuleBuilder:

    def __init__(self):
        self.__xml = None
        self.__totype = None
        self.__is_include_type = RuleNature.INCLUDE
        self.__target = None
        self.__robject = None
        self.__condition = None
        self.__expression = None

    def xml(self, xml):
        self.__xml = xml

    def test_object_type(self, totype):
        self.__totype = TestObjectTypeEnum[totype]
        return self

    def rule_type(self, rtype):
        self.__is_include_type = RuleNature[rtype.upper().strip()] == RuleNature.INCLUDE
        return self

    def target(self, container):
        self.__target = container

    def rule_object(self, target_name):
        self.__robject = target_name
        if type(self.__robject) is str:
            self.__robject = self.__robject.lower()
        return self

    def condition(self, condition):
        try:
            if type(condition) is str:
                if condition.lower() in SYMBOLS_MAP:
                    condition = SYMBOLS_MAP[condition.lower()]
                self.__condition = RuleConditionType[condition.upper()]
            else:
                self.__condition = condition
        except:
            raise Exception("Invalid condition supplied in rule: " + condition)
        return self

    def expression(self, expression):
        self.__expression = expression
        return self

    def build(self):
        if not self.__totype:
            raise Exception("Test object not defined for rule.")
        elif not self.__target:
            raise Exception("Target container not defined for rule.")
        elif not self.__robject:
            raise Exception("Target object not defined for rule.")
        elif not self.__condition:
            raise Exception("Condition not defined for rule.")
        elif not self.__expression:
            raise Exception("Expression not defined for rule.")

        if type(self.__robject) is str:
            if mrules.is_builtin_prop(self.__robject.upper()):
                # For built-in properties, checking for valid conditions happens at time of loading
                # For user defined properties, it is done as per the type of user defined property for a given test object
                # So, the latter can happen not at rule definition level, but based on test object
                # provided at run time.
                converter = mrules.get_value_type(self.__robject)
                allowed_condition_set = ALLOWED_CONDITIONS[converter]
                if self.__condition not in allowed_condition_set:
                    raise Exception("Rules for Built-in property >>{}<< of type {} can only use {} relation(s).".format(
                        self.__robject,
                        converter,
                        ALLOWED_SYMBOLS[converter]
                    ))

            # The condition has been named as contains for eace of use for string conditions in XML
            # Internally, contains for iterables means element content
            # For string it means partial match.
            if self.__condition == RuleConditionType.CONTAINS:
                self.__condition = RuleConditionType.PARTIALLY_MATCHES

        cls = None
        if self.__target == RuleTargetType.TAGS:
            cls = TagsDefinedRule
        elif self.__target == RuleTargetType.BUGS:
            cls = BugsDefinedRule
        elif self.__target == RuleTargetType.PROPS:
            if mrules.is_builtin_prop(self.__robject.upper()):
                if self.__expression in {'defined', 'present'}:
                    cls = BuiltInPropsDefinedRule
                else:
                    cls = BuiltInPropValueRule
            else:
                if self.__expression in {'defined', 'present'}:
                    cls = UserPropsDefinedRule
                else:
                    cls = UserPropValueRule

        elif self.__target == RuleTargetType.EVARS:
            if self.__expression in {'defined', 'present'}:
                cls = EvarsDefinedRule
            else:
                cls = EvarValueRule

        try:
            return cls(
                self.__totype,
                self.__is_include_type,
                self.__robject,
                self.__condition,
                self.__expression
            )
        except Exception as e:
            raise Exception("Problem in constructing rule object for {}. Message: {}".format(
                ETree.tostring(self.__xml).strip(),
                e
            ))