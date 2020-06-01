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

# The tests are based on tests for jsonpath-rw-ext in https://github.com/wolverdude/GenSON

from arjuna import *

@for_test
def builder(request):
    yield JsonSchema.builder()

def __assert_result(request, builder, expected):
    actual = builder.build().as_dict()
    del actual['$schema']
    request.asserter.assert_equal(actual, expected, 'Generated schema (below) does not match expected (above)')

@test
def check_single_type(request, builder):
    schema = {'type': 'null'}
    builder.schema(schema)
    __assert_result(request, builder, schema)


@test
def check_single_type_unicode(request, builder):
    schema = {u'type': u'string'}
    builder.schema(schema)
    __assert_result(request, builder, schema)


@test
def check_typeless(request, builder):
    schema = {}
    builder.schema(schema)
    __assert_result(request, builder, schema)


@test
def check_array_type_no_items(request, builder):
    schema = {'type': 'array'}
    builder.schema(schema)
    __assert_result(request, builder, schema)


# Test anyOf

@test
def check_multi_type(request, builder):
    schema = {'type': ['boolean', 'null', 'number', 'string']}
    builder.schema(schema)
    __assert_result(request, builder, schema)


@test
def check_multi_type_with_extra_keywords(request, builder):
    schema = {'type': ['boolean', 'null', 'number', 'string'],
                  'title': 'this will be duplicated'}
    builder.schema(schema)
    __assert_result(request, builder, {'anyOf': [
            {'type': 'boolean', 'title': 'this will be duplicated'},
            {'type': 'null', 'title': 'this will be duplicated'},
            {'type': 'number', 'title': 'this will be duplicated'},
            {'type': 'string', 'title': 'this will be duplicated'}
        ]})


@test
def check_anyof(request, builder):
    schema = {"anyOf": [
            {"type": "null"},
            {"type": "boolean", "title": "Gruyere"}
        ]}

    builder.schema(schema)
    __assert_result(request, builder, schema)


@test
def check_recursive(request, builder):
    schema = {"anyOf": [
            {"type": ["integer", "string"]},
            {"anyOf": [
                {"type": "null"},
                {"type": "boolean", "title": "Gruyere"}
            ]}
        ]}

    builder.schema(schema)
    # recursive anyOf will be flattened
    __assert_result(request, builder, {"anyOf": [
        {"type": ["integer", "null", "string"]},
        {"type": "boolean", "title": "Gruyere"}
    ]})

# Test required

@test
def check_required(request, builder):
    schema = {'type': 'object', 'required': []}

    builder.schema(schema)
    __assert_result(request, builder, schema)

# Test Preserve Extra Keywords

@test
def check_basic_type(request, builder):
    schema = {'type': 'boolean', 'const': False, 'myKeyword': True}

    builder.schema(schema)
    __assert_result(request, builder, schema)


@test
def check_number(request, builder):
    schema = {'type': 'number', 'const': 5, 'myKeyword': True}

    builder.schema(schema)
    __assert_result(request, builder, schema)


@test
def check_list(request, builder):
    schema = {'type': 'array', 'items': {"type": "null"},
                  'const': [], 'myKeyword': True}

    builder.schema(schema)
    __assert_result(request, builder, schema)


@test
def check_object(request, builder):
    schema = {'type': 'object', 'const': {}, 'myKeyword': True}

    builder.schema(schema)
    __assert_result(request, builder, schema)


@test
def check_typeless(request, builder):
    schema = {'const': 5, 'myKeyword': True}

    builder.schema(schema)
    __assert_result(request, builder, schema)