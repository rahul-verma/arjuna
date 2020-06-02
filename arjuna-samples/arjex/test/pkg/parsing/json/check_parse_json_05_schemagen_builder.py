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
from genson import SchemaBuilder

@for_test
def builder(request):
    yield JsonSchema.builder()

def __assert_result(request, builder, expected):
    actual = builder.build().as_dict()
    request.asserter.assert_equal(actual, expected, 'Generated schema (below) does not match expected (above)')

@test
def check_uri(request):
    test_uri = 'TEST_URI'
    builder = JsonSchema.builder(schema_uri=test_uri)
    __assert_result(request, builder, {"$schema": test_uri})


@test
def check_null_uri(request):
    builder = JsonSchema.builder(schema_uri=None)
    __assert_result(request, builder, {"$schema": SchemaBuilder.DEFAULT_URI})


# Test Methods

@test
def check_add_schema(request, builder):
    builder.schema({"type": "null"})
    __assert_result(request, builder, {
            "$schema": SchemaBuilder.DEFAULT_URI,
            "type": "null"})


@test
def check_add_object(request, builder):
    builder.object(None)
    __assert_result(request, builder, {
            "$schema": SchemaBuilder.DEFAULT_URI,
            "type": "null"})

@test
def check_as_dict(request, builder):
    assert builder.build().as_dict() == {"$schema": SchemaBuilder.DEFAULT_URI}


@test
def check_add_schema_with_uri_default(request, builder):
    test_uri = 'TEST_URI'
    builder.schema({"$schema": test_uri, "type": "null"})
    __assert_result(request, builder, {"$schema": test_uri, "type": "null"})


@test
def check_add_schema_with_uri_not_defuult(request):
    test_uri = 'TEST_URI'
    builder = JsonSchema.builder(schema_uri=test_uri)
    builder.schema({"$schema": 'BAD_URI', "type": "null"})
    __assert_result(request, builder, {"$schema": test_uri, "type": "null"})


@test
def check_add_schema_with_uri_not_defuult(request):
    test_uri = 'TEST_URI'
    builder = JsonSchema.builder(schema_uri=test_uri)
    builder.schema({"$schema": 'BAD_URI', "type": "null"})
    __assert_result(request, builder, {"$schema": test_uri, "type": "null"})




