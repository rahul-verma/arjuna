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
from arjuna.engine.selection.rules.rule import Selector
from arjuna.core.constant import *

# Priority is contextually interpreted and not as a usual integer.
# Priorty 1 in testing is higher than 2.

@test
def check_rule_creation_priority(request):
    r = "priority is 2"
    selector = Selector()    
    selector.add_rule(r)
    rule = selector.rules[0]
    print(rule)
    assert rule.__class__.__name__ == "PropertyPatternRule"
    assert rule.rule_str == r
    assert rule.container == "properties"
    assert rule.target == "priority"
    assert rule.condition == RuleConditionType.EQUAL
    assert rule.expression == 2
    assert rule.checker.__name__ == 'are_equal'

    r = "priority eq 2"
    selector = Selector()    
    selector.add_rule(r)
    rule = selector.rules[0]
    print(rule)
    assert rule.__class__.__name__ == "PropertyPatternRule"
    assert rule.rule_str == r
    assert rule.container == "properties"
    assert rule.target == "priority"
    assert rule.condition == RuleConditionType.EQUAL
    assert rule.expression == 2
    assert rule.checker.__name__ == 'are_equal'

    r = "priority = 2"
    selector = Selector()    
    selector.add_rule(r)
    rule = selector.rules[0]
    print(rule)
    assert rule.__class__.__name__ == "PropertyPatternRule"
    assert rule.rule_str == r
    assert rule.container == "properties"
    assert rule.target == "priority"
    assert rule.condition == RuleConditionType.EQUAL
    assert rule.expression == 2
    assert rule.checker.__name__ == 'are_equal'

    r = "priority == 2"
    selector = Selector()    
    selector.add_rule(r)
    rule = selector.rules[0]
    print(rule)
    assert rule.__class__.__name__ == "PropertyPatternRule"
    assert rule.rule_str == r
    assert rule.container == "properties"
    assert rule.target == "priority"
    assert rule.condition == RuleConditionType.EQUAL
    assert rule.expression == 2
    assert rule.checker.__name__ == 'are_equal'

    r = "priority not 2"
    selector = Selector()    
    selector.add_rule(r)
    rule = selector.rules[0]
    print(rule)
    assert rule.__class__.__name__ == "PropertyPatternRule"
    assert rule.rule_str == r
    assert rule.container == "properties"
    assert rule.target == "priority"
    assert rule.condition == RuleConditionType.NOT_EQUAL
    assert rule.expression == 2
    assert rule.checker.__name__ == 'are_not_equal'

    r = "priority != 2"
    selector = Selector()    
    selector.add_rule(r)
    rule = selector.rules[0]
    print(rule)
    assert rule.__class__.__name__ == "PropertyPatternRule"
    assert rule.rule_str == r
    assert rule.container == "properties"
    assert rule.target == "priority"
    assert rule.condition == RuleConditionType.NOT_EQUAL
    assert rule.expression == 2
    assert rule.checker.__name__ == 'are_not_equal'

    r = "priority ne 2"
    selector = Selector()    
    selector.add_rule(r)
    rule = selector.rules[0]
    print(rule)
    assert rule.__class__.__name__ == "PropertyPatternRule"
    assert rule.rule_str == r
    assert rule.container == "properties"
    assert rule.target == "priority"
    assert rule.condition == RuleConditionType.NOT_EQUAL
    assert rule.expression == 2
    assert rule.checker.__name__ == 'are_not_equal'

    r = "priority lt 3"
    selector = Selector()    
    selector.add_rule(r)
    rule = selector.rules[0]
    print(rule)
    assert rule.__class__.__name__ == "PropertyPatternRule"
    assert rule.rule_str == r
    assert rule.container == "properties"
    assert rule.target == "priority"
    assert rule.condition == RuleConditionType.GREATER_THAN
    assert rule.expression == 3
    assert rule.checker.__name__ == 'greater_than'

    r = "priority < 3"
    selector = Selector()    
    selector.add_rule(r)
    rule = selector.rules[0]
    print(rule)
    assert rule.__class__.__name__ == "PropertyPatternRule"
    assert rule.rule_str == r
    assert rule.container == "properties"
    assert rule.target == "priority"
    assert rule.condition == RuleConditionType.GREATER_THAN
    assert rule.expression == 3
    assert rule.checker.__name__ == 'greater_than'

    r = "priority gt 1"
    selector = Selector()    
    selector.add_rule(r)
    rule = selector.rules[0]
    print(rule)
    assert rule.__class__.__name__ == "PropertyPatternRule"
    assert rule.rule_str == r
    assert rule.container == "properties"
    assert rule.target == "priority"
    assert rule.condition == RuleConditionType.LESS_THAN
    assert rule.expression == 1
    assert rule.checker.__name__ == 'less_than'

    r = "priority > 1"
    selector = Selector()    
    selector.add_rule(r)
    rule = selector.rules[0]
    print(rule)
    assert rule.__class__.__name__ == "PropertyPatternRule"
    assert rule.rule_str == r
    assert rule.container == "properties"
    assert rule.target == "priority"
    assert rule.condition == RuleConditionType.LESS_THAN
    assert rule.expression == 1
    assert rule.checker.__name__ == 'less_than'

    r = "priority le 2"
    selector = Selector()    
    selector.add_rule(r)
    rule = selector.rules[0]
    print(rule)
    assert rule.__class__.__name__ == "PropertyPatternRule"
    assert rule.rule_str == r
    assert rule.container == "properties"
    assert rule.target == "priority"
    assert rule.condition == RuleConditionType.GREATER_OR_EQUAL
    assert rule.expression == 2
    assert rule.checker.__name__ == 'greater_or_equal'

    r = "priority <= 2"
    selector = Selector()    
    selector.add_rule(r)
    rule = selector.rules[0]
    print(rule)
    assert rule.__class__.__name__ == "PropertyPatternRule"
    assert rule.rule_str == r
    assert rule.container == "properties"
    assert rule.target == "priority"
    assert rule.condition == RuleConditionType.GREATER_OR_EQUAL
    assert rule.expression == 2
    assert rule.checker.__name__ == 'greater_or_equal'

    r = "priority ge 2"
    selector = Selector()    
    selector.add_rule(r)
    rule = selector.rules[0]
    print(rule)
    assert rule.__class__.__name__ == "PropertyPatternRule"
    assert rule.rule_str == r
    assert rule.container == "properties"
    assert rule.target == "priority"
    assert rule.condition == RuleConditionType.LESS_OR_EQUAL
    assert rule.expression == 2
    assert rule.checker.__name__ == 'less_or_equal'

    r = "priority >= 2"
    selector = Selector()    
    selector.add_rule(r)
    rule = selector.rules[0]
    print(rule)
    assert rule.__class__.__name__ == "PropertyPatternRule"
    assert rule.rule_str == r
    assert rule.container == "properties"
    assert rule.target == "priority"
    assert rule.condition == RuleConditionType.LESS_OR_EQUAL
    assert rule.expression == 2
    assert rule.checker.__name__ == 'less_or_equal'


class Empty:
    pass

class Obj:
    def __init__(self):
        self.properties = Empty()

@test
def check_priority_selection(request):
    r = "priority is 2"
    selector = Selector()    
    selector.add_rule(r)
    rule = selector.rules[0]
    print(rule)

    obj = Obj()
    assert rule.matches(obj) is False

    obj = Obj()
    obj.properties.priority = 2
    assert rule.matches(obj) is True

    obj = Obj()
    obj.properties.priority = 1
    assert rule.matches(obj) is False

    r = "priority is 5"
    selector = Selector()    
    selector.add_rule(r)
    rule = selector.rules[0]
    print(rule)

    obj = Obj()
    assert rule.matches(obj) is True

    r = "priority not 2"
    selector = Selector()    
    selector.add_rule(r)
    rule = selector.rules[0]
    print(rule)

    obj = Obj()
    assert rule.matches(obj) is True

    obj = Obj()
    obj.properties.priority = 3
    assert rule.matches(obj) is True

    obj = Obj()
    obj.properties.priority = 2
    assert rule.matches(obj) is False

    r = "priority lt 3"
    selector = Selector()    
    selector.add_rule(r)
    rule = selector.rules[0]
    print(rule)

    obj = Obj()
    assert rule.matches(obj) is True

    obj = Obj()
    obj.properties.priority = 4
    assert rule.matches(obj) is True

    obj = Obj()
    obj.properties.priority = 2
    assert rule.matches(obj) is False

    r = "priority gt 2"
    selector = Selector()    
    selector.add_rule(r)
    rule = selector.rules[0]
    print(rule)

    obj = Obj()
    assert rule.matches(obj) is False

    obj = Obj()
    obj.properties.priority = 1
    assert rule.matches(obj) is True

    obj = Obj()
    obj.properties.priority = 3
    assert rule.matches(obj) is False

    r = "priority le 2"
    selector = Selector()    
    selector.add_rule(r)
    rule = selector.rules[0]
    print(rule)

    obj = Obj()
    assert rule.matches(obj) is True

    obj = Obj()
    obj.properties.priority = 2
    assert rule.matches(obj) is True

    obj = Obj()
    obj.properties.priority = 1
    assert rule.matches(obj) is False

    r = "priority ge 2"
    selector = Selector()    
    selector.add_rule(r)
    rule = selector.rules[0]
    print(rule)

    obj = Obj()
    assert rule.matches(obj) is False

    obj = Obj()
    obj.properties.priority = 2
    assert rule.matches(obj) is True

    obj = Obj()
    obj.properties.priority = 3
    assert rule.matches(obj) is False











