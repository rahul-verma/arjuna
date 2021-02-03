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
def check_all_user_props_absent(request):
    pass

@test(user_bool=True)
def check_user_bool_1(request):
    pass

@test(user_bool=False)
def check_user_bool_2(request):
    pass

@test(user_prop=2)
def check_user_prop_1(request):
    pass

@test(user_prop=3)
def check_user_prop_2(request):
    pass

@test(user_iter=['a','b'])
def check_user_iter_1(request):
    pass

@test(user_iter=['a','c'])
def check_user_iter_2(request):
    pass