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

msg="Unexpected data record."

@test(drive_with=record(1,2))
def check_pos_data(request, data):
    request.asserter.assert_equal(data[0] + data[1], 3, msg=msg)

@test(drive_with=record(a=1,b=2))
def check_named_data(request, data):
    request.asserter.assert_equal(data['a'] + data['b'], 3, msg=msg)

@test(drive_with=record(1,2, a=3,b=4))
def check_pos_named_data(request, data):
    request.asserter.assert_equal(data[0] + data[1] + data['a'] + data['b'], 10, msg=msg)

@test(drive_with=record(a=1,b=2))
def check_names_args_with_dot(request, data):
    request.asserter.assert_equal(data.a + data.b, 3, msg=msg)

@test(drive_with=record(a=1,b=2))
def check_names_args_ci(request, data):
    request.asserter.assert_equal(data.A + data['B'], 3, msg=msg)