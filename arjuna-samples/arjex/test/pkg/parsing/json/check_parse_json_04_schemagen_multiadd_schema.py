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
    builder.schema(schema)
    __assert_result(request, builder, schema)


@test
def check_single_type_unicode(request, builder):
    schema = {u'type': u'string'}
    builder.schema(schema)
    builder.schema(schema)
    __assert_result(request, builder, schema)


@test
def check_redundant_integer_type(request, builder):
    builder.schema({'type': 'integer'})
    builder.schema({'type': 'number'})
    __assert_result(request, builder, {'type': 'number'})


@test
def check_typeless(request, builder):
    schema1 = {"title": "ambiguous schema"}
    schema2 = {"grail": "We've already got one"}
    builder.schema(schema1)
    builder.schema(schema2)
    result = dict(schema1)
    result.update(schema2)
    __assert_result(request, builder, result)

@test
def check_typeless_incorporated(request, builder):
    schema1 = {"title": "Gruyere"}
    schema2 = {"type": "boolean"}
    builder.schema(schema1)
    builder.schema(schema2)
    __assert_result(request, builder, {"type": "boolean", "title": "Gruyere"})


@test
def check_typeless_instantly_incorporated(request, builder):
    schema1 = {"type": "boolean"}
    schema2 = {"title": "Gruyere"}
    builder.schema(schema1)
    builder.schema(schema2)
    __assert_result(request, builder, {"type": "boolean", "title": "Gruyere"})


# Test anyOf

@test
def check_multi_type(request, builder):
    builder.schema({'type': 'boolean'})
    builder.schema({'type': 'null'})
    builder.schema({'type': 'string'})
    __assert_result(request, builder, {'type': ['boolean', 'null', 'string']})


@test
def check_anyof_generated(request, builder):
    schema1 = {"type": "null", "title": "African or European Swallow?"}
    schema2 = {"type": "boolean", "title": "Gruyere"}
    builder.schema(schema1)
    builder.schema(schema2)
    __assert_result(request, builder, {"anyOf": [
            schema1,
            schema2
        ]})


@test
def check_anyof_seeded(request, builder):
    schema1 = {"type": "null", "title": "African or European?"}
    schema2 = {"type": "boolean", "title": "Gruyere"}
    builder.schema({"anyOf": [
            {"type": "null"},
            schema2
        ]})
    builder.schema(schema1)
    __assert_result(request, builder, {"anyOf": [
            schema1,
            schema2
        ]})


@test
def check_list_plus_tuple(request, builder):
    schema1 = {"type": "array", "items": {"type": "null"}}
    schema2 = {"type": "array", "items": [{"type": "null"}]}
    builder.schema(schema1)
    builder.schema(schema2)
    __assert_result(request, builder, {"anyOf": [
            schema1,
            schema2
        ]})

@test
def check_multi_type_and_anyof(request, builder):
    schema1 = {'type': ['boolean', 'null', 'string']}
    schema2 = {"type": "boolean", "title": "Gruyere"}
    builder.schema(schema1)
    builder.schema(schema2)
    __assert_result(request, builder, {"anyOf": [
            {'type': ['null', 'string']},
            schema2
        ]})


# Test required

@test
def check_combines(request, builder):
    schema1 = {"type": "object", "required": [
            "series of statements", "definite proposition"]}
    schema2 = {"type": "object", "required": ["definite proposition"]}

    builder.schema(schema1)
    builder.schema(schema2)
    __assert_result(request, builder, {"type": "object", "required": [
            "definite proposition"]})


@test
def check_ignores_missing(request, builder):
    schema1 = {"type": "object"}
    schema2 = {"type": "object", "required": ["definite proposition"]}

    builder.schema(schema1)
    builder.schema(schema2)
    __assert_result(request, builder, {"type": "object", "required": [
            "definite proposition"]})


@test
def check_omits_all_missing(request, builder):
    schema1 = {"type": "object", "properties": {"spam": {}}}
    schema2 = {"type": "object", "properties": {"eggs": {}}}

    builder.schema(schema1)
    builder.schema(schema2)
    __assert_result(request, builder,  {"type": "object", "properties": {"spam": {}, "eggs": {}}})



@test
def check_maintains_empty(request, builder):
    seed = {"required": []}
    schema1 = {"type": "object", "required": ["series of statements"]}
    schema2 = {"type": "object", "required": ["definite proposition"]}

    builder.schema(seed)
    builder.schema(schema1)
    builder.schema(schema2)
    __assert_result(request, builder,  {"type": "object", "required": []})


