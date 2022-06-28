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

import random

from arjuna import *

from arjuna.core.poller.conditions import *
from arjuna.core.error import WaitableError

def is_expected_number_generated_1(num):
    retval = random.randint(1, 20)
    log_info("Generated:", retval)
    return retval == num

def expected_number_generated_1(num):
    return Conditions.true_condition(is_expected_number_generated_1, num)

@test
def check_random_waiter_1(request):
    expected_number_generated_1(5).wait()

@test
def check_random_waiter_2(request):
    expected_number_generated_1(51).wait(max_wait=10)

class ExpectedNumNotGenerated(WaitableError):

    def __init__(self, num):
        super().__init__(f"Expected number {num} not generated despite waiting.")

def is_expected_number_generated_2(num):
    retval = random.randint(1, 20)
    log_info(retval, num, retval==num)
    if retval != num:
        raise ExpectedNumNotGenerated(num)
    else:
        return True

def expected_number_generated_2(num):
    return Conditions.true_condition(is_expected_number_generated_2, num)

@test
def check_random_waiter_3(request):
    expected_number_generated_2(5).wait()

@test
def check_random_waiter_4(request):
    expected_number_generated_2(51).wait(max_wait=10)