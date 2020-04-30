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
def check_rule_creation_bool(request):
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

    rules = Rules()
    r = "unstable is 1"
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
    r = "unstable is 0"
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

@test
def check_rule_creation_str_prop_simple(request):
    
    r = "author is Rahul Verma"
    rules = Rules()    
    rules.from_str(r)
    rule = rules.rules[0]
    print(rule)
    assert rule.__class__.__name__ == "PropertyPatternRule"
    assert rule.rule_str == r
    assert rule.container == "properties"
    assert rule.target == "author"
    assert rule.condition == RuleConditionType.EQUAL
    assert rule.expression == "Rahul Verma"
    assert rule.checker.__name__ == 'are_equal'

    r = "author eq Rahul Verma"
    rules = Rules()    
    rules.from_str(r)
    rule = rules.rules[0]
    print(rule)
    assert rule.__class__.__name__ == "PropertyPatternRule"
    assert rule.rule_str == r
    assert rule.container == "properties"
    assert rule.target == "author"
    assert rule.condition == RuleConditionType.EQUAL
    assert rule.expression == "Rahul Verma"
    assert rule.checker.__name__ == 'are_equal'

    r = "author = Rahul Verma"
    rules = Rules()    
    rules.from_str(r)
    rule = rules.rules[0]
    print(rule)
    assert rule.__class__.__name__ == "PropertyPatternRule"
    assert rule.rule_str == r
    assert rule.container == "properties"
    assert rule.target == "author"
    assert rule.condition == RuleConditionType.EQUAL
    assert rule.expression == "Rahul Verma"
    assert rule.checker.__name__ == 'are_equal'

    r = "author == Rahul Verma"
    rules = Rules()    
    rules.from_str(r)
    rule = rules.rules[0]
    print(rule)
    assert rule.__class__.__name__ == "PropertyPatternRule"
    assert rule.rule_str == r
    assert rule.container == "properties"
    assert rule.target == "author"
    assert rule.condition == RuleConditionType.EQUAL
    assert rule.expression == "Rahul Verma"
    assert rule.checker.__name__ == 'are_equal'

    r = "author != Rahul Verma"
    rules = Rules()    
    rules.from_str(r)
    rule = rules.rules[0]
    print(rule)
    assert rule.__class__.__name__ == "PropertyPatternRule"
    assert rule.rule_str == r
    assert rule.container == "properties"
    assert rule.target == "author"
    assert rule.condition == RuleConditionType.NOT_EQUAL
    assert rule.expression == "Rahul Verma"
    assert rule.checker.__name__ == 'are_not_equal'

    "author not Rahul Verma"
    rules = Rules()    
    rules.from_str(r)
    rule = rules.rules[0]
    print(rule)
    assert rule.__class__.__name__ == "PropertyPatternRule"
    assert rule.rule_str == r
    assert rule.container == "properties"
    assert rule.target == "author"
    assert rule.condition == RuleConditionType.NOT_EQUAL
    assert rule.expression == "Rahul Verma"
    assert rule.checker.__name__ == 'are_not_equal'

    "author ne Rahul Verma"
    rules = Rules()    
    rules.from_str(r)
    rule = rules.rules[0]
    print(rule)
    assert rule.__class__.__name__ == "PropertyPatternRule"
    assert rule.rule_str == r
    assert rule.container == "properties"
    assert rule.target == "author"
    assert rule.condition == RuleConditionType.NOT_EQUAL
    assert rule.expression == "Rahul Verma"
    assert rule.checker.__name__ == 'are_not_equal'

    r = "author matches Rahul VERMA"
    rules = Rules()    
    rules.from_str(r)
    rule = rules.rules[0]
    print(rule)
    assert rule.__class__.__name__ == "PropertyPatternRule"
    assert rule.rule_str == r
    assert rule.container == "properties"
    assert rule.target == "author"
    assert rule.condition == RuleConditionType.MATCHES
    assert rule.expression == "Rahul VERMA"
    assert rule.checker.__name__ == 'match_with_ignore_case'

    r = "author ~= Rahul VERMA"
    rules = Rules()    
    rules.from_str(r)
    rule = rules.rules[0]
    print(rule)
    assert rule.__class__.__name__ == "PropertyPatternRule"
    assert rule.rule_str == r
    assert rule.container == "properties"
    assert rule.target == "author"
    assert rule.condition == RuleConditionType.MATCHES
    assert rule.expression == "Rahul VERMA"
    assert rule.checker.__name__ == 'match_with_ignore_case'

    r = "author *= RaHuL"
    rules = Rules()    
    rules.from_str(r)
    rule = rules.rules[0]
    print(rule)
    assert rule.__class__.__name__ == "PropertyPatternRule"
    assert rule.rule_str == r
    assert rule.container == "properties"
    assert rule.target == "author"
    assert rule.condition == RuleConditionType.PARTIALLY_MATCHES
    assert rule.expression == "RaHuL"
    assert rule.checker.__name__ == 'partially_match_with_ignore_case'

@test
def check_rule_creation_int_prop(request):
    r = "priority is 2"
    rules = Rules()    
    rules.from_str(r)
    rule = rules.rules[0]
    print(rule)
    assert rule.__class__.__name__ == "PropertyPatternRule"
    assert rule.rule_str == r
    assert rule.container == "properties"
    assert rule.target == "priority"
    assert rule.condition == RuleConditionType.EQUAL
    assert rule.expression == 2
    assert rule.checker.__name__ == 'are_equal'

    r = "priority eq 2"
    rules = Rules()    
    rules.from_str(r)
    rule = rules.rules[0]
    print(rule)
    assert rule.__class__.__name__ == "PropertyPatternRule"
    assert rule.rule_str == r
    assert rule.container == "properties"
    assert rule.target == "priority"
    assert rule.condition == RuleConditionType.EQUAL
    assert rule.expression == 2
    assert rule.checker.__name__ == 'are_equal'

    r = "priority = 2"
    rules = Rules()    
    rules.from_str(r)
    rule = rules.rules[0]
    print(rule)
    assert rule.__class__.__name__ == "PropertyPatternRule"
    assert rule.rule_str == r
    assert rule.container == "properties"
    assert rule.target == "priority"
    assert rule.condition == RuleConditionType.EQUAL
    assert rule.expression == 2
    assert rule.checker.__name__ == 'are_equal'

    r = "priority == 2"
    rules = Rules()    
    rules.from_str(r)
    rule = rules.rules[0]
    print(rule)
    assert rule.__class__.__name__ == "PropertyPatternRule"
    assert rule.rule_str == r
    assert rule.container == "properties"
    assert rule.target == "priority"
    assert rule.condition == RuleConditionType.EQUAL
    assert rule.expression == 2
    assert rule.checker.__name__ == 'are_equal'

    r = "priority not 2"
    rules = Rules()    
    rules.from_str(r)
    rule = rules.rules[0]
    print(rule)
    assert rule.__class__.__name__ == "PropertyPatternRule"
    assert rule.rule_str == r
    assert rule.container == "properties"
    assert rule.target == "priority"
    assert rule.condition == RuleConditionType.NOT_EQUAL
    assert rule.expression == 2
    assert rule.checker.__name__ == 'are_not_equal'

    r = "priority != 2"
    rules = Rules()    
    rules.from_str(r)
    rule = rules.rules[0]
    print(rule)
    assert rule.__class__.__name__ == "PropertyPatternRule"
    assert rule.rule_str == r
    assert rule.container == "properties"
    assert rule.target == "priority"
    assert rule.condition == RuleConditionType.NOT_EQUAL
    assert rule.expression == 2
    assert rule.checker.__name__ == 'are_not_equal'

    r = "priority ne 2"
    rules = Rules()    
    rules.from_str(r)
    rule = rules.rules[0]
    print(rule)
    assert rule.__class__.__name__ == "PropertyPatternRule"
    assert rule.rule_str == r
    assert rule.container == "properties"
    assert rule.target == "priority"
    assert rule.condition == RuleConditionType.NOT_EQUAL
    assert rule.expression == 2
    assert rule.checker.__name__ == 'are_not_equal'

    r = "priority lt 3"
    rules = Rules()    
    rules.from_str(r)
    rule = rules.rules[0]
    print(rule)
    assert rule.__class__.__name__ == "PropertyPatternRule"
    assert rule.rule_str == r
    assert rule.container == "properties"
    assert rule.target == "priority"
    assert rule.condition == RuleConditionType.LESS_THAN
    assert rule.expression == 3
    assert rule.checker.__name__ == 'less_than'

    r = "priority < 3"
    rules = Rules()    
    rules.from_str(r)
    rule = rules.rules[0]
    print(rule)
    assert rule.__class__.__name__ == "PropertyPatternRule"
    assert rule.rule_str == r
    assert rule.container == "properties"
    assert rule.target == "priority"
    assert rule.condition == RuleConditionType.LESS_THAN
    assert rule.expression == 3
    assert rule.checker.__name__ == 'less_than'

    r = "priority gt 1"
    rules = Rules()    
    rules.from_str(r)
    rule = rules.rules[0]
    print(rule)
    assert rule.__class__.__name__ == "PropertyPatternRule"
    assert rule.rule_str == r
    assert rule.container == "properties"
    assert rule.target == "priority"
    assert rule.condition == RuleConditionType.GREATER_THAN
    assert rule.expression == 1
    assert rule.checker.__name__ == 'greater_than'

    r = "priority > 1"
    rules = Rules()    
    rules.from_str(r)
    rule = rules.rules[0]
    print(rule)
    assert rule.__class__.__name__ == "PropertyPatternRule"
    assert rule.rule_str == r
    assert rule.container == "properties"
    assert rule.target == "priority"
    assert rule.condition == RuleConditionType.GREATER_THAN
    assert rule.expression == 1
    assert rule.checker.__name__ == 'greater_than'

    r = "priority le 2"
    rules = Rules()    
    rules.from_str(r)
    rule = rules.rules[0]
    print(rule)
    assert rule.__class__.__name__ == "PropertyPatternRule"
    assert rule.rule_str == r
    assert rule.container == "properties"
    assert rule.target == "priority"
    assert rule.condition == RuleConditionType.LESS_OR_EQUAL
    assert rule.expression == 2
    assert rule.checker.__name__ == 'less_or_equal'

    r = "priority <= 2"
    rules = Rules()    
    rules.from_str(r)
    rule = rules.rules[0]
    print(rule)
    assert rule.__class__.__name__ == "PropertyPatternRule"
    assert rule.rule_str == r
    assert rule.container == "properties"
    assert rule.target == "priority"
    assert rule.condition == RuleConditionType.LESS_OR_EQUAL
    assert rule.expression == 2
    assert rule.checker.__name__ == 'less_or_equal'

    r = "priority ge 2"
    rules = Rules()    
    rules.from_str(r)
    rule = rules.rules[0]
    print(rule)
    assert rule.__class__.__name__ == "PropertyPatternRule"
    assert rule.rule_str == r
    assert rule.container == "properties"
    assert rule.target == "priority"
    assert rule.condition == RuleConditionType.GREATER_OR_EQUAL
    assert rule.expression == 2
    assert rule.checker.__name__ == 'greater_or_equal'

    r = "priority >= 2"
    rules = Rules()    
    rules.from_str(r)
    rule = rules.rules[0]
    print(rule)
    assert rule.__class__.__name__ == "PropertyPatternRule"
    assert rule.rule_str == r
    assert rule.container == "properties"
    assert rule.target == "priority"
    assert rule.condition == RuleConditionType.GREATER_OR_EQUAL
    assert rule.expression == 2
    assert rule.checker.__name__ == 'greater_or_equal'


@test
def check_rule_creation_str_prop_comp(request):
    r = "app_version is 2.1.1"
    rules = Rules()    
    rules.from_str(r)
    rule = rules.rules[0]
    print(rule)
    assert rule.__class__.__name__ == "PropertyPatternRule"
    assert rule.rule_str == r
    assert rule.container == "properties"
    assert rule.target == "app_version"
    assert rule.condition == RuleConditionType.EQUAL
    assert rule.expression == "2.1.1"
    assert rule.checker.__name__ == 'are_equal'

    r = "app_version eq 2.1.1"
    rules = Rules()    
    rules.from_str(r)
    rule = rules.rules[0]
    print(rule)
    assert rule.__class__.__name__ == "PropertyPatternRule"
    assert rule.rule_str == r
    assert rule.container == "properties"
    assert rule.target == "app_version"
    assert rule.condition == RuleConditionType.EQUAL
    assert rule.expression == "2.1.1"
    assert rule.checker.__name__ == 'are_equal'

    r = "app_version = 2.1.1"
    rules = Rules()    
    rules.from_str(r)
    rule = rules.rules[0]
    print(rule)
    assert rule.__class__.__name__ == "PropertyPatternRule"
    assert rule.rule_str == r
    assert rule.container == "properties"
    assert rule.target == "app_version"
    assert rule.condition == RuleConditionType.EQUAL
    assert rule.expression == "2.1.1"
    assert rule.checker.__name__ == 'are_equal'

    r = "app_version == 2.1.1"
    rules = Rules()    
    rules.from_str(r)
    rule = rules.rules[0]
    print(rule)
    assert rule.__class__.__name__ == "PropertyPatternRule"
    assert rule.rule_str == r
    assert rule.container == "properties"
    assert rule.target == "app_version"
    assert rule.condition == RuleConditionType.EQUAL
    assert rule.expression == "2.1.1"
    assert rule.checker.__name__ == 'are_equal'

    r = "app_version not 2.1.2"
    rules = Rules()    
    rules.from_str(r)
    rule = rules.rules[0]
    print(rule)
    assert rule.__class__.__name__ == "PropertyPatternRule"
    assert rule.rule_str == r
    assert rule.container == "properties"
    assert rule.target == "app_version"
    assert rule.condition == RuleConditionType.NOT_EQUAL
    assert rule.expression == "2.1.2"
    assert rule.checker.__name__ == 'are_not_equal'

    r = "app_version != 2.1.2"
    rules = Rules()    
    rules.from_str(r)
    rule = rules.rules[0]
    print(rule)
    assert rule.__class__.__name__ == "PropertyPatternRule"
    assert rule.rule_str == r
    assert rule.container == "properties"
    assert rule.target == "app_version"
    assert rule.condition == RuleConditionType.NOT_EQUAL
    assert rule.expression == "2.1.2"
    assert rule.checker.__name__ == 'are_not_equal'

    r = "app_version ne 2.1.2"
    rules = Rules()    
    rules.from_str(r)
    rule = rules.rules[0]
    print(rule)
    assert rule.__class__.__name__ == "PropertyPatternRule"
    assert rule.rule_str == r
    assert rule.container == "properties"
    assert rule.target == "app_version"
    assert rule.condition == RuleConditionType.NOT_EQUAL
    assert rule.expression == "2.1.2"
    assert rule.checker.__name__ == 'are_not_equal'

    r = "app_version lt 2.1.2"
    rules = Rules()    
    rules.from_str(r)
    rule = rules.rules[0]
    print(rule)
    assert rule.__class__.__name__ == "PropertyPatternRule"
    assert rule.rule_str == r
    assert rule.container == "properties"
    assert rule.target == "app_version"
    assert rule.condition == RuleConditionType.LESS_THAN
    assert rule.expression == "2.1.2"
    assert rule.checker.__name__ == 'less_than'

    r = "app_version < 2.1.2"
    rules = Rules()    
    rules.from_str(r)
    rule = rules.rules[0]
    print(rule)
    assert rule.__class__.__name__ == "PropertyPatternRule"
    assert rule.rule_str == r
    assert rule.container == "properties"
    assert rule.target == "app_version"
    assert rule.condition == RuleConditionType.LESS_THAN
    assert rule.expression == "2.1.2"
    assert rule.checker.__name__ == 'less_than'

    r = "app_version gt 2.1.0"
    rules = Rules()    
    rules.from_str(r)
    rule = rules.rules[0]
    print(rule)
    assert rule.__class__.__name__ == "PropertyPatternRule"
    assert rule.rule_str == r
    assert rule.container == "properties"
    assert rule.target == "app_version"
    assert rule.condition == RuleConditionType.GREATER_THAN
    assert rule.expression == "2.1.0"
    assert rule.checker.__name__ == 'greater_than'

    r = "app_version > 2.1.0"
    rules = Rules()    
    rules.from_str(r)
    rule = rules.rules[0]
    print(rule)
    assert rule.__class__.__name__ == "PropertyPatternRule"
    assert rule.rule_str == r
    assert rule.container == "properties"
    assert rule.target == "app_version"
    assert rule.condition == RuleConditionType.GREATER_THAN
    assert rule.expression == "2.1.0"
    assert rule.checker.__name__ == 'greater_than'

    r = "app_version le 2.1.1"
    rules = Rules()    
    rules.from_str(r)
    rule = rules.rules[0]
    print(rule)
    assert rule.__class__.__name__ == "PropertyPatternRule"
    assert rule.rule_str == r
    assert rule.container == "properties"
    assert rule.target == "app_version"
    assert rule.condition == RuleConditionType.LESS_OR_EQUAL
    assert rule.expression == "2.1.1"
    assert rule.checker.__name__ == 'less_or_equal'

    r = "app_version <= 2.1.1"
    rules = Rules()    
    rules.from_str(r)
    rule = rules.rules[0]
    print(rule)
    assert rule.__class__.__name__ == "PropertyPatternRule"
    assert rule.rule_str == r
    assert rule.container == "properties"
    assert rule.target == "app_version"
    assert rule.condition == RuleConditionType.LESS_OR_EQUAL
    assert rule.expression == "2.1.1"
    assert rule.checker.__name__ == 'less_or_equal'

    r = "app_version ge 2.1.1"
    rules = Rules()    
    rules.from_str(r)
    rule = rules.rules[0]
    print(rule)
    assert rule.__class__.__name__ == "PropertyPatternRule"
    assert rule.rule_str == r
    assert rule.container == "properties"
    assert rule.target == "app_version"
    assert rule.condition == RuleConditionType.GREATER_OR_EQUAL
    assert rule.expression == "2.1.1"
    assert rule.checker.__name__ == 'greater_or_equal'

    r = "app_version >= 2.1.1"
    rules = Rules()    
    rules.from_str(r)
    rule = rules.rules[0]
    print(rule)
    assert rule.__class__.__name__ == "PropertyPatternRule"
    assert rule.rule_str == r
    assert rule.container == "properties"
    assert rule.target == "app_version"
    assert rule.condition == RuleConditionType.GREATER_OR_EQUAL
    assert rule.expression == "2.1.1"
    assert rule.checker.__name__ == 'greater_or_equal'


@test
def check_rule_creation_tags(request):
    r = "with tags chrome, firefox"
    rules = Rules()    
    rules.from_str(r)
    rule = rules.rules[0]
    print(rule)
    assert rule.__class__.__name__ == "TagsPatternRule"
    assert rule.rule_str == r
    assert rule.container == "tags"
    assert rule.target == set({'chrome', 'firefox'})
    assert rule.condition == RuleConditionType.HAS_INTERSECTION
    assert rule.expression == set({'chrome', 'firefox'})
    assert rule.checker.__name__ == 'has_intersection'

    r = "with tag chrome"
    rules = Rules()    
    rules.from_str(r)
    rule = rules.rules[0]
    print(rule)
    assert rule.__class__.__name__ == "TagsPatternRule"
    assert rule.rule_str == r
    assert rule.container == "tags"
    assert rule.target == set({'chrome'})
    assert rule.condition == RuleConditionType.HAS_INTERSECTION
    assert rule.expression == set({'chrome'})
    assert rule.checker.__name__ == 'has_intersection'

    r = "withall tags chrome, abc"
    rules = Rules()    
    rules.from_str(r)
    rule = rules.rules[0]
    print(rule)
    assert rule.__class__.__name__ == "TagsPatternRule"
    assert rule.rule_str == r
    assert rule.container == "tags"
    assert rule.target == set({'chrome', 'abc'})
    assert rule.condition == RuleConditionType.IS_SUBSET
    assert rule.expression == set({'chrome', 'abc'})
    assert rule.checker.__name__ == 'is_subset'

    r = "without tags chrome, abc"
    rules = Rules()    
    rules.from_str(r)
    rule = rules.rules[0]
    print(rule)
    assert rule.__class__.__name__ == "TagsPatternRule"
    assert rule.rule_str == r
    assert rule.container == "tags"
    assert rule.target == set({'chrome', 'abc'})
    assert rule.condition == RuleConditionType.NO_INTERSECTION
    assert rule.expression == set({'chrome', 'abc'})
    assert rule.checker.__name__ == 'has_no_intersection'

    r = "without tag chrome"
    rules = Rules()    
    rules.from_str(r)
    rule = rules.rules[0]
    print(rule)
    assert rule.__class__.__name__ == "TagsPatternRule"
    assert rule.rule_str == r
    assert rule.container == "tags"
    assert rule.target == set({'chrome'})
    assert rule.condition == RuleConditionType.NO_INTERSECTION
    assert rule.expression == set({'chrome'})
    assert rule.checker.__name__ == 'has_no_intersection'

    r = "with bugs b1,b2"
    rules = Rules()    
    rules.from_str(r)
    rule = rules.rules[0]
    print(rule)
    assert rule.__class__.__name__ == "TagsPatternRule"
    assert rule.rule_str == r
    assert rule.container == "bugs"
    assert rule.target == set({'b1', 'b2'})
    assert rule.condition == RuleConditionType.HAS_INTERSECTION
    assert rule.expression == set({'b1', 'b2'})
    assert rule.checker.__name__ == 'has_intersection'

    r = "with bug b1"
    rules = Rules()    
    rules.from_str(r)
    rule = rules.rules[0]
    print(rule)
    assert rule.__class__.__name__ == "TagsPatternRule"
    assert rule.rule_str == r
    assert rule.container == "bugs"
    assert rule.target == set({'b1'})
    assert rule.condition == RuleConditionType.HAS_INTERSECTION
    assert rule.expression == set({'b1'})
    assert rule.checker.__name__ == 'has_intersection'

    r = "withall bugs b1,abc"
    rules = Rules()    
    rules.from_str(r)
    rule = rules.rules[0]
    print(rule)
    assert rule.__class__.__name__ == "TagsPatternRule"
    assert rule.rule_str == r
    assert rule.container == "bugs"
    assert rule.target == set({'b1', 'abc'})
    assert rule.condition == RuleConditionType.IS_SUBSET
    assert rule.expression == set({'b1', 'abc'})
    assert rule.checker.__name__ == 'is_subset'

    r = "without bugs b1,abc"
    rules = Rules()    
    rules.from_str(r)
    rule = rules.rules[0]
    print(rule)
    assert rule.__class__.__name__ == "TagsPatternRule"
    assert rule.rule_str == r
    assert rule.container == "bugs"
    assert rule.target == set({'b1', 'abc'})
    assert rule.condition == RuleConditionType.NO_INTERSECTION
    assert rule.expression == set({'b1', 'abc'})
    assert rule.checker.__name__ == 'has_no_intersection'

    r = "without bug b1"
    rules = Rules()    
    rules.from_str(r)
    rule = rules.rules[0]
    print(rule)
    assert rule.__class__.__name__ == "TagsPatternRule"
    assert rule.rule_str == r
    assert rule.container == "bugs"
    assert rule.target == set({'b1'})
    assert rule.condition == RuleConditionType.NO_INTERSECTION
    assert rule.expression == set({'b1'})
    assert rule.checker.__name__ == 'has_no_intersection'

    r = "with envs env1, env2"
    rules = Rules()    
    rules.from_str(r)
    rule = rules.rules[0]
    print(rule)
    assert rule.__class__.__name__ == "TagsPatternRule"
    assert rule.rule_str == r
    assert rule.container == "envs"
    assert rule.target == set({'env1', 'env2'})
    assert rule.condition == RuleConditionType.HAS_INTERSECTION
    assert rule.expression == set({'env1', 'env2'})
    assert rule.checker.__name__ == 'has_intersection'

    r = "with env env1"
    rules = Rules()    
    rules.from_str(r)
    rule = rules.rules[0]
    print(rule)
    assert rule.__class__.__name__ == "TagsPatternRule"
    assert rule.rule_str == r
    assert rule.container == "envs"
    assert rule.target == set({'env1'})
    assert rule.condition == RuleConditionType.HAS_INTERSECTION
    assert rule.expression == set({'env1'})
    assert rule.checker.__name__ == 'has_intersection'

    r = "withall envs env1, env2"
    rules = Rules()    
    rules.from_str(r)
    rule = rules.rules[0]
    print(rule)
    assert rule.__class__.__name__ == "TagsPatternRule"
    assert rule.rule_str == r
    assert rule.container == "envs"
    assert rule.target == set({'env1', 'env2'})
    assert rule.condition == RuleConditionType.IS_SUBSET
    assert rule.expression == set({'env1', 'env2'})
    assert rule.checker.__name__ == 'is_subset'

    r = "without envs env1, env2"
    rules = Rules()    
    rules.from_str(r)
    rule = rules.rules[0]
    print(rule)
    assert rule.__class__.__name__ == "TagsPatternRule"
    assert rule.rule_str == r
    assert rule.container == "envs"
    assert rule.target == set({'env1', 'env2'})
    assert rule.condition == RuleConditionType.NO_INTERSECTION
    assert rule.expression == set({'env1', 'env2'})
    assert rule.checker.__name__ == 'has_no_intersection'

    r = "without env env1"
    rules = Rules()    
    rules.from_str(r)
    rule = rules.rules[0]
    print(rule)
    assert rule.__class__.__name__ == "TagsPatternRule"
    assert rule.rule_str == r
    assert rule.container == "envs"
    assert rule.target == set({'env1'})
    assert rule.condition == RuleConditionType.NO_INTERSECTION
    assert rule.expression == set({'env1'})
    assert rule.checker.__name__ == 'has_no_intersection'