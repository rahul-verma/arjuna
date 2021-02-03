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

@test
def check_normal_fail(request):
    print("Should be reported as FAIL")
    assert 1 == 2

@test(xfail=False)
def check_xfail_false(request):
    print("Should be reported as FAIL")
    assert 1 == 2

@test(xfail=1 is 1)
def check_xfail_condition(request):
    print("Should be reported as XFAIL")
    assert 1 == 2

@test(xfail=True)
def check_xfail(request):
    print("Should be reported as XFAIL")
    assert 1 == 2

@test(xfail=True)
def check_xpass(request):
    print("Should be reported as XPASS")
    assert 1 == 1

@test(xfail=xfail(1 is 1, reason="Some reason", raises=TypeError))
def check_xfail_condition_exc_nonexpected(request):
    assert 1 == 2

@test(xfail=xfail(1 is 1, reason="Some reason", raises=TypeError))
def check_xfail_condition_exc_expected(request):
    1 + "a"