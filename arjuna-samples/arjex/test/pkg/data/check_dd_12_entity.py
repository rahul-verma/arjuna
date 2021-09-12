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

@test
def check_basic_data_entity(request):
    Person = data_entity("Person", "name age")
    person = Person(name="Rahul", age=99)
    from arjuna.tpi.data.entity import _DataEntity
    print(person, isinstance(person, _DataEntity), issubclass(person.__class__, _DataEntity))

@test
def check_basic_data_entity_del_attr(request):
    Person = data_entity("Person", "name age gender")
    person = Person(name="R", age=99, gender="m")
    print(person)

@test
def check_wrong_attr_data_entity(request):
    Person = data_entity("Person", "name age")
    try:
        person = Person(name="Rahul", age=99, not_allowed=123)
    except Exception as e:
        assert str(e).find("Wrong arguments") != -1
    else:
        request.asserter.fail("Failed")

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
def check_entity_with_spchars(request):
    v1 = generator(
                            Random.ustr, 
                            prefix='with non ascii chars ÄÖÜ@€!§$%/()=?``', 
                            maxlen=50
                    ).generate()
    print(v1)

@test
def check_entity_with_simple_gen_args(request):
    for i in range(3):
        Person1 = data_entity("Person", "name age", debt=generator(Random.fixed_length_number, length=i+1))
        print(Person1(name='Mac', age=21))

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
        Person = data_entity("Person", "name", 
                info=composite(
                    Random.last_name,
                    generator(Random.fixed_length_number, length=i+1),
                    103,
                    composer=composer(concat, "::")
                )
        )
        print(Person(name='Mac'))


@test
def check_entity_with_one_base(request):
    # Simple base with one mandatory and one optional attr
    Person1 = data_entity("Person1", "age", fname=Random.first_name)

    # Top entity adds a mandatory attr
    Person2 = data_entity("Person2", "gender", bases=Person1)
    print(Person2(gender="M", age=20))
    print(Person2(gender="M", age=20, fname="Roy"))

    # Top entity adds an optional attr
    Person3 = data_entity("Person3", "gender", city=Random.city, bases=Person1)
    print(Person3(gender="M", age=20, fname="Roy"))
    print(Person3(gender="M", age=20, fname="Roy", city="Bengaluru"))

    # Top entity makes a field mandatory (optional in base)
    Person4 = data_entity("Person4", "gender fname", city=Random.city, bases=Person1)
    try:
        print(Person4(gender="M", age=20))
    except Exception as e:
        assert str(e).find("Wrong arguments") != -1
    else:
        request.asserter.fail("Failed")
    print(Person4(gender="M", age=20, fname="Roy"))

    # Top entity makes a mandatory field optional
    Person5 = data_entity("Person5", "gender fname", age=generator(Random.fixed_length_number, length=2), city=Random.city, bases=Person1)
    print(Person5(gender="M", fname="Roy"))


@test
def check_entity_with_two_base(request):
    # Simple base1 with one mandatory and one optional attr
    Person1 = data_entity("Person1", "age", fname=Random.first_name)

    # Base 2 adds one mandatory arg, makes fname mandatory, adds one optional arg
    Person2 = data_entity("Person2", "gender fname", city=Random.city, bases=Person1)

    # Top entity makes age optional, add one mandatory parameter
    Person5 = data_entity("Person5", "country", age=generator(Random.fixed_length_number, length=2), bases=(Person1, Person2))
    print(Person5(gender="M", fname="Roy", country="India"))
    print(Person5(gender="M", fname="Roy", age=15, country="India"))

@test
def check_simple_merged_entity(request):
    Person = data_entity("Person", "age", fname=Random.first_name)
    Address = data_entity("Address", city=Random.city, country=Random.country, postal_code=Random.postal_code)

    # Merged Entity
    PersonWithAddress = data_entity("PersonWithAddress", bases=(Person, Address))
    print(PersonWithAddress(age=40))

Person = data_entity("Person", "name age gender")

@test
def check_basic_data_entity_dict_behavior_1(request):
    person = Person(name="R", age=99, gender="m")
    print(person['name'])

@test
def check_basic_data_entity_dict_behavior_2_1(request):
    person = Person(name="R", age=99, gender="m")
    def f(**kwargs):
        print(kwargs)
    f(**person)

@test
def check_basic_data_entity_dict_behavior_2_2(request):
    person = Person(name="R", age=99, gender=None)
    def f(**kwargs):
        print(kwargs)
    f(**person)


@test
def check_basic_data_entity_dict_behavior_3_1(request):
    person = Person(name="R", age=99, gender="m")
    for k,v in person.items():
        print(k,v)

@test
def check_basic_data_entity_dict_behavior_3_2(request):
    person = Person(name="R", age=99, gender=None)
    for k,v in person.items():
        print(k,v)

@test
def check_basic_data_entity_dict_behavior_3_3(request):
    person = Person(name="R", age=99, gender=None)
    for k,v in person.items(remove_none=False):
        print(k,v)

@test
def check_basic_data_entity_dict_behavior_3_4(request):
    person = Person(name="R", age=99, gender=None)
    for k,v in person.items(remove="age"):
        print(k,v)

@test
def check_basic_data_entity_dict_behavior_4_1(request):
    person = Person(name="R", age=99, gender="m")
    print(len(person))

@test
def check_basic_data_entity_dict_behavior_4_2(request):
    person = Person(name="R", age=99, gender=None)
    print(person.size())

@test
def check_basic_data_entity_dict_behavior_4_3(request):
    person = Person(name="R", age=99, gender=None)
    print(person.size(remove_none=False))

@test
def check_basic_data_entity_dict_behavior_5_1(request):
    person = Person(name="R", age=99, gender="m")
    print(person.items())

@test
def check_basic_data_entity_dict_behavior_5_2(request):
    person = Person(name="R", age=99, gender=None)
    print(person.items())

@test
def check_basic_data_entity_dict_behavior_5_3(request):
    person = Person(name="R", age=99, gender=None)
    print(person.items(remove_none=False))

@test
def check_basic_data_entity_dict_behavior_6_1(request):
    person = Person(name="R", age=99, gender="m")
    print(person.keys())

@test
def check_basic_data_entity_dict_behavior_6_2(request):
    person = Person(name="R", age=99, gender=None)
    print(person.keys())

@test
def check_basic_data_entity_dict_behavior_6_3(request):
    person = Person(name="R", age=99, gender=None)
    print(person.keys(remove_none=False))

@test
def check_basic_data_entity_mmutable_1(request):
    person = Person(name="R", age=99, gender="m")
    person.age = 12
    print(person)

@test
def check_basic_data_entity_mutable_2(request):
    person = Person(name="R", age=99, gender="m")
    person['age'] = 12
    print(person)

@test(xfail=True)
def check_basic_data_entity_mutable_but_delnotallowed(request):
    person = Person(name="R", age=99, gender="m")
    del person['age']

@test(xfail=True)
def check_basic_data_entity_immutable_1(request):
    person = Person(name="R", age=99, gender="m", freeze=True)
    person.age = 15

@test(xfail=True)
def check_basic_data_entity_immutable_2(request):
    person = Person(name="R", age=99, gender="m", freeze=True)
    person['age'] = 15