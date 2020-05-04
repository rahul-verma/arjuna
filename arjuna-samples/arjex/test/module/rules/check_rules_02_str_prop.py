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
def check_rule_creation_str_prop_simple(request):
    
    r = "author is Rahul Verma"
    selector = Selector()    
    selector.include(r)
    rule = selector.irules[0]
    print(rule)
    assert rule.__class__.__name__ == "InfoPatternRule"
    assert rule.rule_str == r
    assert rule.container == "info"
    assert rule.target == "author"
    assert rule.condition == RuleConditionType.EQUAL
    assert rule.expression == "Rahul Verma"
    assert rule.checker.__name__ == 'are_equal'

    r = "author eq Rahul Verma"
    selector = Selector()    
    selector.include(r)
    rule = selector.irules[0]
    print(rule)
    assert rule.__class__.__name__ == "InfoPatternRule"
    assert rule.rule_str == r
    assert rule.container == "info"
    assert rule.target == "author"
    assert rule.condition == RuleConditionType.EQUAL
    assert rule.expression == "Rahul Verma"
    assert rule.checker.__name__ == 'are_equal'

    r = "author = Rahul Verma"
    selector = Selector()    
    selector.include(r)
    rule = selector.irules[0]
    print(rule)
    assert rule.__class__.__name__ == "InfoPatternRule"
    assert rule.rule_str == r
    assert rule.container == "info"
    assert rule.target == "author"
    assert rule.condition == RuleConditionType.EQUAL
    assert rule.expression == "Rahul Verma"
    assert rule.checker.__name__ == 'are_equal'

    r = "author == Rahul Verma"
    selector = Selector()    
    selector.include(r)
    rule = selector.irules[0]
    print(rule)
    assert rule.__class__.__name__ == "InfoPatternRule"
    assert rule.rule_str == r
    assert rule.container == "info"
    assert rule.target == "author"
    assert rule.condition == RuleConditionType.EQUAL
    assert rule.expression == "Rahul Verma"
    assert rule.checker.__name__ == 'are_equal'

    r = "author != Rahul Verma"
    selector = Selector()    
    selector.include(r)
    rule = selector.irules[0]
    print(rule)
    assert rule.__class__.__name__ == "InfoPatternRule"
    assert rule.rule_str == r
    assert rule.container == "info"
    assert rule.target == "author"
    assert rule.condition == RuleConditionType.NOT_EQUAL
    assert rule.expression == "Rahul Verma"
    assert rule.checker.__name__ == 'are_not_equal'

    "author not Rahul Verma"
    selector = Selector()    
    selector.include(r)
    rule = selector.irules[0]
    print(rule)
    assert rule.__class__.__name__ == "InfoPatternRule"
    assert rule.rule_str == r
    assert rule.container == "info"
    assert rule.target == "author"
    assert rule.condition == RuleConditionType.NOT_EQUAL
    assert rule.expression == "Rahul Verma"
    assert rule.checker.__name__ == 'are_not_equal'

    "author ne Rahul Verma"
    selector = Selector()    
    selector.include(r)
    rule = selector.irules[0]
    print(rule)
    assert rule.__class__.__name__ == "InfoPatternRule"
    assert rule.rule_str == r
    assert rule.container == "info"
    assert rule.target == "author"
    assert rule.condition == RuleConditionType.NOT_EQUAL
    assert rule.expression == "Rahul Verma"
    assert rule.checker.__name__ == 'are_not_equal'

    r = "author matches Rahul VERMA"
    selector = Selector()    
    selector.include(r)
    rule = selector.irules[0]
    print(rule)
    assert rule.__class__.__name__ == "InfoPatternRule"
    assert rule.rule_str == r
    assert rule.container == "info"
    assert rule.target == "author"
    assert rule.condition == RuleConditionType.MATCHES
    assert rule.expression == "Rahul VERMA"
    assert rule.checker.__name__ == 'match_with_ignore_case'

    r = "author ~= Rahul VERMA"
    selector = Selector()    
    selector.include(r)
    rule = selector.irules[0]
    print(rule)
    assert rule.__class__.__name__ == "InfoPatternRule"
    assert rule.rule_str == r
    assert rule.container == "info"
    assert rule.target == "author"
    assert rule.condition == RuleConditionType.MATCHES
    assert rule.expression == "Rahul VERMA"
    assert rule.checker.__name__ == 'match_with_ignore_case'

    r = "author *= RaHuL"
    selector = Selector()    
    selector.include(r)
    rule = selector.irules[0]
    print(rule)
    assert rule.__class__.__name__ == "InfoPatternRule"
    assert rule.rule_str == r
    assert rule.container == "info"
    assert rule.target == "author"
    assert rule.condition == RuleConditionType.PARTIALLY_MATCHES
    assert rule.expression == "RaHuL"
    assert rule.checker.__name__ == 'partially_match_with_ignore_case'

class Empty:
    pass

class Obj:
    def __init__(self):
        self.info = Empty()

@test
def check_str_selection(request):
    r = "author is Rahul Verma"
    selector = Selector()    
    selector.include(r)
    rule = selector.irules[0]
    print(rule)

    obj = Obj()
    assert rule.matches(obj) is False

    obj = Obj()
    obj.author = None
    assert rule.matches(obj) is False

    obj = Obj()
    obj.info.author = 'Rahul Verma'
    assert rule.matches(obj) is True

    obj = Obj()
    obj.info.author = 'rahul Verma'
    assert rule.matches(obj) is False

    r = "author != Rahul Verma"
    selector = Selector()    
    selector.include(r)
    rule = selector.irules[0]
    print(rule)

    obj = Obj()
    assert rule.matches(obj) is True

    obj = Obj()
    obj.author = None
    assert rule.matches(obj) is True

    obj = Obj()
    obj.info.author = 'Rahul Verma'
    assert rule.matches(obj) is False

    obj = Obj()
    obj.info.author = 'rahul Verma'
    assert rule.matches(obj) is True

    r = "author ~= Rahul VERMA"
    selector = Selector()    
    selector.include(r)
    rule = selector.irules[0]
    print(rule)

    obj = Obj()
    assert rule.matches(obj) is False

    obj = Obj()
    obj.author = None
    assert rule.matches(obj) is False

    obj = Obj()
    obj.info.author = 'rahul Verma'
    assert rule.matches(obj) is True

    obj = Obj()
    obj.info.author = 'Arjuna'
    assert rule.matches(obj) is False

    r = "author *= RaHuL"
    selector = Selector()    
    selector.include(r)
    rule = selector.irules[0]
    print(rule)

    obj = Obj()
    assert rule.matches(obj) is False

    obj = Obj()
    obj.author = None
    assert rule.matches(obj) is False

    obj = Obj()
    obj.info.author = 'X RAHul Y'
    assert rule.matches(obj) is True

    obj = Obj()
    obj.info.author = 'Rah'
    assert rule.matches(obj) is False


