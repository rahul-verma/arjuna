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

@init_module(id=91, priority=1,
    name='This test demonstrates using of custom keywords for describing a test module.',
    author='Rahul',
    idea='Explore the test module properties dictionary',
    policy='Product Policy 33',
    os='Mac'
)
def setup_module(my):
    pass

@test_function
def demo_inherited_module_props(my):
    print("Print stmt 1")
    console.display(my.info.module.props)
    print("Print stmt 2")
    console.display(my.info.module.props['author'])