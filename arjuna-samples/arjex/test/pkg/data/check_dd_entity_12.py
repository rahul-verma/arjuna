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

@test
def check_entity_with_simple_generators(request):
    for i in range(3):
        Person1 = data_entity("Person1", "age", fname=Random.first_name)
        print(Person1(age=99))
        Person2 = data_entity("Person2", "age", fname=generator(Random.first_name))
        print(Person2(age=99))

@test
def check_entity_with_simple_gen_args(request):
    for i in range(3):
        Person1 = data_entity("Person", "name", debt=generator(Random.fixed_length_number, length=i+1))
        print(Person1(name='Mac'))

@test
def check_entity_with_composite_gen(request):
    for i in range(3):
        Person1 = data_entity("Person", "name", 
                info=composite(
                    Random.last_name,
                    generator(Random.fixed_length_number, length=i+1),
                    103
                )
        )
        print(Person1(name='Mac'))

def simple_concat(in_iter):
    return " ".join(str(i) for i in in_iter)

@test
def check_entity_with_composite_gen_func_composer(request):
    for i in range(3):
        Person1 = data_entity("Person", "name", 
                info=composite(
                    Random.last_name,
                    generator(Random.fixed_length_number, length=i+1),
                    103,
                    composer=simple_concat
                )
        )
        print(Person1(name='Mac'))

def concat(in_iter, delimiter):
    out = in_iter[0] + delimiter
    value = sum([int(i) for i in in_iter[1:]])
    out += str(value)
    return out

@test
def check_entity_with_composite_gen_arg_composer(request):
    for i in range(3):
        Person1 = data_entity("Person", "name", 
                info=composite(
                    Random.last_name,
                    generator(Random.fixed_length_number, length=i+1),
                    103,
                    composer=composer(concat, "::")
                )
        )
        print(Person1(name='Mac'))