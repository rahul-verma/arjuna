# This file is a part of Arjuna
# Copyright 2015-2020 Rahul Verma

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

from .rule import *

class Selector:

    def __init__(self):
        self.__rules = list()

    def add_rule(self, rule_str):
        self.__rules.append(self.__build_rule(rule_str))

    def __build_rule(self, rule_str):
        pattern = None
        try:
            return BooleanPropPatternRule.from_str(rule_str)
        except RulePatternDoesNotMatchError:
            try:
                return TagsPatternRule.from_str(rule_str)
            except RulePatternDoesNotMatchError:
                try:
                    return InfoPatternRule.from_str(rule_str)
                except RulePatternDoesNotMatchError:
                    raise Exception("Rule is invalid: " + rule_str)

    @property
    def rules(self):
        return self.__rules

    def __str__(self):
        return str([str(r) for r in self.__rules])
