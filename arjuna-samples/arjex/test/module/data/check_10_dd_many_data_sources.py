# This file is a part of Arjuna
# Copyright 2015-2020 Rahul Verma

# Website: www.RahulVerma.net

# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at

#   http://www.apache.org/licenses/LICENSE-2.0

# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from arjuna import *

class MyDataClass:

    def __iter__(self):
        records = (
            {'left':10, 'right':12, 'sum':22},
            {'left':20, 'right':32, 'sum':13},
        )
        return iter(records)


def myrange():
    return (
            {'left':30, 'right':42, 'sum':72},
            {'left':40, 'right':52, 'sum':17},
        )

@test(drive_with=many_data_sources(
    record(left=1, right=2, sum=3),
    records(
        record(left=3, right=4, sum=7),
        record(left=7, right=8, sum=10)
    ),
    data_function(myrange),
    data_class(MyDataClass),
    data_file("input.xls")
))
def check_drive_with_many_sources(request, data):
    request.asserter.assert_equal(int(data.left) + int(data.right), int(data.sum), "Calculation failed.")