'''
This file is a part of Test Mile Arjuna
Copyright 2018 Test Mile Software Testing Pvt Ltd

Website: www.TestMile.com
Email: support [at] testmile.com
Creator: Rahul Verma

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

  http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
'''

import random
import time

from arjuna.tpi.markup import *
from arjuna.tpi.markup_helpers import *
from arjuna.tpi.helpers import *
from arjuna.lib.utils import thread_utils

def myrange(num):
    return range(num)


def induce_random_sleep():
    time.sleep(random.randint(2,6))
    console.display(thread_utils.get_current_thread_name())

'''
Test is an instance of a test function. Data driven tests 
Decorating with data-driven keywords, creates such instances. E.g. here 12 test would be created using data function.
The 12 tests would be executed using a pool of 5 threads.
For you to observer, thread name is printed.
It is of the format: st-<num>::g-<num>::gs-<num>::m-<num>::ms-<num>::f-<num>::t-<num>
Pay attention to the names. You would find while other sections remain same, the t-<num> is seen from t-1 to t-5
'''
@test_function(
    drive_with=data_function(myrange, 12),
    threads=5
)
def test_level_threads(my):
    induce_random_sleep()
    print(my.data.record)