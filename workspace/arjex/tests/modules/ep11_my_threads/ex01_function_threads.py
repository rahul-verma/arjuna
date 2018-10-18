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

from arjuna.lib.core.utils import thread_utils

'''
The 12 test methods would be executed using a pool of 5 threads.
For you to observer, thread name is printed.
It is of the format: st-<num>::g-<num>::gs-<num>::m-<num>::ms-<num>::f-<num>::t-<num>
Pay attention to the names. You would find while other sections remain same, the f-<num> is seen from f-1 to f-5
'''
@init_module(
    threads=5
)
def setup_module(my):
    pass

def induce_random_sleep():
    time.sleep(random.randint(2,6))
    console.display(thread_utils.get_current_thread_name())

@test_function
def test1(my):
    induce_random_sleep()

@test_function
def test2(my):
    induce_random_sleep()

@test_function
def test3(my):
    induce_random_sleep()

@test_function
def test4(my):
    induce_random_sleep()

@test_function
def test5(my):
    induce_random_sleep()

@test_function
def test6(my):
    induce_random_sleep()

@test_function
def test7(my):
    induce_random_sleep()

@test_function
def test8(my):
    induce_random_sleep()

@test_function
def test9(my):
    induce_random_sleep()

@test_function
def test10(my):
    induce_random_sleep()

@test_function
def test11(my):
    induce_random_sleep()

@test_function
def test12(my):
    induce_random_sleep()
