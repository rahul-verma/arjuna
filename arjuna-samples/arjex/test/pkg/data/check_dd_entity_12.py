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

@test
def check_basic_data_entity(request):
    Person = data_entity("Person", "name age")
    person = Person(name="Rahul", age=99)
    print(person)

@test
def check_wrong_attr_data_entity(request):
    Person = data_entity("Person", "name age")
    person = Person(name="Rahul", age=99, not_allowed=123)
    print(person)

@test
def check_multi_str_data_entity(request):
    Person = data_entity("Person", "name age", "country")
    person = Person(name="Rahul", age=99, country="India")
    print(person)

@test
def check_default_data_entity(request):
    Person = data_entity("Person", "name age", country="India")
    person = Person(name="Rahul", age=99)
    print(person)
    person = Person(name="Rahul", age=99, country="Germany")
    print(person)