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


class MyDataClass:

    def __init__(self, num):
        self.num = num

    def __iter__(self):
        return iter(range(self.num))

def myrange(num):
    return range(num)

# The following decorator binds multiple data sources to the test function.
# You should see test method executed 1 (record) + 2 (records) + 4 (func) + 7 (class) + 2 (file) = 16 times
@test_function(
    drive_with=many_data_sources(
        record(1,2,3),
        records(record(4,5,6), record(a=4)),
        data_function(myrange, 4),
        data_class(MyDataClass, 7),
        data_file("input.xls")
    )
)
def test_multiple_data_sources(my):
    print(my.data.record)