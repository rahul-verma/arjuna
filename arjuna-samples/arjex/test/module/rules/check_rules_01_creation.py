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
    rules.include(r)
    irule = rules.irules[0]
    print(irule)
    assert irule.__class__.__name__ == "BooleanPropPatternRule"
    assert irule.rule_str == r
    assert irule.nature == RuleNature.INCLUDE
    assert irule.container == "properties"
    assert irule.target == "unstable"
    assert irule.condition == RuleConditionType.EQUAL
    assert irule.expression == True
    assert irule.checker.__name__ == 'are_equal'

    r = "unstable"
    rules.exclude(r)
    erule = rules.erules[0]
    print(erule)
    assert erule.__class__.__name__ == "BooleanPropPatternRule"
    assert erule.rule_str == r
    assert erule.nature == RuleNature.EXCLUDE
    assert erule.container == "properties"
    assert erule.target == "unstable"
    assert erule.condition == RuleConditionType.EQUAL
    assert erule.expression == True
    assert irule.checker.__name__ == 'are_equal'

    # Check NOT
    rules = Rules()
    r = "not unstable"
    rules.include(r)
    irule = rules.irules[0]
    print(irule)
    assert irule.__class__.__name__ == "BooleanPropPatternRule"
    assert irule.rule_str == r
    assert irule.nature == RuleNature.INCLUDE
    assert irule.container == "properties"
    assert irule.target == "unstable"
    assert irule.condition == RuleConditionType.NOT_EQUAL
    assert irule.expression == True
    assert irule.checker.__name__ == 'are_not_equal'

    # Check boolean prop
    rules = Rules()
    r = "unstable is False"
    rules.include(r)
    irule = rules.irules[0]
    print(irule)
    assert irule.__class__.__name__ == "PropertyPatternRule"
    assert irule.rule_str == r
    assert irule.nature == RuleNature.INCLUDE
    assert irule.container == "properties"
    assert irule.target == "unstable"
    assert irule.condition == RuleConditionType.EQUAL
    assert irule.expression == False
    assert irule.checker.__name__ == 'are_equal'

    rules = Rules()
    r = "unstable not True"
    rules.include(r)
    irule = rules.irules[0]
    print(irule)
    assert irule.__class__.__name__ == "PropertyPatternRule"
    assert irule.rule_str == r
    assert irule.nature == RuleNature.INCLUDE
    assert irule.container == "properties"
    assert irule.target == "unstable"
    assert irule.condition == RuleConditionType.NOT_EQUAL
    assert irule.expression == True
    assert irule.checker.__name__ == 'are_not_equal'

    # Check boolean prop - value alternatives
    rules = Rules()
    r = "unstable is On"
    rules.include(r)
    irule = rules.irules[0]
    print(irule)
    assert irule.__class__.__name__ == "PropertyPatternRule"
    assert irule.rule_str == r
    assert irule.nature == RuleNature.INCLUDE
    assert irule.container == "properties"
    assert irule.target == "unstable"
    assert irule.condition == RuleConditionType.EQUAL
    assert irule.expression == True
    assert irule.checker.__name__ == 'are_equal'

    rules = Rules()
    r = "unstable is oFf"
    rules.include(r)
    irule = rules.irules[0]
    print(irule)
    assert irule.__class__.__name__ == "PropertyPatternRule"
    assert irule.rule_str == r
    assert irule.nature == RuleNature.INCLUDE
    assert irule.container == "properties"
    assert irule.target == "unstable"
    assert irule.condition == RuleConditionType.EQUAL
    assert irule.expression == False
    assert irule.checker.__name__ == 'are_equal'

    # Check boolean prop - value alternatives
    rules = Rules()
    r = "unstable is YeS"
    rules.include(r)
    irule = rules.irules[0]
    print(irule)
    assert irule.__class__.__name__ == "PropertyPatternRule"
    assert irule.rule_str == r
    assert irule.nature == RuleNature.INCLUDE
    assert irule.container == "properties"
    assert irule.target == "unstable"
    assert irule.condition == RuleConditionType.EQUAL
    assert irule.expression == True
    assert irule.checker.__name__ == 'are_equal'

    rules = Rules()
    r = "unstable is nO"
    rules.include(r)
    irule = rules.irules[0]
    print(irule)
    assert irule.__class__.__name__ == "PropertyPatternRule"
    assert irule.rule_str == r
    assert irule.nature == RuleNature.INCLUDE
    assert irule.container == "properties"
    assert irule.target == "unstable"
    assert irule.condition == RuleConditionType.EQUAL
    assert irule.expression == False
    assert irule.checker.__name__ == 'are_equal'

    rules = Rules()
    r = "unstable is 1"
    rules.include(r)
    irule = rules.irules[0]
    print(irule)
    assert irule.__class__.__name__ == "PropertyPatternRule"
    assert irule.rule_str == r
    assert irule.nature == RuleNature.INCLUDE
    assert irule.container == "properties"
    assert irule.target == "unstable"
    assert irule.condition == RuleConditionType.EQUAL
    assert irule.expression == True
    assert irule.checker.__name__ == 'are_equal'

    rules = Rules()
    r = "unstable is 0"
    rules.include(r)
    irule = rules.irules[0]
    print(irule)
    assert irule.__class__.__name__ == "PropertyPatternRule"
    assert irule.rule_str == r
    assert irule.nature == RuleNature.INCLUDE
    assert irule.container == "properties"
    assert irule.target == "unstable"
    assert irule.condition == RuleConditionType.EQUAL
    assert irule.expression == False
    assert irule.checker.__name__ == 'are_equal'

    try:
        rules = Rules()
        r = "unstable is anything"
        rules.include(r)
    except InvalidSelectionRule:
        pass
    else:
        assert 1 == 2

    try:
        rules = Rules()
        r = "unstable < True"
        rules.include(r)
    except InvalidSelectionRule:
        pass
    else:
        assert 1 == 2

@test
def check_rule_creation_str_prop_simple(request):
    
    r = "author is Rahul Verma"
    rules = Rules()    
    rules.include(r)
    irule = rules.irules[0]
    print(irule)
    assert irule.__class__.__name__ == "PropertyPatternRule"
    assert irule.rule_str == r
    assert irule.nature == RuleNature.INCLUDE
    assert irule.container == "properties"
    assert irule.target == "author"
    assert irule.condition == RuleConditionType.EQUAL
    assert irule.expression == "Rahul Verma"
    assert irule.checker.__name__ == 'are_equal'

    r = "author eq Rahul Verma"
    rules = Rules()    
    rules.include(r)
    irule = rules.irules[0]
    print(irule)
    assert irule.__class__.__name__ == "PropertyPatternRule"
    assert irule.rule_str == r
    assert irule.nature == RuleNature.INCLUDE
    assert irule.container == "properties"
    assert irule.target == "author"
    assert irule.condition == RuleConditionType.EQUAL
    assert irule.expression == "Rahul Verma"
    assert irule.checker.__name__ == 'are_equal'

    r = "author = Rahul Verma"
    rules = Rules()    
    rules.include(r)
    irule = rules.irules[0]
    print(irule)
    assert irule.__class__.__name__ == "PropertyPatternRule"
    assert irule.rule_str == r
    assert irule.nature == RuleNature.INCLUDE
    assert irule.container == "properties"
    assert irule.target == "author"
    assert irule.condition == RuleConditionType.EQUAL
    assert irule.expression == "Rahul Verma"
    assert irule.checker.__name__ == 'are_equal'

    r = "author == Rahul Verma"
    rules = Rules()    
    rules.include(r)
    irule = rules.irules[0]
    print(irule)
    assert irule.__class__.__name__ == "PropertyPatternRule"
    assert irule.rule_str == r
    assert irule.nature == RuleNature.INCLUDE
    assert irule.container == "properties"
    assert irule.target == "author"
    assert irule.condition == RuleConditionType.EQUAL
    assert irule.expression == "Rahul Verma"
    assert irule.checker.__name__ == 'are_equal'

    r = "author != Rahul Verma"
    rules = Rules()    
    rules.include(r)
    irule = rules.irules[0]
    print(irule)
    assert irule.__class__.__name__ == "PropertyPatternRule"
    assert irule.rule_str == r
    assert irule.nature == RuleNature.INCLUDE
    assert irule.container == "properties"
    assert irule.target == "author"
    assert irule.condition == RuleConditionType.NOT_EQUAL
    assert irule.expression == "Rahul Verma"
    assert irule.checker.__name__ == 'are_not_equal'

    "author not Rahul Verma"
    rules = Rules()    
    rules.include(r)
    irule = rules.irules[0]
    print(irule)
    assert irule.__class__.__name__ == "PropertyPatternRule"
    assert irule.rule_str == r
    assert irule.nature == RuleNature.INCLUDE
    assert irule.container == "properties"
    assert irule.target == "author"
    assert irule.condition == RuleConditionType.NOT_EQUAL
    assert irule.expression == "Rahul Verma"
    assert irule.checker.__name__ == 'are_not_equal'

    "author ne Rahul Verma"
    rules = Rules()    
    rules.include(r)
    irule = rules.irules[0]
    print(irule)
    assert irule.__class__.__name__ == "PropertyPatternRule"
    assert irule.rule_str == r
    assert irule.nature == RuleNature.INCLUDE
    assert irule.container == "properties"
    assert irule.target == "author"
    assert irule.condition == RuleConditionType.NOT_EQUAL
    assert irule.expression == "Rahul Verma"
    assert irule.checker.__name__ == 'are_not_equal'

    r = "author matches Rahul VERMA"
    rules = Rules()    
    rules.include(r)
    irule = rules.irules[0]
    print(irule)
    assert irule.__class__.__name__ == "PropertyPatternRule"
    assert irule.rule_str == r
    assert irule.nature == RuleNature.INCLUDE
    assert irule.container == "properties"
    assert irule.target == "author"
    assert irule.condition == RuleConditionType.MATCHES
    assert irule.expression == "Rahul VERMA"
    assert irule.checker.__name__ == 'match_with_ignore_case'

    r = "author ~= Rahul VERMA"
    rules = Rules()    
    rules.include(r)
    irule = rules.irules[0]
    print(irule)
    assert irule.__class__.__name__ == "PropertyPatternRule"
    assert irule.rule_str == r
    assert irule.nature == RuleNature.INCLUDE
    assert irule.container == "properties"
    assert irule.target == "author"
    assert irule.condition == RuleConditionType.MATCHES
    assert irule.expression == "Rahul VERMA"
    assert irule.checker.__name__ == 'match_with_ignore_case'

    r = "author *= RaHuL"
    rules = Rules()    
    rules.include(r)
    irule = rules.irules[0]
    print(irule)
    assert irule.__class__.__name__ == "PropertyPatternRule"
    assert irule.rule_str == r
    assert irule.nature == RuleNature.INCLUDE
    assert irule.container == "properties"
    assert irule.target == "author"
    assert irule.condition == RuleConditionType.PARTIALLY_MATCHES
    assert irule.expression == "RaHuL"
    assert irule.checker.__name__ == 'partially_match_with_ignore_case'

@test
def check_rule_creation_int_prop(request):
    r = "priority is 2"
    rules = Rules()    
    rules.include(r)
    irule = rules.irules[0]
    print(irule)
    assert irule.__class__.__name__ == "PropertyPatternRule"
    assert irule.rule_str == r
    assert irule.nature == RuleNature.INCLUDE
    assert irule.container == "properties"
    assert irule.target == "priority"
    assert irule.condition == RuleConditionType.EQUAL
    assert irule.expression == 2
    assert irule.checker.__name__ == 'are_equal'

    r = "priority eq 2"
    rules = Rules()    
    rules.include(r)
    irule = rules.irules[0]
    print(irule)
    assert irule.__class__.__name__ == "PropertyPatternRule"
    assert irule.rule_str == r
    assert irule.nature == RuleNature.INCLUDE
    assert irule.container == "properties"
    assert irule.target == "priority"
    assert irule.condition == RuleConditionType.EQUAL
    assert irule.expression == 2
    assert irule.checker.__name__ == 'are_equal'

    r = "priority = 2"
    rules = Rules()    
    rules.include(r)
    irule = rules.irules[0]
    print(irule)
    assert irule.__class__.__name__ == "PropertyPatternRule"
    assert irule.rule_str == r
    assert irule.nature == RuleNature.INCLUDE
    assert irule.container == "properties"
    assert irule.target == "priority"
    assert irule.condition == RuleConditionType.EQUAL
    assert irule.expression == 2
    assert irule.checker.__name__ == 'are_equal'

    r = "priority == 2"
    rules = Rules()    
    rules.include(r)
    irule = rules.irules[0]
    print(irule)
    assert irule.__class__.__name__ == "PropertyPatternRule"
    assert irule.rule_str == r
    assert irule.nature == RuleNature.INCLUDE
    assert irule.container == "properties"
    assert irule.target == "priority"
    assert irule.condition == RuleConditionType.EQUAL
    assert irule.expression == 2
    assert irule.checker.__name__ == 'are_equal'

    r = "priority not 2"
    rules = Rules()    
    rules.include(r)
    irule = rules.irules[0]
    print(irule)
    assert irule.__class__.__name__ == "PropertyPatternRule"
    assert irule.rule_str == r
    assert irule.nature == RuleNature.INCLUDE
    assert irule.container == "properties"
    assert irule.target == "priority"
    assert irule.condition == RuleConditionType.NOT_EQUAL
    assert irule.expression == 2
    assert irule.checker.__name__ == 'are_not_equal'

    r = "priority != 2"
    rules = Rules()    
    rules.include(r)
    irule = rules.irules[0]
    print(irule)
    assert irule.__class__.__name__ == "PropertyPatternRule"
    assert irule.rule_str == r
    assert irule.nature == RuleNature.INCLUDE
    assert irule.container == "properties"
    assert irule.target == "priority"
    assert irule.condition == RuleConditionType.NOT_EQUAL
    assert irule.expression == 2
    assert irule.checker.__name__ == 'are_not_equal'

    r = "priority ne 2"
    rules = Rules()    
    rules.include(r)
    irule = rules.irules[0]
    print(irule)
    assert irule.__class__.__name__ == "PropertyPatternRule"
    assert irule.rule_str == r
    assert irule.nature == RuleNature.INCLUDE
    assert irule.container == "properties"
    assert irule.target == "priority"
    assert irule.condition == RuleConditionType.NOT_EQUAL
    assert irule.expression == 2
    assert irule.checker.__name__ == 'are_not_equal'

    r = "priority lt 3"
    rules = Rules()    
    rules.include(r)
    irule = rules.irules[0]
    print(irule)
    assert irule.__class__.__name__ == "PropertyPatternRule"
    assert irule.rule_str == r
    assert irule.nature == RuleNature.INCLUDE
    assert irule.container == "properties"
    assert irule.target == "priority"
    assert irule.condition == RuleConditionType.LESS_THAN
    assert irule.expression == 3
    assert irule.checker.__name__ == 'less_than'

    r = "priority < 3"
    rules = Rules()    
    rules.include(r)
    irule = rules.irules[0]
    print(irule)
    assert irule.__class__.__name__ == "PropertyPatternRule"
    assert irule.rule_str == r
    assert irule.nature == RuleNature.INCLUDE
    assert irule.container == "properties"
    assert irule.target == "priority"
    assert irule.condition == RuleConditionType.LESS_THAN
    assert irule.expression == 3
    assert irule.checker.__name__ == 'less_than'

    r = "priority gt 1"
    rules = Rules()    
    rules.include(r)
    irule = rules.irules[0]
    print(irule)
    assert irule.__class__.__name__ == "PropertyPatternRule"
    assert irule.rule_str == r
    assert irule.nature == RuleNature.INCLUDE
    assert irule.container == "properties"
    assert irule.target == "priority"
    assert irule.condition == RuleConditionType.GREATER_THAN
    assert irule.expression == 1
    assert irule.checker.__name__ == 'greater_than'

    r = "priority > 1"
    rules = Rules()    
    rules.include(r)
    irule = rules.irules[0]
    print(irule)
    assert irule.__class__.__name__ == "PropertyPatternRule"
    assert irule.rule_str == r
    assert irule.nature == RuleNature.INCLUDE
    assert irule.container == "properties"
    assert irule.target == "priority"
    assert irule.condition == RuleConditionType.GREATER_THAN
    assert irule.expression == 1
    assert irule.checker.__name__ == 'greater_than'

    r = "priority le 2"
    rules = Rules()    
    rules.include(r)
    irule = rules.irules[0]
    print(irule)
    assert irule.__class__.__name__ == "PropertyPatternRule"
    assert irule.rule_str == r
    assert irule.nature == RuleNature.INCLUDE
    assert irule.container == "properties"
    assert irule.target == "priority"
    assert irule.condition == RuleConditionType.LESS_OR_EQUAL
    assert irule.expression == 2
    assert irule.checker.__name__ == 'less_or_equal'

    r = "priority <= 2"
    rules = Rules()    
    rules.include(r)
    irule = rules.irules[0]
    print(irule)
    assert irule.__class__.__name__ == "PropertyPatternRule"
    assert irule.rule_str == r
    assert irule.nature == RuleNature.INCLUDE
    assert irule.container == "properties"
    assert irule.target == "priority"
    assert irule.condition == RuleConditionType.LESS_OR_EQUAL
    assert irule.expression == 2
    assert irule.checker.__name__ == 'less_or_equal'

    r = "priority ge 2"
    rules = Rules()    
    rules.include(r)
    irule = rules.irules[0]
    print(irule)
    assert irule.__class__.__name__ == "PropertyPatternRule"
    assert irule.rule_str == r
    assert irule.nature == RuleNature.INCLUDE
    assert irule.container == "properties"
    assert irule.target == "priority"
    assert irule.condition == RuleConditionType.GREATER_OR_EQUAL
    assert irule.expression == 2
    assert irule.checker.__name__ == 'greater_or_equal'

    r = "priority >= 2"
    rules = Rules()    
    rules.include(r)
    irule = rules.irules[0]
    print(irule)
    assert irule.__class__.__name__ == "PropertyPatternRule"
    assert irule.rule_str == r
    assert irule.nature == RuleNature.INCLUDE
    assert irule.container == "properties"
    assert irule.target == "priority"
    assert irule.condition == RuleConditionType.GREATER_OR_EQUAL
    assert irule.expression == 2
    assert irule.checker.__name__ == 'greater_or_equal'


@test
def check_rule_creation_str_prop_comp(request):
    r = "app_version is 2.1.1"
    rules = Rules()    
    rules.include(r)
    irule = rules.irules[0]
    print(irule)
    assert irule.__class__.__name__ == "PropertyPatternRule"
    assert irule.rule_str == r
    assert irule.nature == RuleNature.INCLUDE
    assert irule.container == "properties"
    assert irule.target == "app_version"
    assert irule.condition == RuleConditionType.EQUAL
    assert irule.expression == "2.1.1"
    assert irule.checker.__name__ == 'are_equal'

    r = "app_version eq 2.1.1"
    rules = Rules()    
    rules.include(r)
    irule = rules.irules[0]
    print(irule)
    assert irule.__class__.__name__ == "PropertyPatternRule"
    assert irule.rule_str == r
    assert irule.nature == RuleNature.INCLUDE
    assert irule.container == "properties"
    assert irule.target == "app_version"
    assert irule.condition == RuleConditionType.EQUAL
    assert irule.expression == "2.1.1"
    assert irule.checker.__name__ == 'are_equal'

    r = "app_version = 2.1.1"
    rules = Rules()    
    rules.include(r)
    irule = rules.irules[0]
    print(irule)
    assert irule.__class__.__name__ == "PropertyPatternRule"
    assert irule.rule_str == r
    assert irule.nature == RuleNature.INCLUDE
    assert irule.container == "properties"
    assert irule.target == "app_version"
    assert irule.condition == RuleConditionType.EQUAL
    assert irule.expression == "2.1.1"
    assert irule.checker.__name__ == 'are_equal'

    r = "app_version == 2.1.1"
    rules = Rules()    
    rules.include(r)
    irule = rules.irules[0]
    print(irule)
    assert irule.__class__.__name__ == "PropertyPatternRule"
    assert irule.rule_str == r
    assert irule.nature == RuleNature.INCLUDE
    assert irule.container == "properties"
    assert irule.target == "app_version"
    assert irule.condition == RuleConditionType.EQUAL
    assert irule.expression == "2.1.1"
    assert irule.checker.__name__ == 'are_equal'

    r = "app_version not 2.1.2"
    rules = Rules()    
    rules.include(r)
    irule = rules.irules[0]
    print(irule)
    assert irule.__class__.__name__ == "PropertyPatternRule"
    assert irule.rule_str == r
    assert irule.nature == RuleNature.INCLUDE
    assert irule.container == "properties"
    assert irule.target == "app_version"
    assert irule.condition == RuleConditionType.NOT_EQUAL
    assert irule.expression == "2.1.2"
    assert irule.checker.__name__ == 'are_not_equal'

    r = "app_version != 2.1.2"
    rules = Rules()    
    rules.include(r)
    irule = rules.irules[0]
    print(irule)
    assert irule.__class__.__name__ == "PropertyPatternRule"
    assert irule.rule_str == r
    assert irule.nature == RuleNature.INCLUDE
    assert irule.container == "properties"
    assert irule.target == "app_version"
    assert irule.condition == RuleConditionType.NOT_EQUAL
    assert irule.expression == "2.1.2"
    assert irule.checker.__name__ == 'are_not_equal'

    r = "app_version ne 2.1.2"
    rules = Rules()    
    rules.include(r)
    irule = rules.irules[0]
    print(irule)
    assert irule.__class__.__name__ == "PropertyPatternRule"
    assert irule.rule_str == r
    assert irule.nature == RuleNature.INCLUDE
    assert irule.container == "properties"
    assert irule.target == "app_version"
    assert irule.condition == RuleConditionType.NOT_EQUAL
    assert irule.expression == "2.1.2"
    assert irule.checker.__name__ == 'are_not_equal'

    r = "app_version lt 2.1.2"
    rules = Rules()    
    rules.include(r)
    irule = rules.irules[0]
    print(irule)
    assert irule.__class__.__name__ == "PropertyPatternRule"
    assert irule.rule_str == r
    assert irule.nature == RuleNature.INCLUDE
    assert irule.container == "properties"
    assert irule.target == "app_version"
    assert irule.condition == RuleConditionType.LESS_THAN
    assert irule.expression == "2.1.2"
    assert irule.checker.__name__ == 'less_than'

    r = "app_version < 2.1.2"
    rules = Rules()    
    rules.include(r)
    irule = rules.irules[0]
    print(irule)
    assert irule.__class__.__name__ == "PropertyPatternRule"
    assert irule.rule_str == r
    assert irule.nature == RuleNature.INCLUDE
    assert irule.container == "properties"
    assert irule.target == "app_version"
    assert irule.condition == RuleConditionType.LESS_THAN
    assert irule.expression == "2.1.2"
    assert irule.checker.__name__ == 'less_than'

    r = "app_version gt 2.1.0"
    rules = Rules()    
    rules.include(r)
    irule = rules.irules[0]
    print(irule)
    assert irule.__class__.__name__ == "PropertyPatternRule"
    assert irule.rule_str == r
    assert irule.nature == RuleNature.INCLUDE
    assert irule.container == "properties"
    assert irule.target == "app_version"
    assert irule.condition == RuleConditionType.GREATER_THAN
    assert irule.expression == "2.1.0"
    assert irule.checker.__name__ == 'greater_than'

    r = "app_version > 2.1.0"
    rules = Rules()    
    rules.include(r)
    irule = rules.irules[0]
    print(irule)
    assert irule.__class__.__name__ == "PropertyPatternRule"
    assert irule.rule_str == r
    assert irule.nature == RuleNature.INCLUDE
    assert irule.container == "properties"
    assert irule.target == "app_version"
    assert irule.condition == RuleConditionType.GREATER_THAN
    assert irule.expression == "2.1.0"
    assert irule.checker.__name__ == 'greater_than'

    r = "app_version le 2.1.1"
    rules = Rules()    
    rules.include(r)
    irule = rules.irules[0]
    print(irule)
    assert irule.__class__.__name__ == "PropertyPatternRule"
    assert irule.rule_str == r
    assert irule.nature == RuleNature.INCLUDE
    assert irule.container == "properties"
    assert irule.target == "app_version"
    assert irule.condition == RuleConditionType.LESS_OR_EQUAL
    assert irule.expression == "2.1.1"
    assert irule.checker.__name__ == 'less_or_equal'

    r = "app_version <= 2.1.1"
    rules = Rules()    
    rules.include(r)
    irule = rules.irules[0]
    print(irule)
    assert irule.__class__.__name__ == "PropertyPatternRule"
    assert irule.rule_str == r
    assert irule.nature == RuleNature.INCLUDE
    assert irule.container == "properties"
    assert irule.target == "app_version"
    assert irule.condition == RuleConditionType.LESS_OR_EQUAL
    assert irule.expression == "2.1.1"
    assert irule.checker.__name__ == 'less_or_equal'

    r = "app_version ge 2.1.1"
    rules = Rules()    
    rules.include(r)
    irule = rules.irules[0]
    print(irule)
    assert irule.__class__.__name__ == "PropertyPatternRule"
    assert irule.rule_str == r
    assert irule.nature == RuleNature.INCLUDE
    assert irule.container == "properties"
    assert irule.target == "app_version"
    assert irule.condition == RuleConditionType.GREATER_OR_EQUAL
    assert irule.expression == "2.1.1"
    assert irule.checker.__name__ == 'greater_or_equal'

    r = "app_version >= 2.1.1"
    rules = Rules()    
    rules.include(r)
    irule = rules.irules[0]
    print(irule)
    assert irule.__class__.__name__ == "PropertyPatternRule"
    assert irule.rule_str == r
    assert irule.nature == RuleNature.INCLUDE
    assert irule.container == "properties"
    assert irule.target == "app_version"
    assert irule.condition == RuleConditionType.GREATER_OR_EQUAL
    assert irule.expression == "2.1.1"
    assert irule.checker.__name__ == 'greater_or_equal'


@test
def check_rule_creation_tags(request):
    r = "with tags chrome, firefox"
    rules = Rules()    
    rules.include(r)
    irule = rules.irules[0]
    print(irule)
    assert irule.__class__.__name__ == "TagsPatternRule"
    assert irule.rule_str == r
    assert irule.nature == RuleNature.INCLUDE
    assert irule.container == "tags"
    assert irule.target == set({'chrome', 'firefox'})
    assert irule.condition == RuleConditionType.HAS_INTERSECTION
    assert irule.expression == set({'chrome', 'firefox'})
    assert irule.checker.__name__ == 'has_intersection'

    r = "with tag chrome"
    rules = Rules()    
    rules.include(r)
    irule = rules.irules[0]
    print(irule)
    assert irule.__class__.__name__ == "TagsPatternRule"
    assert irule.rule_str == r
    assert irule.nature == RuleNature.INCLUDE
    assert irule.container == "tags"
    assert irule.target == set({'chrome'})
    assert irule.condition == RuleConditionType.HAS_INTERSECTION
    assert irule.expression == set({'chrome'})
    assert irule.checker.__name__ == 'has_intersection'

    r = "withall tags chrome, abc"
    rules = Rules()    
    rules.include(r)
    irule = rules.irules[0]
    print(irule)
    assert irule.__class__.__name__ == "TagsPatternRule"
    assert irule.rule_str == r
    assert irule.nature == RuleNature.INCLUDE
    assert irule.container == "tags"
    assert irule.target == set({'chrome', 'abc'})
    assert irule.condition == RuleConditionType.IS_SUBSET
    assert irule.expression == set({'chrome', 'abc'})
    assert irule.checker.__name__ == 'is_subset'

    r = "without tags chrome, abc"
    rules = Rules()    
    rules.include(r)
    irule = rules.irules[0]
    print(irule)
    assert irule.__class__.__name__ == "TagsPatternRule"
    assert irule.rule_str == r
    assert irule.nature == RuleNature.INCLUDE
    assert irule.container == "tags"
    assert irule.target == set({'chrome', 'abc'})
    assert irule.condition == RuleConditionType.NO_INTERSECTION
    assert irule.expression == set({'chrome', 'abc'})
    assert irule.checker.__name__ == 'has_no_intersection'

    r = "without tag chrome"
    rules = Rules()    
    rules.include(r)
    irule = rules.irules[0]
    print(irule)
    assert irule.__class__.__name__ == "TagsPatternRule"
    assert irule.rule_str == r
    assert irule.nature == RuleNature.INCLUDE
    assert irule.container == "tags"
    assert irule.target == set({'chrome'})
    assert irule.condition == RuleConditionType.NO_INTERSECTION
    assert irule.expression == set({'chrome'})
    assert irule.checker.__name__ == 'has_no_intersection'

    r = "with bugs b1,b2"
    rules = Rules()    
    rules.include(r)
    irule = rules.irules[0]
    print(irule)
    assert irule.__class__.__name__ == "TagsPatternRule"
    assert irule.rule_str == r
    assert irule.nature == RuleNature.INCLUDE
    assert irule.container == "bugs"
    assert irule.target == set({'b1', 'b2'})
    assert irule.condition == RuleConditionType.HAS_INTERSECTION
    assert irule.expression == set({'b1', 'b2'})
    assert irule.checker.__name__ == 'has_intersection'

    r = "with bug b1"
    rules = Rules()    
    rules.include(r)
    irule = rules.irules[0]
    print(irule)
    assert irule.__class__.__name__ == "TagsPatternRule"
    assert irule.rule_str == r
    assert irule.nature == RuleNature.INCLUDE
    assert irule.container == "bugs"
    assert irule.target == set({'b1'})
    assert irule.condition == RuleConditionType.HAS_INTERSECTION
    assert irule.expression == set({'b1'})
    assert irule.checker.__name__ == 'has_intersection'

    r = "withall bugs b1,abc"
    rules = Rules()    
    rules.include(r)
    irule = rules.irules[0]
    print(irule)
    assert irule.__class__.__name__ == "TagsPatternRule"
    assert irule.rule_str == r
    assert irule.nature == RuleNature.INCLUDE
    assert irule.container == "bugs"
    assert irule.target == set({'b1', 'abc'})
    assert irule.condition == RuleConditionType.IS_SUBSET
    assert irule.expression == set({'b1', 'abc'})
    assert irule.checker.__name__ == 'is_subset'

    r = "without bugs b1,abc"
    rules = Rules()    
    rules.include(r)
    irule = rules.irules[0]
    print(irule)
    assert irule.__class__.__name__ == "TagsPatternRule"
    assert irule.rule_str == r
    assert irule.nature == RuleNature.INCLUDE
    assert irule.container == "bugs"
    assert irule.target == set({'b1', 'abc'})
    assert irule.condition == RuleConditionType.NO_INTERSECTION
    assert irule.expression == set({'b1', 'abc'})
    assert irule.checker.__name__ == 'has_no_intersection'

    r = "without bug b1"
    rules = Rules()    
    rules.include(r)
    irule = rules.irules[0]
    print(irule)
    assert irule.__class__.__name__ == "TagsPatternRule"
    assert irule.rule_str == r
    assert irule.nature == RuleNature.INCLUDE
    assert irule.container == "bugs"
    assert irule.target == set({'b1'})
    assert irule.condition == RuleConditionType.NO_INTERSECTION
    assert irule.expression == set({'b1'})
    assert irule.checker.__name__ == 'has_no_intersection'

    r = "with envs env1, env2"
    rules = Rules()    
    rules.include(r)
    irule = rules.irules[0]
    print(irule)
    assert irule.__class__.__name__ == "TagsPatternRule"
    assert irule.rule_str == r
    assert irule.nature == RuleNature.INCLUDE
    assert irule.container == "envs"
    assert irule.target == set({'env1', 'env2'})
    assert irule.condition == RuleConditionType.HAS_INTERSECTION
    assert irule.expression == set({'env1', 'env2'})
    assert irule.checker.__name__ == 'has_intersection'

    r = "with env env1"
    rules = Rules()    
    rules.include(r)
    irule = rules.irules[0]
    print(irule)
    assert irule.__class__.__name__ == "TagsPatternRule"
    assert irule.rule_str == r
    assert irule.nature == RuleNature.INCLUDE
    assert irule.container == "envs"
    assert irule.target == set({'env1'})
    assert irule.condition == RuleConditionType.HAS_INTERSECTION
    assert irule.expression == set({'env1'})
    assert irule.checker.__name__ == 'has_intersection'

    r = "withall envs env1, env2"
    rules = Rules()    
    rules.include(r)
    irule = rules.irules[0]
    print(irule)
    assert irule.__class__.__name__ == "TagsPatternRule"
    assert irule.rule_str == r
    assert irule.nature == RuleNature.INCLUDE
    assert irule.container == "envs"
    assert irule.target == set({'env1', 'env2'})
    assert irule.condition == RuleConditionType.IS_SUBSET
    assert irule.expression == set({'env1', 'env2'})
    assert irule.checker.__name__ == 'is_subset'

    r = "without envs env1, env2"
    rules = Rules()    
    rules.include(r)
    irule = rules.irules[0]
    print(irule)
    assert irule.__class__.__name__ == "TagsPatternRule"
    assert irule.rule_str == r
    assert irule.nature == RuleNature.INCLUDE
    assert irule.container == "envs"
    assert irule.target == set({'env1', 'env2'})
    assert irule.condition == RuleConditionType.NO_INTERSECTION
    assert irule.expression == set({'env1', 'env2'})
    assert irule.checker.__name__ == 'has_no_intersection'

    r = "without env env1"
    rules = Rules()    
    rules.include(r)
    irule = rules.irules[0]
    print(irule)
    assert irule.__class__.__name__ == "TagsPatternRule"
    assert irule.rule_str == r
    assert irule.nature == RuleNature.INCLUDE
    assert irule.container == "envs"
    assert irule.target == set({'env1'})
    assert irule.condition == RuleConditionType.NO_INTERSECTION
    assert irule.expression == set({'env1'})
    assert irule.checker.__name__ == 'has_no_intersection'