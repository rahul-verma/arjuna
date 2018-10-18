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

from arjuna.tpi.markup import *
from arjuna.tpi.markup_helpers import *
from arjuna.tpi.helpers import *

@init_module
def module_level_setup(my):
    console.display("Module level setup executed")

@end_module
def module_level_cleanup(my):
    console.display("Module level cleanup executed")

@init_each_function
def each_function_level_setup(my):
    console.display("Function level setup executed")

@end_each_function
def each_function_level_cleanup(my):
    console.display("Function level cleanup executed")

@init_each_test
def each_test_level_setup(my):
    console.display("Test level setup executed")

@end_each_test
def each_test_level_cleanup(my):
    console.display("Test level cleanup executed")

def data_func_with_args(num):
    return range(num)

@test_function(
    drive_with=data_function(data_func_with_args, 2)
)
def ddt1(my):
    console.display(my.data.record)

@test_function(
    drive_with=data_function(data_func_with_args, 3)
)
def ddt2(my):
    console.display(my.data.record)