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

import abc

from arjuna.unitee.enums import *
from arjuna.unitee.markup import mrules

from .enums import *
from .exceptions import *
from .ref import *

class __BaseRule(metaclass=abc.ABCMeta):
    def __init__(self, rule_type, totype, is_inclusion_rule, robject, condition, expression):
        self.rule_type = rule_type
        self.totype = totype
        self.is_include_type = is_inclusion_rule
        self.robject = robject
        self.condition = condition
        self.expression = expression

        self._act_on_incompatible_converter(self.expression, name=self.robject)

    def _act_on_incompatible_converter(self, provided_value, name=None):
        pass

    def _not_met_exc(self):
        # Run time rules checking did not succeed for the test object
        raise RuleNotMet()

    def _raise_exception_for_check_result(self, check_result):
        if check_result:
            if self.is_include_type:
                return
            else:
                self._not_met_exc()
        else:
            if self.is_include_type:
                self._not_met_exc()
            else:
                return

    @abc.abstractmethod
    def _get_container(self, test_object):
        pass

    @abc.abstractmethod
    def is_object_defined_in(self, container):
        pass

    @abc.abstractmethod
    def _act_on_not_defined(self, expression):
        pass

    def _act_on_none_value(self, expression):
        pass

    def _get_target_value(self, container, name):
        return None

    def _act_on_value(self):
        pass

    def _convert_provided_value(self, provided_value, name=None, target_object_value=None):
        return provided_value

    def __is_applicable(self, test_object):
        if test_object.type not in {TestObjectTypeEnum.Module, TestObjectTypeEnum.Function}:
            return False
        elif test_object.type != self.totype:
            return False

        return True

    def evaluate(self, test_object):
        if not self.__is_applicable(test_object):
            return

        container = self._get_container(test_object)

        defined = self.is_object_defined_in(container)
        if not defined:
            self._act_on_not_defined(self.expression)

        if self.rule_type == RuleType.SET:
            return

        target_object_value = None
        if defined:
            target_object_value = self._get_target_value(container, self.robject)

        if target_object_value is None:
            self._act_on_none_value(self.expression)
            return

        if self.rule_type == RuleType.DICT_KEY:
            return

        try:
            provided_value = self._convert_provided_value(self.expression, name=self.robject, target_object_value=target_object_value)
        except Exception as e:
            # This would take place for user defined props/evars at this stage
            # E.g. in test user_prop is of type int and in rule it is given as a string
            # TO DO: Add more info and log as a run time error
            self._raise_exception_for_check_result(False)
        else:
            succeeded = self.__call_checker(target_object_value, provided_value)
            self._raise_exception_for_check_result(succeeded)

    def __call_checker(self, actual, expected):
        if type(actual) is str:
            actual = actual and actual.lower() or None
            expected = expected and expected.lower() or None
        func = VALUE_CHECKERS[self.condition]
        return func(actual, expected)

class _DictRule(__BaseRule):

    def __init__(self, rule_type, totype, is_inclusion_rule, robject, condition, expression):
        super().__init__(rule_type, totype, is_inclusion_rule, robject, condition, expression)

    def __contains(self, container, value):
        try:
            container[value]
            return True
        except:
            return False

    def is_object_defined_in(self, container):
        if type(self.robject) is str:
            return self.__contains(container, self.robject.lower())
        else:
            for value in self.robject:
                if not self.__contains(container, value):
                    return False
            return True

    def _act_on_not_defined(self, expression):
        if expression.lower() in {"defined", "present"}:
            self._raise_exception_for_check_result(False)
        elif expression.lower() == "none":
            # For a None value check, should be considered a match
            self._raise_exception_for_check_result(True)
        else:
            # For non-None expression, should be considered a non-match
            self._raise_exception_for_check_result(False)

    def _get_target_value(self, container, name):
        return container[name]

    def _act_on_none_value(self, expression):
        # Decision process is same as Not-def value. However this one works for dictionaries as well.
        self._act_on_not_defined(expression)

class DictKeyPresenceRule(_DictRule):

    def __init__(self, totype, is_inclusion_rule, robject, condition, expression):
        super().__init__(RuleType.DICT_KEY, totype, is_inclusion_rule, robject, condition, expression)

class DictKeyValueRule(_DictRule):

    def __init__(self, totype, is_inclusion_rule, robject, condition, expression):
        super().__init__(RuleType.DICT_VALUE, totype, is_inclusion_rule, robject, condition, expression)

class SetEntryPresenceRule(__BaseRule):

    def __init__(self, totype, is_inclusion_rule, robject, condition, expression):
        super().__init__(RuleType.SET, totype, is_inclusion_rule, robject, condition, expression)

    def is_object_defined_in(self, container):
        if type(self.robject) is str:
            return self.robject.lower() in container
        else:
            for i in self.robject:
                if i not in container:
                    return False
            return True

    def _act_on_not_defined(self, expression):
        self._raise_exception_for_check_result(False)


