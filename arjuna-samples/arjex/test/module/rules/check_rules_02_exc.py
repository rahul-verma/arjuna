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
def check_creation_exclude_rule(request):
    selector = Selector()

    r = "unstable"
    selector.exclude(r)
    rule = selector.erules[0]
    print(rule)
    assert rule.__class__.__name__ == "BooleanPropPatternRule"
    assert rule.rule_str == r
    assert rule.container == "info"
    assert rule.target == "unstable"
    assert rule.condition == RuleConditionType.EQUAL
    assert rule.expression == True
    assert rule.checker.__name__ == 'are_equal'

    # Check NOT
    selector = Selector()
    r = "not unstable"
    selector.exclude(r)
    rule = selector.erules[0]
    print(rule)
    assert rule.__class__.__name__ == "BooleanPropPatternRule"
    assert rule.rule_str == r
    assert rule.container == "info"
    assert rule.target == "unstable"
    assert rule.condition == RuleConditionType.NOT_EQUAL
    assert rule.expression == True
    assert rule.checker.__name__ == 'are_not_equal'

class Empty:
    pass

class Obj:
    def __init__(self):
        self.info = Empty()

@test
def check_evaluation_exclude_rule(request):
    selector = Selector()
    r = "unstable"
    selector.exclude(r)
    rule = selector.erules[0]
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
    selector.exclude(r)
    rule = selector.erules[0]
    print(rule)

    obj = Obj()
    assert rule.matches(obj) is True

    obj = Obj()
    obj.info.unstable = True
    assert rule.matches(obj) is False

    obj = Obj()
    obj.info.unstable = False
    assert rule.matches(obj) is True

