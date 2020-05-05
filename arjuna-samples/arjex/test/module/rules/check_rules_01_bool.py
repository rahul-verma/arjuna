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
from arjuna.engine.selection.selector import Selector
from arjuna.core.constant import *

@test
def check_rule_creation_bool_pattern(request):
    selector = Selector()

    r = "unstable"
    selector.include(r)
    rule = selector.irules[0]
    print(rule)
    assert rule.__class__.__name__ == "BoolAttrPatternRule"
    assert rule.rule_str == r
    assert rule.container == "info"
    assert rule.target == "unstable"
    assert rule.condition == RuleConditionType.EQUAL
    assert rule.expression == True
    assert rule.checker.__name__ == 'are_equal'

    # Check NOT
    selector = Selector()
    r = "not unstable"
    selector.include(r)
    rule = selector.irules[0]
    print(rule)
    assert rule.__class__.__name__ == "BoolAttrPatternRule"
    assert rule.rule_str == r
    assert rule.container == "info"
    assert rule.target == "unstable"
    assert rule.condition == RuleConditionType.NOT_EQUAL
    assert rule.expression == True
    assert rule.checker.__name__ == 'are_not_equal'

@test
def check_rule_creation_prop_pattern(request):
    # Check boolean prop
    selector = Selector()
    r = "unstable is False"
    selector.include(r)
    rule = selector.irules[0]
    print(rule)
    assert rule.__class__.__name__ == "AttrPatternRule"
    assert rule.rule_str == r
    assert rule.container == "info"
    assert rule.target == "unstable"
    assert rule.condition == RuleConditionType.EQUAL
    assert rule.expression == False
    assert rule.checker.__name__ == 'are_equal'

    selector = Selector()
    r = "unstable not True"
    selector.include(r)
    rule = selector.irules[0]
    print(rule)
    assert rule.__class__.__name__ == "AttrPatternRule"
    assert rule.rule_str == r
    assert rule.container == "info"
    assert rule.target == "unstable"
    assert rule.condition == RuleConditionType.NOT_EQUAL
    assert rule.expression == True
    assert rule.checker.__name__ == 'are_not_equal'

    # Check boolean prop - value alternatives
    selector = Selector()
    r = "unstable is On"
    selector.include(r)
    rule = selector.irules[0]
    print(rule)
    assert rule.__class__.__name__ == "AttrPatternRule"
    assert rule.rule_str == r
    assert rule.container == "info"
    assert rule.target == "unstable"
    assert rule.condition == RuleConditionType.EQUAL
    assert rule.expression == True
    assert rule.checker.__name__ == 'are_equal'

    selector = Selector()
    r = "unstable is oFf"
    selector.include(r)
    rule = selector.irules[0]
    print(rule)
    assert rule.__class__.__name__ == "AttrPatternRule"
    assert rule.rule_str == r
    assert rule.container == "info"
    assert rule.target == "unstable"
    assert rule.condition == RuleConditionType.EQUAL
    assert rule.expression == False
    assert rule.checker.__name__ == 'are_equal'

    # Check boolean prop - value alternatives
    selector = Selector()
    r = "unstable is YeS"
    selector.include(r)
    rule = selector.irules[0]
    print(rule)
    assert rule.__class__.__name__ == "AttrPatternRule"
    assert rule.rule_str == r
    assert rule.container == "info"
    assert rule.target == "unstable"
    assert rule.condition == RuleConditionType.EQUAL
    assert rule.expression == True
    assert rule.checker.__name__ == 'are_equal'

    selector = Selector()
    r = "unstable is nO"
    selector.include(r)
    rule = selector.irules[0]
    print(rule)
    assert rule.__class__.__name__ == "AttrPatternRule"
    assert rule.rule_str == r
    assert rule.container == "info"
    assert rule.target == "unstable"
    assert rule.condition == RuleConditionType.EQUAL
    assert rule.expression == False
    assert rule.checker.__name__ == 'are_equal'

@test
def check_rule_creation_invalid(request):
    try:
        selector = Selector()
        r = "unstable is anything"
        selector.include(r)
    except InvalidSelectionRule:
        pass
    else:
        assert 1 == 2

    try:
        selector = Selector()
        r = "unstable < True"
        selector.include(r)
    except InvalidSelectionRule:
        pass
    else:
        assert 1 == 2


class Empty:
    pass

class Obj:
    def __init__(self):
        self.info = Empty()

@test
def check_rule_evaluation_boolean_pattern(request):
    selector = Selector()
    r = "unstable"
    selector.include(r)
    rule = selector.irules[0]
    print(rule)

    obj = Obj()
    assert rule.matches(obj) is False

    obj = Obj()
    obj.info.unstable = True
    assert rule.matches(obj) is True

    obj = Obj()
    obj.info.unstable = False
    assert rule.matches(obj) is False

    selector = Selector()
    r = "not unstable"
    selector.include(r)
    rule = selector.irules[0]
    print(rule)

    obj = Obj()
    assert rule.matches(obj) is True

    obj = Obj()
    obj.info.unstable = True
    assert rule.matches(obj) is False

    obj = Obj()
    obj.info.unstable = False
    assert rule.matches(obj) is True


@test
def check_rule_evaluation_prop_pattern(request):
    selector = Selector()
    r = "unstable is true"
    selector.include(r)
    rule = selector.irules[0]
    print(rule)

    obj = Obj()
    assert rule.matches(obj) is False

    obj = Obj()
    obj.info.unstable = True
    assert rule.matches(obj) is True

    obj = Obj()
    obj.info.unstable = False
    assert rule.matches(obj) is False

    selector = Selector()
    r = "unstable is false"
    selector.include(r)
    rule = selector.irules[0]
    print(rule)

    obj = Obj()
    assert rule.matches(obj) is True

    obj = Obj()
    obj.info.unstable = True
    assert rule.matches(obj) is False

    obj = Obj()
    obj.info.unstable = False
    assert rule.matches(obj) is True




