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

from arjuna import *
from arjuna.engine.selection.selector import Selector
from arjuna.core.constant import *
from .helpers import *

@test
def check_rule_creation_str_prop_comp(request):
    r = "app_version is 2.1.1"
    selector = Selector()    
    selector.include(r)
    rule = selector.irules[0]
    print(rule)
    assert rule.__class__.__name__ == "AttrPatternRule"
    assert rule.rule_str == r
    assert rule.container == "info"
    assert rule.target == "app_version"
    assert rule.condition == RuleConditionType.EQUAL
    assert rule.expression == "2.1.1"
    assert rule.checker.__name__ == 'are_equal'

    r = "app_version eq 2.1.1"
    selector = Selector()    
    selector.include(r)
    rule = selector.irules[0]
    print(rule)
    assert rule.__class__.__name__ == "AttrPatternRule"
    assert rule.rule_str == r
    assert rule.container == "info"
    assert rule.target == "app_version"
    assert rule.condition == RuleConditionType.EQUAL
    assert rule.expression == "2.1.1"
    assert rule.checker.__name__ == 'are_equal'

    r = "app_version = 2.1.1"
    selector = Selector()    
    selector.include(r)
    rule = selector.irules[0]
    print(rule)
    assert rule.__class__.__name__ == "AttrPatternRule"
    assert rule.rule_str == r
    assert rule.container == "info"
    assert rule.target == "app_version"
    assert rule.condition == RuleConditionType.EQUAL
    assert rule.expression == "2.1.1"
    assert rule.checker.__name__ == 'are_equal'

    r = "app_version == 2.1.1"
    selector = Selector()    
    selector.include(r)
    rule = selector.irules[0]
    print(rule)
    assert rule.__class__.__name__ == "AttrPatternRule"
    assert rule.rule_str == r
    assert rule.container == "info"
    assert rule.target == "app_version"
    assert rule.condition == RuleConditionType.EQUAL
    assert rule.expression == "2.1.1"
    assert rule.checker.__name__ == 'are_equal'

    r = "app_version not 2.1.2"
    selector = Selector()    
    selector.include(r)
    rule = selector.irules[0]
    print(rule)
    assert rule.__class__.__name__ == "AttrPatternRule"
    assert rule.rule_str == r
    assert rule.container == "info"
    assert rule.target == "app_version"
    assert rule.condition == RuleConditionType.NOT_EQUAL
    assert rule.expression == "2.1.2"
    assert rule.checker.__name__ == 'are_not_equal'

    r = "app_version != 2.1.2"
    selector = Selector()    
    selector.include(r)
    rule = selector.irules[0]
    print(rule)
    assert rule.__class__.__name__ == "AttrPatternRule"
    assert rule.rule_str == r
    assert rule.container == "info"
    assert rule.target == "app_version"
    assert rule.condition == RuleConditionType.NOT_EQUAL
    assert rule.expression == "2.1.2"
    assert rule.checker.__name__ == 'are_not_equal'

    r = "app_version ne 2.1.2"
    selector = Selector()    
    selector.include(r)
    rule = selector.irules[0]
    print(rule)
    assert rule.__class__.__name__ == "AttrPatternRule"
    assert rule.rule_str == r
    assert rule.container == "info"
    assert rule.target == "app_version"
    assert rule.condition == RuleConditionType.NOT_EQUAL
    assert rule.expression == "2.1.2"
    assert rule.checker.__name__ == 'are_not_equal'

    r = "app_version lt 2.1.2"
    selector = Selector()    
    selector.include(r)
    rule = selector.irules[0]
    print(rule)
    assert rule.__class__.__name__ == "AttrPatternRule"
    assert rule.rule_str == r
    assert rule.container == "info"
    assert rule.target == "app_version"
    assert rule.condition == RuleConditionType.LESS_THAN
    assert rule.expression == "2.1.2"
    assert rule.checker.__name__ == 'less_than'

    r = "app_version < 2.1.2"
    selector = Selector()    
    selector.include(r)
    rule = selector.irules[0]
    print(rule)
    assert rule.__class__.__name__ == "AttrPatternRule"
    assert rule.rule_str == r
    assert rule.container == "info"
    assert rule.target == "app_version"
    assert rule.condition == RuleConditionType.LESS_THAN
    assert rule.expression == "2.1.2"
    assert rule.checker.__name__ == 'less_than'

    r = "app_version gt 2.1.0"
    selector = Selector()    
    selector.include(r)
    rule = selector.irules[0]
    print(rule)
    assert rule.__class__.__name__ == "AttrPatternRule"
    assert rule.rule_str == r
    assert rule.container == "info"
    assert rule.target == "app_version"
    assert rule.condition == RuleConditionType.GREATER_THAN
    assert rule.expression == "2.1.0"
    assert rule.checker.__name__ == 'greater_than'

    r = "app_version > 2.1.0"
    selector = Selector()    
    selector.include(r)
    rule = selector.irules[0]
    print(rule)
    assert rule.__class__.__name__ == "AttrPatternRule"
    assert rule.rule_str == r
    assert rule.container == "info"
    assert rule.target == "app_version"
    assert rule.condition == RuleConditionType.GREATER_THAN
    assert rule.expression == "2.1.0"
    assert rule.checker.__name__ == 'greater_than'

    r = "app_version le 2.1.1"
    selector = Selector()    
    selector.include(r)
    rule = selector.irules[0]
    print(rule)
    assert rule.__class__.__name__ == "AttrPatternRule"
    assert rule.rule_str == r
    assert rule.container == "info"
    assert rule.target == "app_version"
    assert rule.condition == RuleConditionType.LESS_OR_EQUAL
    assert rule.expression == "2.1.1"
    assert rule.checker.__name__ == 'less_or_equal'

    r = "app_version <= 2.1.1"
    selector = Selector()    
    selector.include(r)
    rule = selector.irules[0]
    print(rule)
    assert rule.__class__.__name__ == "AttrPatternRule"
    assert rule.rule_str == r
    assert rule.container == "info"
    assert rule.target == "app_version"
    assert rule.condition == RuleConditionType.LESS_OR_EQUAL
    assert rule.expression == "2.1.1"
    assert rule.checker.__name__ == 'less_or_equal'

    r = "app_version ge 2.1.1"
    selector = Selector()    
    selector.include(r)
    rule = selector.irules[0]
    print(rule)
    assert rule.__class__.__name__ == "AttrPatternRule"
    assert rule.rule_str == r
    assert rule.container == "info"
    assert rule.target == "app_version"
    assert rule.condition == RuleConditionType.GREATER_OR_EQUAL
    assert rule.expression == "2.1.1"
    assert rule.checker.__name__ == 'greater_or_equal'

    r = "app_version >= 2.1.1"
    selector = Selector()    
    selector.include(r)
    rule = selector.irules[0]
    print(rule)
    assert rule.__class__.__name__ == "AttrPatternRule"
    assert rule.rule_str == r
    assert rule.container == "info"
    assert rule.target == "app_version"
    assert rule.condition == RuleConditionType.GREATER_OR_EQUAL
    assert rule.expression == "2.1.1"
    assert rule.checker.__name__ == 'greater_or_equal'


@test
def check_str_comp_selection(request):
    rule = get_rule("app_version is 2.1.1")
    obj = Obj()
    assert rule.matches(obj) is False

    obj = Obj()
    obj.info.app_version = "2.1.1"
    assert rule.matches(obj) is True

    obj = Obj()
    obj.info.app_version = "2.1.2"
    assert rule.matches(obj) is False

    rule = get_rule("app_version not 2.1.2")
    obj = Obj()
    assert rule.matches(obj) is True

    obj = Obj()
    obj.info.app_version = "2.1.1"
    assert rule.matches(obj) is True

    obj = Obj()
    obj.info.app_version = "2.1.2"
    assert rule.matches(obj) is False

    rule = get_rule("app_version lt 2.1.2")
    obj = Obj()
    assert rule.matches(obj) is True

    obj = Obj()
    obj.info.app_version = "2.1.3"
    assert rule.matches(obj) is False

    obj = Obj()
    obj.info.app_version = "2.1.2"
    assert rule.matches(obj) is False

    rule = get_rule("app_version gt 2.1.2")
    obj = Obj()
    assert rule.matches(obj) is False

    obj = Obj()
    obj.info.app_version = "2.1.3"
    assert rule.matches(obj) is True

    obj = Obj()
    obj.info.app_version = "2.1.2"
    assert rule.matches(obj) is False

    rule = get_rule("app_version le 2.1.2")
    obj = Obj()
    assert rule.matches(obj) is True

    obj = Obj()
    obj.info.app_version = "2.1.1"
    assert rule.matches(obj) is True

    obj = Obj()
    obj.info.app_version = "2.1.2"
    assert rule.matches(obj) is True

    obj = Obj()
    obj.info.app_version = "2.1.3"
    assert rule.matches(obj) is False

    rule = get_rule("app_version ge 2.1.2")
    obj = Obj()
    assert rule.matches(obj) is False

    obj = Obj()
    obj.info.app_version = "2.1.3"
    assert rule.matches(obj) is True

    obj = Obj()
    obj.info.app_version = "2.1.2"
    assert rule.matches(obj) is True

    obj = Obj()
    obj.info.app_version = "2.1.1"
    assert rule.matches(obj) is False




