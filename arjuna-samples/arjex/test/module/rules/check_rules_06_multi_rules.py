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
from arjuna.core.error import *
from .helpers import *


@test
def check_3_passing_rules(request):
    obj = Obj()
    obj.info.unstable = True
    obj.info.priority = 2
    obj.tags = {'chrome'}

    selector = Selector()    
    selector.add_rule("unstable")
    selector.add_rule("priority is 2")
    selector.add_rule("with tag chrome")
    
    selector.validate(obj)

@test
def check_first_mismatch(request):
    obj = Obj()
    obj.info.unstable = True
    obj.info.priority = 2
    obj.tags = {'chrome'}

    selector = Selector()    
    selector.add_rule("not unstable")
    selector.add_rule("priority is 2")
    selector.add_rule("with tag chrome")
    
    try:
        selector.validate(obj)
    except RuleNotMet as e:
        assert e.rule.rule_str == "not unstable"

@test
def check_second_mismatch(request):
    obj = Obj()
    obj.info.unstable = True
    obj.info.priority = 2
    obj.tags = {'chrome'}

    selector = Selector()    
    selector.add_rule("unstable")
    selector.add_rule("priority is 1")
    selector.add_rule("with tag chrome")
    
    try:
        selector.validate(obj)
    except RuleNotMet as e:
        assert e.rule.rule_str == "priority is 1"

@test
def check_third_mismatch(request):
    obj = Obj()
    obj.info.unstable = True
    obj.info.priority = 2
    obj.tags = {'chrome'}

    selector = Selector()    
    selector.add_rule("unstable")
    selector.add_rule("priority is 2")
    selector.add_rule("with tag firefox")
    
    try:
        selector.validate(obj)
    except RuleNotMet as e:
        assert e.rule.rule_str == "with tag firefox"