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

# The tests are based on tests for jsonpath-rw in https://github.com/kennknowles/python-jsonpath-rw

def __test_cases(test_cases):

    for string, data, target in test_cases:
        print('parse("%s").find(%s) =?= %s' % (string, data, target))
        result = Json.from_object(data, allow_any=True).findall(string)
        print(result)
        assert result == target

@test
def check_fields_value(request):
    Json.reset_auto_id_key()
    __test_cases([ ('foo', {'foo': 'baz'}, ['baz']),
                        ('foo,baz', {'foo': 1, 'baz': 2}, [1, 2]),
                        ('@foo', {'@foo': 1}, [1]),
                        ('*', {'foo': 1, 'baz': 2}, [1, 2]) ])

    Json.set_auto_id_key()
    __test_cases([ ('*', {'foo': 1, 'baz': 2}, [1, 2, '`this`']) ])


@test
def check_root_value(request):
    Json.reset_auto_id_key()
    __test_cases([ 
        ('$', {'foo': 'baz'}, [{'foo':'baz'}]),
        ('foo.$', {'foo': 'baz'}, [{'foo':'baz'}]),
        ('foo.$.foo', {'foo': 'baz'}, ['baz']),
    ])


@test
def check_this_value(request):
    Json.reset_auto_id_key()
    __test_cases([ 
        ('`this`', {'foo': 'baz'}, [{'foo':'baz'}]),
        ('foo.`this`', {'foo': 'baz'}, ['baz']),
        ('foo.`this`.baz', {'foo': {'baz': 3}}, [3]),
    ])


@test
def check_index_value(request):
    __test_cases([
        ('[0]', [42], [42]),
        ('[5]', [42], []),
        ('[2]', [34, 65, 29, 59], [29]),
        # ('[0]', None, [])
    ])


@test
def check_slice_value(request):
    __test_cases([('[*]', [1, 2, 3], [1, 2, 3]),
                        ('[*]', range(1, 4), [1, 2, 3]),
                        ('[1:]', [1, 2, 3, 4], [2, 3, 4]),
                        ('[:2]', [1, 2, 3, 4], [1, 2])])

    # Funky slice hacks
    __test_cases([
        ('[*]', {'foo':1}, [{'foo': 1}]), # This is a funky hack
        ('[*].foo', {'foo':1}, [1]), # This is a funky hack
    ])


@test
def check_child_value(request):
    __test_cases([('foo.baz', {'foo': {'baz': 3}}, [3]),
                        ('foo.baz', {'foo': {'baz': [3]}}, [[3]]),
                        ('foo.baz.bizzle', {'foo': {'baz': {'bizzle': 5}}}, [5])])


@test
def check_descendants_value(request):
    __test_cases([ 
        ('foo..baz', {'foo': {'baz': 1, 'bing': {'baz': 2}}}, [1, 2] ),
        ('foo..baz', {'foo': [{'baz': 1}, {'baz': 2}]}, [1, 2] ), 
    ])


@test
def check_parent_value(request):
    __test_cases([('foo.baz.`parent`', {'foo': {'baz': 3}}, [{'baz': 3}]),
                        ('foo.`parent`.foo.baz.`parent`.baz.bizzle', {'foo': {'baz': {'bizzle': 5}}}, [5])])

#
# Check the "auto_id_field" feature
#

@test
def check_fields_auto_id(request):
    Json.set_auto_id_key()
    __test_cases([ ('foo.id', {'foo': 'baz'}, ['foo']),
                        ('foo.id', {'foo': {'id': 'baz'}}, ['baz']),
                        ('foo,baz.id', {'foo': 1, 'baz': 2}, ['foo', 'baz']),
                        ('*.id', 
                        {'foo':{'id': 1},
                            'baz': 2},
                            ['1', 'baz']) ])


@test
def check_root_auto_id(request):
    Json.set_auto_id_key()
    __test_cases([ 
        ('$.id', {'foo': 'baz'}, ['$']), # This is a wonky case that is not that interesting
        ('foo.$.id', {'foo': 'baz', 'id': 'bizzle'}, ['bizzle']), 
        ('foo.$.baz.id', {'foo': 4, 'baz': 3}, ['baz']),
    ])


@test
def check_this_auto_id(request):
    Json.set_auto_id_key()
    __test_cases([ 
        ('id', {'foo': 'baz'}, ['`this`']), # This is, again, a wonky case that is not that interesting
        ('foo.`this`.id', {'foo': 'baz'}, ['foo']),
        ('foo.`this`.baz.id', {'foo': {'baz': 3}}, ['foo.baz']),
    ])


@test
def check_index_auto_id(request):
    Json.set_auto_id_key()
    __test_cases([('[0].id', [42], ['[0]']),
                        ('[2].id', [34, 65, 29, 59], ['[2]'])])


@test
def check_slice_auto_id(request):
    Json.set_auto_id_key()
    __test_cases([ ('[*].id', [1, 2, 3], ['[0]', '[1]', '[2]']),
                        ('[1:].id', [1, 2, 3, 4], ['[1]', '[2]', '[3]']) ])


@test
def check_child_auto_id(request):
    Json.set_auto_id_key()
    __test_cases([('foo.baz.id', {'foo': {'baz': 3}}, ['foo.baz']),
                        ('foo.baz.id', {'foo': {'baz': [3]}}, ['foo.baz']),
                        ('foo.baz.id', {'foo': {'id': 'bizzle', 'baz': 3}}, ['bizzle.baz']),
                        ('foo.baz.id', {'foo': {'baz': {'id': 'hi'}}}, ['foo.hi']),
                        ('foo.baz.bizzle.id', {'foo': {'baz': {'bizzle': 5}}}, ['foo.baz.bizzle'])])


@test
def check_descendants_auto_id(request):
    Json.set_auto_id_key()
    __test_cases([('foo..baz.id', 
                        {'foo': {
                            'baz': 1, 
                            'bing': {
                                'baz': 2
                            }
                            } },
                            ['foo.baz', 
                            'foo.bing.baz'] )])


