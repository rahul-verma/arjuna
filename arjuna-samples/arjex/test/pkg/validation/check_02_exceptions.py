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

def call_this(i):
    return int(i)

def generate_exc(e):
    raise e()

@test
def check_assert_exc_pass(request):
    request.asserter.assert_exceptions(ValueError, call_this, "a")

@test(xfail=True)
def check_assert_exc_fail(request):
    request.asserter.assert_exceptions(ValueError, call_this, 1)

@test
def check_assert_exc_cm_pass(request):
    with request.asserter.assert_exceptions(ValueError):
        call_this("a")

@test(xfail=True)
def check_assert_exc_cm_fail(request):
    with request.asserter.assert_exceptions(ValueError):
        call_this(1)

@test
def check_assert_exc_regex_pass(request):
    request.asserter.assert_exceptions(ValueError, call_this, "a", regex=".*invalid literal.*")


@test(xfail=True)
def check_assert_exc_regex_fail(request):
    request.asserter.assert_exceptions(ValueError, call_this, "a", regex=".*wrong msg.*")

@test
def check_assert_exc_multi_pass(request):
    request.asserter.assert_exceptions((ValueError, TypeError), generate_exc, ValueError)
    request.asserter.assert_exceptions((ValueError, TypeError), generate_exc, TypeError)

@test(xfail=True)
def check_assert_exc_multi_fail(request):
    request.asserter.assert_exceptions((ValueError, IndexError), generate_exc, TypeError)