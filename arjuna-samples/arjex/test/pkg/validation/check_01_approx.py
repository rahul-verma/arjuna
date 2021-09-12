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
def check_assert_approx_pass(request):
    request.asserter.assert_approx_equal(4.4555, 4.4566, "Mismtatch", places=2)

@test(xfail=True)
def check_assert_approx_fail(request):
    request.asserter.assert_approx_equal(4.4555, 4.4566, "Mismtatch", places=3)

@test(xfail=True)
def check_assert_approx_pass_delta(request):
    request.asserter.assert_approx_equal(4.4555, 4.4566, "Mismtatch", delta=0.002)

@test
def check_assert_approx_fail_delta(request):
    request.asserter.assert_approx_equal(4.4555, 4.4566, "Mismtatch", delta=0.0001)



