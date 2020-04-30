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