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

'''
Unlike evars, runtime can contain any type of objects.
runtime objects can only be assigned at run time and not in markup decorators or config files.
Built-in props, user-props, test meta data and evars could be used to determine what type of object you
want to create an store in run-time.
'''
@test_function
def test_simple_runtime(my):
    my.runtime['int'] = 1
    my.runtime['dynamic'] = CustomObject()
    console.display(my.runtime)


@test_function
def test_disallowed_reassignment_of_runtime_objects(my):
    my.runtime['ref_name'] = 1
    # This would raise exception as reference names are once-only. Once set, you can not change their values.
    my.runtime['ref_name'] = 2