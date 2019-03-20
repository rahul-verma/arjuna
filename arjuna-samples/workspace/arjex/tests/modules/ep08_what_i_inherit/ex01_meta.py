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

@test_function
def test_access_all_meta_data(my):
    # Session Info
    console.display(my.info.session.meta['name'])

    # Stage Info
    console.display(my.info.stage.meta['name'])

    # Group Info
    console.display(my.info.group.meta['name'])
    console.display(my.info.group.meta['slot'])

    # Module Info
    console.display(my.info.module.meta['pkg'])
    console.display(my.info.module.meta['name'])
    console.display(my.info.module.meta['qname'])
    console.display(my.info.module.meta['slot'])

    # Function Info
    console.display(my.info.function.meta['name'])
    console.display(my.info.function.meta['qname'])

    # Object Type (Here it is always Test. However Test is one of the many test object types in Arjuna)
    console.display(my.info.object_type)

    # Test Number. Usually 1. For data driven tests, it is the incremental counter
    console.display(my.info.test_num)

