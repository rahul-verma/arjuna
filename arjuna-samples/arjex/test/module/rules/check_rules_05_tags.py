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
def check_rule_creation_tags(request):
    r = "with tags chrome, firefox"
    selector = Selector()    
    selector.add_rule(r)
    rule = selector.rules[0]
    print(rule)
    assert rule.__class__.__name__ == "TagsPatternRule"
    assert rule.rule_str == r
    assert rule.container == "tags"
    assert rule.target == set({'chrome', 'firefox'})
    assert rule.condition == RuleConditionType.HAS_INTERSECTION
    assert rule.expression == set({'chrome', 'firefox'})
    assert rule.checker.__name__ == 'has_intersection'

    r = "with tag chrome"
    selector = Selector()    
    selector.add_rule(r)
    rule = selector.rules[0]
    print(rule)
    assert rule.__class__.__name__ == "TagsPatternRule"
    assert rule.rule_str == r
    assert rule.container == "tags"
    assert rule.target == set({'chrome'})
    assert rule.condition == RuleConditionType.HAS_INTERSECTION
    assert rule.expression == set({'chrome'})
    assert rule.checker.__name__ == 'has_intersection'

    r = "withall tags chrome, abc"
    selector = Selector()    
    selector.add_rule(r)
    rule = selector.rules[0]
    print(rule)
    assert rule.__class__.__name__ == "TagsPatternRule"
    assert rule.rule_str == r
    assert rule.container == "tags"
    assert rule.target == set({'chrome', 'abc'})
    assert rule.condition == RuleConditionType.IS_SUBSET
    assert rule.expression == set({'chrome', 'abc'})
    assert rule.checker.__name__ == 'is_subset'

    r = "without tags chrome, abc"
    selector = Selector()    
    selector.add_rule(r)
    rule = selector.rules[0]
    print(rule)
    assert rule.__class__.__name__ == "TagsPatternRule"
    assert rule.rule_str == r
    assert rule.container == "tags"
    assert rule.target == set({'chrome', 'abc'})
    assert rule.condition == RuleConditionType.NO_INTERSECTION
    assert rule.expression == set({'chrome', 'abc'})
    assert rule.checker.__name__ == 'has_no_intersection'

    r = "without tag chrome"
    selector = Selector()    
    selector.add_rule(r)
    rule = selector.rules[0]
    print(rule)
    assert rule.__class__.__name__ == "TagsPatternRule"
    assert rule.rule_str == r
    assert rule.container == "tags"
    assert rule.target == set({'chrome'})
    assert rule.condition == RuleConditionType.NO_INTERSECTION
    assert rule.expression == set({'chrome'})
    assert rule.checker.__name__ == 'has_no_intersection'

    r = "with bugs b1,b2"
    selector = Selector()    
    selector.add_rule(r)
    rule = selector.rules[0]
    print(rule)
    assert rule.__class__.__name__ == "TagsPatternRule"
    assert rule.rule_str == r
    assert rule.container == "bugs"
    assert rule.target == set({'b1', 'b2'})
    assert rule.condition == RuleConditionType.HAS_INTERSECTION
    assert rule.expression == set({'b1', 'b2'})
    assert rule.checker.__name__ == 'has_intersection'

    r = "with bug b1"
    selector = Selector()    
    selector.add_rule(r)
    rule = selector.rules[0]
    print(rule)
    assert rule.__class__.__name__ == "TagsPatternRule"
    assert rule.rule_str == r
    assert rule.container == "bugs"
    assert rule.target == set({'b1'})
    assert rule.condition == RuleConditionType.HAS_INTERSECTION
    assert rule.expression == set({'b1'})
    assert rule.checker.__name__ == 'has_intersection'

    r = "withall bugs b1,abc"
    selector = Selector()    
    selector.add_rule(r)
    rule = selector.rules[0]
    print(rule)
    assert rule.__class__.__name__ == "TagsPatternRule"
    assert rule.rule_str == r
    assert rule.container == "bugs"
    assert rule.target == set({'b1', 'abc'})
    assert rule.condition == RuleConditionType.IS_SUBSET
    assert rule.expression == set({'b1', 'abc'})
    assert rule.checker.__name__ == 'is_subset'

    r = "without bugs b1,abc"
    selector = Selector()    
    selector.add_rule(r)
    rule = selector.rules[0]
    print(rule)
    assert rule.__class__.__name__ == "TagsPatternRule"
    assert rule.rule_str == r
    assert rule.container == "bugs"
    assert rule.target == set({'b1', 'abc'})
    assert rule.condition == RuleConditionType.NO_INTERSECTION
    assert rule.expression == set({'b1', 'abc'})
    assert rule.checker.__name__ == 'has_no_intersection'

    r = "without bug b1"
    selector = Selector()    
    selector.add_rule(r)
    rule = selector.rules[0]
    print(rule)
    assert rule.__class__.__name__ == "TagsPatternRule"
    assert rule.rule_str == r
    assert rule.container == "bugs"
    assert rule.target == set({'b1'})
    assert rule.condition == RuleConditionType.NO_INTERSECTION
    assert rule.expression == set({'b1'})
    assert rule.checker.__name__ == 'has_no_intersection'

    r = "with envs env1, env2"
    selector = Selector()    
    selector.add_rule(r)
    rule = selector.rules[0]
    print(rule)
    assert rule.__class__.__name__ == "TagsPatternRule"
    assert rule.rule_str == r
    assert rule.container == "envs"
    assert rule.target == set({'env1', 'env2'})
    assert rule.condition == RuleConditionType.HAS_INTERSECTION
    assert rule.expression == set({'env1', 'env2'})
    assert rule.checker.__name__ == 'has_intersection'

    r = "with env env1"
    selector = Selector()    
    selector.add_rule(r)
    rule = selector.rules[0]
    print(rule)
    assert rule.__class__.__name__ == "TagsPatternRule"
    assert rule.rule_str == r
    assert rule.container == "envs"
    assert rule.target == set({'env1'})
    assert rule.condition == RuleConditionType.HAS_INTERSECTION
    assert rule.expression == set({'env1'})
    assert rule.checker.__name__ == 'has_intersection'

    r = "withall envs env1, env2"
    selector = Selector()    
    selector.add_rule(r)
    rule = selector.rules[0]
    print(rule)
    assert rule.__class__.__name__ == "TagsPatternRule"
    assert rule.rule_str == r
    assert rule.container == "envs"
    assert rule.target == set({'env1', 'env2'})
    assert rule.condition == RuleConditionType.IS_SUBSET
    assert rule.expression == set({'env1', 'env2'})
    assert rule.checker.__name__ == 'is_subset'

    r = "without envs env1, env2"
    selector = Selector()    
    selector.add_rule(r)
    rule = selector.rules[0]
    print(rule)
    assert rule.__class__.__name__ == "TagsPatternRule"
    assert rule.rule_str == r
    assert rule.container == "envs"
    assert rule.target == set({'env1', 'env2'})
    assert rule.condition == RuleConditionType.NO_INTERSECTION
    assert rule.expression == set({'env1', 'env2'})
    assert rule.checker.__name__ == 'has_no_intersection'

    r = "without env env1"
    selector = Selector()    
    selector.add_rule(r)
    rule = selector.rules[0]
    print(rule)
    assert rule.__class__.__name__ == "TagsPatternRule"
    assert rule.rule_str == r
    assert rule.container == "envs"
    assert rule.target == set({'env1'})
    assert rule.condition == RuleConditionType.NO_INTERSECTION
    assert rule.expression == set({'env1'})
    assert rule.checker.__name__ == 'has_no_intersection'

@test
def check_tag_selection(request):
    for tname in ['tag', 'bug' , 'env']:
        rule = get_rule(f"with {tname}s t1, t2")
        obj = Obj()
        assert rule.matches(obj) is False

        obj = Obj()
        getattr(obj, f'{tname}s').add('t1')
        assert rule.matches(obj) is True

        obj = Obj()
        getattr(obj, f'{tname}s').add('t2')
        assert rule.matches(obj) is True

        obj = Obj()
        getattr(obj, f'{tname}s').add('abc')
        assert rule.matches(obj) is False

        rule = get_rule(f"with {tname} t1")
        obj = Obj()
        assert rule.matches(obj) is False

        obj = Obj()
        getattr(obj, f'{tname}s').add('t1')
        assert rule.matches(obj) is True

        obj = Obj()
        getattr(obj, f'{tname}s').add('abc')
        assert rule.matches(obj) is False

        rule = get_rule(f"withall {tname}s t1, abc")
        obj = Obj()
        assert rule.matches(obj) is False

        obj = Obj()
        getattr(obj, f'{tname}s').add('t1')
        assert rule.matches(obj) is False

        obj = Obj()
        getattr(obj, f'{tname}s').add('t2')
        assert rule.matches(obj) is False

        obj = Obj()
        getattr(obj, f'{tname}s').update({'t2', 't1'})
        assert rule.matches(obj) is False

        obj = Obj()
        getattr(obj, f'{tname}s').add('abc')
        assert rule.matches(obj) is False

        rule = get_rule(f"without {tname}s t1, abc")
        obj = Obj()
        assert rule.matches(obj) is True

        obj = Obj()
        getattr(obj, f'{tname}s').add('t1')
        assert rule.matches(obj) is False

        obj = Obj()
        getattr(obj, f'{tname}s').add('abc')
        assert rule.matches(obj) is False

        obj = Obj()
        getattr(obj, f'{tname}s').add('t2')
        assert rule.matches(obj) is True

        rule = get_rule(f"without {tname} t1")
        obj = Obj()
        assert rule.matches(obj) is True

        obj = Obj()
        getattr(obj, f'{tname}s').add('t1')
        assert rule.matches(obj) is False

        obj = Obj()
        getattr(obj, f'{tname}s').add('abc')
        assert rule.matches(obj) is True