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
def check_empty_include_rules(request):
    obj = Obj()
    obj.info.unstable = True
    obj.info.priority = 2
    obj.tags = {'chrome'}

    selector = Selector()        
    selector.validate(obj)

@test
def check_empty_exclude_rules(request):
    obj = Obj()

    selector = Selector()        
    selector.validate(obj)

@test
def check_first_include_match(request):
    obj = Obj()
    obj.info.unstable = True
    obj.info.priority = 2
    obj.tags = {'chrome'}

    selector = Selector()    
    selector.include("unstable")
    selector.include("priority is 3")
    selector.include("with tag firefox")
    
    selector.validate(obj)

@test
def check_second_include_match(request):
    obj = Obj()
    obj.info.unstable = True
    obj.info.priority = 2
    obj.tags = {'chrome'}

    selector = Selector()    
    selector.include("not unstable")
    selector.include("priority is 2")
    selector.include("with tag firefox")
    
    selector.validate(obj)

@test
def check_third_include_match(request):
    obj = Obj()
    obj.info.unstable = True
    obj.info.priority = 2
    obj.tags = {'chrome'}

    selector = Selector()    
    selector.include("not unstable")
    selector.include("priority is 3")
    selector.include("with tag chrome")
    
    selector.validate(obj)

@test
def check_no_include_match(request):
    obj = Obj()
    obj.info.unstable = True
    obj.info.priority = 2
    obj.tags = {'chrome'}

    selector = Selector()    
    selector.include("not unstable")
    selector.include("priority is 3")
    selector.include("with tag firefox")
    
    try:
        selector.validate(obj)
    except NoInclusionRuleMet as e:
        pass
    else:
        raise AssertionError()

@test
def check_first_exclude_match(request):
    obj = Obj()
    obj.info.unstable = True
    obj.info.priority = 2
    obj.tags = {'chrome'}

    selector = Selector()    
    selector.exclude("unstable")
    selector.exclude("priority is 3")
    selector.exclude("with tag firefox")
    
    try:
        selector.validate(obj)
    except ExclusionRuleMet as e:
        assert e.rule.rule_str == "unstable"
    else:
        raise AssertionError()


@test
def check_second_exclude_match(request):
    obj = Obj()
    obj.info.unstable = True
    obj.info.priority = 2
    obj.tags = {'chrome'}

    selector = Selector()    
    selector.exclude("not unstable")
    selector.exclude("priority is 2")
    selector.exclude("with tag firefox")
    
    try:
        selector.validate(obj)
    except ExclusionRuleMet as e:
        assert e.rule.rule_str == "priority is 2"
    else:
        raise AssertionError()


@test
def check_third_exclude_match(request):
    obj = Obj()
    obj.info.unstable = True
    obj.info.priority = 2
    obj.tags = {'chrome'}

    selector = Selector()    
    selector.exclude("not unstable")
    selector.exclude("priority is 3")
    selector.exclude("with tag chrome")
    
    try:
        selector.validate(obj)
    except ExclusionRuleMet as e:
        assert e.rule.rule_str == "with tag chrome"
    else:
        raise AssertionError()

@test
def check_no_exclude_match(request):
    obj = Obj()
    obj.info.unstable = True
    obj.info.priority = 2
    obj.tags = {'chrome'}

    selector = Selector()    
    selector.exclude("not unstable")
    selector.exclude("priority is 3")
    selector.exclude("with tag firefox")
    
    selector.validate(obj)
