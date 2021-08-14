# This file is a part of Arjuna
# Copyright 2015-2021 Rahul Verma

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
Person = data_entity("Person", "name age")

@test(drive_with=record(
    person=Person(name="Rahul", age=99)
))
def check_drive_with_simple_entity(request, data):
    request.asserter.assert_equal(data.person.name, "Rahul", msg=msg)



@test(drive_with=record(
    fname=generator(Random.first_name).generate()
))
def check_drive_with_gen_generate_call(request, data):
    print(data.fname)

@test(drive_with=record(
    fname=generator(Random.first_name)
))
def check_drive_with_gen_without_generate_call(request, data):
    print(data.fname)