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

@test_function(
    bugs = bugs('B1', 'B2')
)
def configure_bugs(my):
    console.display(my.bugs)

@test_function(
    bugs=bugs('B1', 'B2')
)
def demo_immutable_bugs(my):
    console.display(my.bugs)
    # This would throw an exception as bugs set is not mutable within the body of methods just like props.
    # Bug names are stored as a Frozen Set
    my.bugs['runtime_tag'] = "B123"