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
from .helpers import *

@test
def check_rule_creation_user_prop(request):
    r = "rating is 2"
    selector = Selector()    
    selector.include(r)
    rule = selector.irules[0]
    print(rule)
    assert rule.__class__.__name__ == "AttrPatternRule"
    assert rule.rule_str == r
    assert rule.container == "info"
    assert rule.target == "rating"
    assert rule.condition == RuleConditionType.EQUAL
    assert rule.expression == "2"
    assert rule.checker.__name__ == 'are_equal'


@test
def check_user_attr_prop_selection(request):
    rule = get_rule("rating is 2")
    obj = Obj()
    assert rule.matches(obj) is False

    obj = Obj()
    obj.info.rating = 3
    assert rule.matches(obj) is False

    rule = get_rule("rating > 2")
    obj = Obj()
    assert rule.matches(obj) is False

    obj = Obj()
    obj.info.rating = 3
    assert rule.matches(obj) is True

    rule = get_rule("rating ~= true")
    obj = Obj()
    assert rule.matches(obj) is False

    obj = Obj()
    obj.info.rating = True
    assert rule.matches(obj) is True


@test
def check_user_attr_bool_selection(request):
    rule = get_rule("complete")
    obj = Obj()
    assert rule.matches(obj) is False

    obj = Obj()
    obj.info.complete = True
    assert rule.matches(obj) is True

    obj = Obj()
    obj.info.complete = False
    assert rule.matches(obj) is False

    obj = Obj()
    obj.info.complete = "non_bool"  # Non empty string is True
    assert rule.matches(obj) is True

    obj = Obj()
    obj.info.complete = ""  # Empty string is True
    assert rule.matches(obj) is False


@test
def check_user_iterable_selection(request):
    rule = get_rule("with usertags abc,def")
    obj = Obj()
    assert rule.matches(obj) is False

    rule = get_rule("with usertags abc,def")
    obj = Obj()
    obj.info.usertags = None
    assert rule.matches(obj) is False

    rule = get_rule("with usertags abc,def")
    obj = Obj()
    obj.info.usertags = {'abc'}
    assert rule.matches(obj) is True

    rule = get_rule("with usertags abc,def")
    obj = Obj()
    obj.info.usertags = {'xyz'}
    assert rule.matches(obj) is False

    rule = get_rule("with usertags abc,def")
    obj = Obj()
    obj.info.usertags = {'xyz', 'def'}
    assert rule.matches(obj) is True

    rule = get_rule("with usertags abc,def")
    obj = Obj()
    obj.info.usertags = 'def'
    assert rule.matches(obj) is True

    rule = get_rule("with usertags 123")
    obj = Obj()
    obj.info.usertags = 123
    assert rule.matches(obj) is True

    rule = get_rule("with usertags def")
    obj = Obj()
    obj.info.usertags = ['xyz', 'def', 'ghi']
    assert rule.matches(obj) is True

