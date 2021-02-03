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

from arjuna.core.error import ExclusionRuleMet, NoInclusionRuleMet

from .rule import *

class Selector:

    def __init__(self):
        self.__irules = list()
        self.__erules = list()

        self.__package_erules = list()
        self.__package_irules = list()
        self.__module_erules = list()
        self.__module_irules = list()
        self.__test_erules = list()
        self.__test_irules = list()

        self.__frozen = False

    def include(self, rule_str):
        self.__irules.append(self.__build_rule(rule_str))

    def exclude(self, rule_str):
        self.__erules.append(self.__build_rule(rule_str))

    def __build_rule(self, rule_str):
        pattern = None
        rule_str = rule_str.replace(r'\!', '!') # From command line ! has to be escaped
        try:
            return BoolAttrPatternRule.from_str(rule_str)
        except RulePatternDoesNotMatchError:
            try:
                return IterablePatternRule.from_str(rule_str)
            except RulePatternDoesNotMatchError:
                try:
                    return AttrPatternRule.from_str(rule_str)
                except RulePatternDoesNotMatchError:
                    raise Exception("Rule is invalid: " + rule_str)

    @property
    def irules(self):
        return self.__irules

    @property
    def erules(self):
        return self.__erules

    @property
    def package_irules(self):
        return self.__package_irules

    @property
    def package_erules(self):
        return self.__package_erules

    @property
    def module_irules(self):
        return self.__module_irules

    @property
    def module_erules(self):
        return self.__module_erules

    @property
    def test_irules(self):
        return self.__test_irules

    @property
    def test_erules(self):
        return self.__test_erules

    def __freeze(self):
        for irule in self.irules:
            if irule.target == "package":
                self.__package_irules.append(irule)
            elif irule.target == "module":
                self.__module_irules.append(irule)
            else:
                self.__test_irules.append(irule)

        for erule in self.erules:
            if erule.target == "package":
                self.__package_erules.append(erule)
            elif erule.target == "module":
                self.__module_erules.append(erule)
            else:
                self.__test_erules.append(erule)

    def __validate_package_rules(self, obj):
        for rule in self.__package_erules:
            if rule.matches(obj):
                raise ExclusionRuleMet(rule)

        if not self.__package_irules:
            return

        for rule in self.__package_irules:
            if not rule.matches(obj):
                continue
            else:
                return

        raise NoInclusionRuleMet()

    def __validate_module_rules(self, obj):
        for rule in self.__module_erules:
            if rule.matches(obj):
                raise ExclusionRuleMet(rule)

        if not self.__module_irules:
            return

        for rule in self.__module_irules:
            if not rule.matches(obj):
                continue
            else:
                return

        raise NoInclusionRuleMet()

    def __validate_test_rules(self, obj):
        for rule in self.__test_erules:
            if rule.matches(obj):
                raise ExclusionRuleMet(rule)

        if not self.__test_irules:
            return

        for rule in self.__test_irules:
            if not rule.matches(obj):
                continue
            else:
                return

        raise NoInclusionRuleMet()

    def validate(self, obj):
        '''
        Rules are segregated as package, module and test rules (inclusion/exclusion).

        Following is the test selection process as per Arjuna rules:

            #. Package check: Specified using ip/ep or ir/er with "package operator operand" grammar.
                - if package for a test meets an exclusion rule, it is excluded.
                - if no inclusion rule is specified, it is included for module validation.
                - if an inclusion rule is met, it is selected for module validation.
                - if no inclusion rule is met, it is excluded.
            #. Module check: Specified using im/em or ir/er with "module operator operand" grammar.
                - if module for a test meets an exclusion rule, it is excluded.
                - if no inclusion rule is specified, it is included for test validation.
                - if an inclusion rule is met, it is selected for test validation.
                - if no inclusion rule is met, it is excluded.
            #. Test check: Specified using it/et or ir/er with any rule grammar except "package operator operand" and "module operator operand".
                - if a test meets an exclusion rule, it is excluded.
                - if no inclusion rule is specified, it is included in test group run.
                - if an inclusion rule is met, it is included in test group run.
                - if no inclusion rule is met, it is excluded from test group run.
        '''

        if not self.__frozen:
            self.__freeze()
            self.__frozen = True

        try:
            self.__validate_package_rules(obj)
        except (ExclusionRuleMet, NoInclusionRuleMet) as e:
            raise e
        else:
            try:
                self.__validate_module_rules(obj)
            except (ExclusionRuleMet, NoInclusionRuleMet) as e:
                raise e    
            else:
                self.__validate_test_rules(obj)

    def __str__(self):
        return str([str(r) for r in self.irules] + [str(r) for r in self.erules])
