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
    drive_with=records(
        record(1,2,3, ver='v1'),
        record(4,5,6, ver='v2'),
    )
)

def drive_with_multiple_records(my):
    console.display(my.data.record)
    console.display(my.data.record.indexed_values())
    console.display(my.data.record.value_at(1))
    console.display(my.data.record.named_values())
    console.display(my.data.record.value_named('ver'))