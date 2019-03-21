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

class CustomObject:
    pass

@test_function(
    evars = evars(
        i = 1,
        f = 2.3,
        s = 'test',
        b = False
    )
)
def test_evar_allowed_value_types(my):
    console.display(my.evars)
    my.evars['int'] = -3.4
    my.evars['float'] = 1.23468564
    my.evars['str'] = 'sample'
    my.evars['bool'] = True
    console.display(my.evars)

'''
The following would be reported as a step and hence test error.
Arjuna handles run-time issues that happen once test execution has started in corresponding test object context.
'''
@test_function
def test_disallowed_evar_in_body(my):
    my.evars['c'] = CustomObject()
    console.display(my.evars)


'''
Arjuna does a strict check on the values supplied in markup decorators.
Uncommenting the following would cause Arjuna's exit.
'''
# @test_function(
#     evars = evars(
#         c = CustomObject()
#     )
# )
# def test_disallowed_evar_in_decorator(my):
#     console.display(my.evars)