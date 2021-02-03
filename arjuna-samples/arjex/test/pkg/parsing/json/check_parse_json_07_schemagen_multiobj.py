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
    builder.object("bacon")
    builder.object("egg")
    builder.object("spam")
    __assert_result(request, builder, {"type": "string"})


@test
def check_redundant_integer_type(request, builder):
    builder.object(1)
    builder.object(1.1)
    __assert_result(request, builder, {"type": "number"})


# Test anyOf

@test
def check_simple(request, builder):
    builder.object("string")
    builder.object(1.1)
    builder.object(True)
    builder.object(None)
    __assert_result(request, builder, {"type": ["boolean", "null", "number", "string"]})


@test
def check_complex(request, builder):
    builder.object({})
    builder.object([None])
    __assert_result(request, builder, {"anyOf": [
            {"type": "object"},
            {"type": "array", "items": {"type": "null"}}
        ]})


@test
def check_simple_and_complex(request, builder):
    builder.object(None)
    builder.object([None])
    __assert_result(request, builder, {"anyOf": [
            {"type": "null"},
            {"type": "array", "items": {"type": "null"}}
        ]})


# Array List

@test
def check_empty(request, builder):
    builder.object([])
    builder.object([])
    __assert_result(request, builder, {"type": "array"})


@test
def check_monotype(request, builder):
    builder.object(["spam", "spam", "spam", "eggs", "spam"])
    builder.object(["spam", "spam", "spam", "eggs"])
    __assert_result(request, builder, {"type": "array", "items": {"type": "string"}})


@test
def check_multitype(request, builder):
    builder.object([1, "2", "3", None, False])
    builder.object([1, 2, "3", False])
    __assert_result(request, builder, {
            "type": "array",
            "items": {
                "type": ["boolean", "integer", "null", "string"]}
        })


@test
def check_nested(request, builder):
    builder.object([
            ["surprise"],
            ["fear", "surprise"]
        ])
    builder.object([
            ["fear", "surprise", "ruthless efficiency"],
            ["fear", "surprise", "ruthless efficiency",
             "an almost fanatical devotion to the Pope"]
        ])
    __assert_result(request, builder, {
            "type": "array",
            "items": {
                "type": "array",
                "items": {"type": "string"}}
        })


# Adding Schema as well as object

@test
def check_empty_2(request, builder):
    builder.schema({"type": "array", "items": []})
    builder.object([])
    builder.object([])
    __assert_result(request, builder, {"type": "array", "items": [{}]})


@test
def check_multitype_2(request, builder):
    builder.schema({"type": "array", "items": []})
    builder.object([1, "2", "3", None, False])
    builder.object([1, 2, "3", False])
    __assert_result(request, builder, {
            "type": "array",
            "items": [
                {"type": "integer"},
                {"type": ["integer", "string"]},
                {"type": "string"},
                {"type": ["boolean", "null"]},
                {"type": "boolean"}]
        })


@test
def check_nested_2(request, builder):
    builder.schema({"type": "array", "items": {"type": "array", "items": []}})
    builder.object([
            ["surprise"],
            ["fear", "surprise"]
        ])
    builder.object([
            ["fear", "surprise", "ruthless efficiency"],
            ["fear", "surprise", "ruthless efficiency",
             "an almost fanatical devotion to the Pope"]
        ])
    __assert_result(request, builder, {
            "type": "array",
            "items": {
                "type": "array",
                "items": [
                    {"type": "string"},
                    {"type": "string"},
                    {"type": "string"},
                    {"type": "string"}
                ]
            }
        })


