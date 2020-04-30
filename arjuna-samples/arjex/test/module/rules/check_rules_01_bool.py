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

from arjuna import *
from arjuna.engine.selection.rules.rule import Rules
from arjuna.core.constant import *

@test
def check_rule_creation_bool_pattern(request):
    rules = Rules()

    r = "unstable"
    rules.from_str(r)
    rule = rules.rules[0]
    print(rule)
    assert rule.__class__.__name__ == "BooleanPropPatternRule"
    assert rule.rule_str == r
    assert rule.container == "properties"
    assert rule.target == "unstable"
    assert rule.condition == RuleConditionType.EQUAL
    assert rule.expression == True
    assert rule.checker.__name__ == 'are_equal'

    # Check NOT
    rules = Rules()
    r = "not unstable"
    rules.from_str(r)
    rule = rules.rules[0]
    print(rule)
    assert rule.__class__.__name__ == "BooleanPropPatternRule"
    assert rule.rule_str == r
    assert rule.container == "properties"
    assert rule.target == "unstable"
    assert rule.condition == RuleConditionType.NOT_EQUAL
    assert rule.expression == True
    assert rule.checker.__name__ == 'are_not_equal'

@test
def check_rule_creation_prop_pattern(request):
    # Check boolean prop
    rules = Rules()
    r = "unstable is False"
    rules.from_str(r)
    rule = rules.rules[0]
    print(rule)
    assert rule.__class__.__name__ == "PropertyPatternRule"
    assert rule.rule_str == r
    assert rule.container == "properties"
    assert rule.target == "unstable"
    assert rule.condition == RuleConditionType.EQUAL
    assert rule.expression == False
    assert rule.checker.__name__ == 'are_equal'

    rules = Rules()
    r = "unstable not True"
    rules.from_str(r)
    rule = rules.rules[0]
    print(rule)
    assert rule.__class__.__name__ == "PropertyPatternRule"
    assert rule.rule_str == r
    assert rule.container == "properties"
    assert rule.target == "unstable"
    assert rule.condition == RuleConditionType.NOT_EQUAL
    assert rule.expression == True
    assert rule.checker.__name__ == 'are_not_equal'

    # Check boolean prop - value alternatives
    rules = Rules()
    r = "unstable is On"
    rules.from_str(r)
    rule = rules.rules[0]
    print(rule)
    assert rule.__class__.__name__ == "PropertyPatternRule"
    assert rule.rule_str == r
    assert rule.container == "properties"
    assert rule.target == "unstable"
    assert rule.condition == RuleConditionType.EQUAL
    assert rule.expression == True
    assert rule.checker.__name__ == 'are_equal'

    rules = Rules()
    r = "unstable is oFf"
    rules.from_str(r)
    rule = rules.rules[0]
    print(rule)
    assert rule.__class__.__name__ == "PropertyPatternRule"
    assert rule.rule_str == r
    assert rule.container == "properties"
    assert rule.target == "unstable"
    assert rule.condition == RuleConditionType.EQUAL
    assert rule.expression == False
    assert rule.checker.__name__ == 'are_equal'

    # Check boolean prop - value alternatives
    rules = Rules()
    r = "unstable is YeS"
    rules.from_str(r)
    rule = rules.rules[0]
    print(rule)
    assert rule.__class__.__name__ == "PropertyPatternRule"
    assert rule.rule_str == r
    assert rule.container == "properties"
    assert rule.target == "unstable"
    assert rule.condition == RuleConditionType.EQUAL
    assert rule.expression == True
    assert rule.checker.__name__ == 'are_equal'

    rules = Rules()
    r = "unstable is nO"
    rules.from_str(r)
    rule = rules.rules[0]
    print(rule)
    assert rule.__class__.__name__ == "PropertyPatternRule"
    assert rule.rule_str == r
    assert rule.container == "properties"
    assert rule.target == "unstable"
    assert rule.condition == RuleConditionType.EQUAL
    assert rule.expression == False
    assert rule.checker.__name__ == 'are_equal'

@test
def check_rule_creation_invalid(request):
    try:
        rules = Rules()
        r = "unstable is anything"
        rules.from_str(r)
    except InvalidSelectionRule:
        pass
    else:
        assert 1 == 2

    try:
        rules = Rules()
        r = "unstable < True"
        rules.from_str(r)
    except InvalidSelectionRule:
        pass
    else:
        assert 1 == 2


class Empty:
    pass

class Obj:
    def __init__(self):
        self.properties = Empty()

@test
def check_rule_evaluation_boolean_pattern(request):
    rules = Rules()
    r = "unstable"
    rules.from_str(r)
    rule = rules.rules[0]
    print(rule)

    obj = Obj()
    assert rule.matches(obj) is False

    obj = Obj()
    obj.properties.unstable = True
    assert rule.matches(obj) is True

    obj = Obj()
    obj.properties.unstable = False
    assert rule.matches(obj) is False

    rules = Rules()
    r = "not unstable"
    rules.from_str(r)
    rule = rules.rules[0]
    print(rule)

    obj = Obj()
    assert rule.matches(obj) is True

    obj = Obj()
    obj.properties.unstable = True
    assert rule.matches(obj) is False

    obj = Obj()
    obj.properties.unstable = False
    assert rule.matches(obj) is True


@test
def check_rule_evaluation_prop_pattern(request):
    rules = Rules()
    r = "unstable is true"
    rules.from_str(r)
    rule = rules.rules[0]
    print(rule)

    obj = Obj()
    assert rule.matches(obj) is False

    obj = Obj()
    obj.properties.unstable = True
    assert rule.matches(obj) is True

    obj = Obj()
    obj.properties.unstable = False
    assert rule.matches(obj) is False

    rules = Rules()
    r = "unstable is false"
    rules.from_str(r)
    rule = rules.rules[0]
    print(rule)

    obj = Obj()
    assert rule.matches(obj) is True

    obj = Obj()
    obj.properties.unstable = True
    assert rule.matches(obj) is False

    obj = Obj()
    obj.properties.unstable = False
    assert rule.matches(obj) is True




