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

@test_function(4)
def id_test(my):
    console.display(my.info.function.props)

@test_function(id=5)
def id_test2(my):
    console.display(my.info.function.props)

@test_function(id=91, priority=1,
    name='This test demonstrates using of built-in keywords for describing a test function.',
    author='Rahul',
    idea='Explore the test function properties dictionary',
    unstable=True,
    component='Arjuna Sample Project',
    app_version='3.23'
)
def id_test3(my):
    console.display(my.info.function.props)

@test_function(id=91, priority=1,
    name='This test demonstrates using of custom keywords for describing a test function.',
    author='Rahul',
    idea='Explore the test function properties dictionary',
    policy='Product Policy 33',
    os='Mac'
)
def id_test4(my):
    console.display(my.info.function.props)
