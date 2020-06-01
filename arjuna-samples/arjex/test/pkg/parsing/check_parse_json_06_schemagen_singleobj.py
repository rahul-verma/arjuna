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
def check_no_object(request, builder):
    __assert_result(request, builder, {})


@test
def check_string(request, builder):
    builder.object("string")
    __assert_result(request, builder, {"type": "string"})


@test
def check_integer(request, builder):
    builder.object(1)
    __assert_result(request, builder, {"type": "integer"})


@test
def check_number(request, builder):
    builder.object(1.1)
    __assert_result(request, builder, {"type": "number"})


@test
def check_boolean(request, builder):
    builder.object(True)
    __assert_result(request, builder, {"type": "boolean"})


@test
def check_null(request, builder):
    builder.object(None)
    __assert_result(request, builder, {"type": "null"})


# Array List

@test
def check_empty(request, builder):
    builder.object([])
    __assert_result(request, builder, {"type": "array"})


@test
def check_monotype(request, builder):
    builder.object(["spam", "spam", "spam", "eggs", "spam"])
    __assert_result(request, builder, {"type": "array", "items": {"type": "string"}})


@test
def check_multitype(request, builder):
    builder.object([1, "2", None, False])
    __assert_result(request, builder, {
            "type": "array",
            "items": {
                "type": ["boolean", "integer", "null", "string"]}
        })


@test
def check_nested(request, builder):
    builder.object([
            ["surprise"],
            ["fear", "surprise"],
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


# Test Add Object

@test
def check_empty_object(request, builder):
    builder.object({})
    __assert_result(request, builder, {"type": "object"})


@test
def check_basic_object(request, builder):
    builder.object({
            "Red Windsor": "Normally, but today the van broke down.",
            "Stilton": "Sorry.",
            "Gruyere": False})
    __assert_result(request, builder, {
            "required": ["Gruyere", "Red Windsor", "Stilton"],
            "type": "object",
            "properties": {
                "Red Windsor": {"type": "string"},
                "Gruyere": {"type": "boolean"},
                "Stilton": {"type": "string"}
            }
        })


# Test Complex

@test
def check_array_in_object(request, builder):
    builder.object({"a": "b", "c": [1, 2, 3]})
    __assert_result(request, builder, {
            "required": ["a", "c"],
            "type": "object",
            "properties": {
                "a": {"type": "string"},
                "c": {
                    "type": "array",
                    "items": {"type": "integer"}
                }
            }
        })


@test
def check_object_in_array(request, builder):
    builder.object([
            {"name": "Sir Lancelot of Camelot",
             "quest": "to seek the Holy Grail",
             "favorite colour": "blue"},
            {"name": "Sir Robin of Camelot",
             "quest": "to seek the Holy Grail",
             "capitol of Assyria": None}])
    __assert_result(request, builder, {
            "type": "array",
            "items": {
                "type": "object",
                "required": ["name", "quest"],
                "properties": {
                    "quest": {"type": "string"},
                    "name": {"type": "string"},
                    "favorite colour": {"type": "string"},
                    "capitol of Assyria": {"type": "null"}
                }
            }
        })


@test
def check_three_deep(request, builder):
    builder.object({"matryoshka": {"design": {"principle": "FTW!"}}})
    __assert_result(request, builder, {
            "type": "object",
            "required": ["matryoshka"],
            "properties": {
                "matryoshka": {
                    "type": "object",
                    "required": ["design"],
                    "properties": {
                        "design": {
                            "type": "object",
                            "required": ["principle"],
                            "properties": {
                                "principle": {"type": "string"}
                            }
                        }
                    }
                }
            }
        })
