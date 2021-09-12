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


@test(skip=True)
def check_skip(request):
    print("Should be skipped")
    assert 1 == 2

@test(skip=False, xfail=True)
def check_not_skip(request):
    print("Should not be skipped")
    assert 1 == 2

@test(skip=skip("True is True"))
def check_skip_with_condition_str(request):
    print("Should be skipped")
    assert 1 == 2

@test(skip=skip("True is False"), xfail=True)
def check_not_skip_with_condition_str(request):
    print("Should not be skipped")
    assert 1 == 2

@test(skip=skip("True is True"), reason="Whatever reason")
def check_skip_with_condition_str_reason(request):
    print("Should be skipped")
    assert 1 == 2