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

import json
import copy
from arjuna.tpi.helper.arjtype import _ArDict
from jsonpath_rw import jsonpath, parse
from typing import Any

from arjuna.tpi.tracker import track
from arjuna.tpi.engine.asserter import AsserterMixIn

@track("trace")
class JsonList(AsserterMixIn):
    '''
        Arjuna's Json List object.
    '''

    def __init__(self, pylist: list=None):
        super().__init__()
        self.__list = pylist

    def __str__(self):
        return str(self.__list)

    def __getitem__(self, index):
        return Json.convert_to_json_element(self.__list[index], allow_any=True)

    def is_empty(self):
        return len(self.__list) == 0

    def assert_empty(self):
        if not self.is_empty():
            raise AssertionError("JsonList is not empty. Length: {}".format(len(self.__list)))

    def assert_not_empty(self):
        if self.is_empty():
            raise AssertionError(f"JsonList is empty.")

    def assert_size(self, size):
        length = len(self)
        if length != size:
            raise AssertionError(f"JsonList is not of expected size. Expected: {size}. Actual: {length}")

    def assert_min_size(self, size):
        length = len(self)
        if length < size:
            raise AssertionError(f"JsonList is not of minimum expected size. Expected minimum size is {size}. Actual: {length}")

    def assert_max_size(self, size):
        length = len(self)
        if length > size:
            raise AssertionError(f"JsonList is not of maximum expected size. Expected maximum size is {size}. Actual: {length}")

    def assert_size_range(self, min_size, max_size):
        length = len(self)
        if length < min_size or length > max_size:
            raise AssertionError(f"JsonList is not in expected size range. Expected maximum size is {size}. Actual: {length}")

    @property
    def size(self):
        return len(self)

    @property
    def raw_object(self):
        return copy.deepcopy(self.__list)

    def __str__(self):
        return str(self.__list)

    def __len__(self):
        return len(self.__list)

    def __eq__(self, other):
        if type(other) is list:
            pass
        elif type(other) is JsonList:
            other = other.raw_object
        elif other is None:
            return False
        else:
            raise Exception("JsonList == operator expects list/JsonList as right operand.")

        if len(self) != len(other):
            return False
        else:
            return self.raw_object == other

class JsonSchema:

    def __init__(self, schema_dict):
        self.__dict = schema_dict

    def mark_optional(self, *keys):
        for key in keys:
            if 'required' in self.__dict:
                try:
                    self.__dict['required'].remove(key)
                except ValueError:
                    pass

    def allow_null(self, *keys):
        for key in keys:
            if key in self.__dict['properties']:
                target_dict = self.__dict['properties'][key]
                if 'type' in target_dict:
                    type_value = target_dict['type']
                    if type(type_value) is str:
                        self.__dict['properties'][key]['type'] = [type_value, "null"]
                    else:
                        self.__dict['properties'][key]['type'].append('null')
                elif 'anyOf' in target_dict:
                    if {"type": "null"} not in target_dict['anyOf']:
                        target_dict['anyOf'].append({"type": "null"})                   

    def as_dict(self):
        return self.__dict

    def __str__(self):
        return json.dumps(self.__dict, indent=2)


@track("trace")
class JsonDict(_ArDict, AsserterMixIn):
    '''
        Arjuna's Json Object.

        Supports dictionary methods as well as **.** access for key.

        Arguments:
            pydict: Python dict.
    '''

    def __init__(self, pydict: dict=None):
        _ArDict.__init__(self, pydict)
        AsserterMixIn.__init__(self)

    @property
    def size(self):
        return len(self)

    @property
    def raw_object(self):
        return dict(super().items())

    def _process_key(self, key: str):
        return key

    def findall(self, query) -> list:
        '''
            Find all elements with JsonPath.

            Arguments:
                query: JsonPath Query string

            Returns:
                python list of found Json elements.
        '''

        jsonpath_expr = parse(query)
        return [Json.convert_to_json_element(match.value, allow_any=True) for match in jsonpath_expr.find(self.store)]


    def find(self, query) -> Any:
        '''
            Find first element with JsonPath.

            Arguments:
                query: JsonPath Query string

            Returns:
                A Json element.
        '''
        results = self.findall(query)
        if not results:
            raise Exception(f"A Json element could not be found with {query}")
        return results[0]


    def __getitem__(self, query):
        return self.find(query)

    def is_empty(self):
        return len(self) == 0

    def assert_empty(self):
        if not self.is_empty():
            raise AssertionError("JsonDict is not empty. Length: {}".format(len(self)))

    def assert_not_empty(self):
        if self.is_empty():
            raise AssertionError(f"JsonDict is empty.")

    def assert_size(self, size):
        length = len(self)
        if length != size:
            raise AssertionError(f"JsonDict is not of expected size. Expected: {size}. Actual: {length}")

    def assert_min_size(self, size):
        length = len(self)
        if length < size:
            raise AssertionError(f"JsonDict is not of minimum expected size. Expected minimum size is {size}. Actual: {length}")

    def assert_max_size(self, size):
        length = len(self)
        if length > size:
            raise AssertionError(f"JsonDict is not of maximum expected size. Expected maximum size is {size}. Actual: {length}")

    def assert_size_range(self, min_size, max_size):
        length = len(self)
        if length < min_size or length > max_size:
            raise AssertionError(f"JsonDict is not in expected size range. Expected maximum size is {size}. Actual: {length}")

    def assert_contents(self, *, msg, **kwargs):
        for k,v in kwargs.items():
            self.asserter.assert_equal(Json.convert_to_json_element(self[k], allow_any=True), v, msg=msg)

    def assert_keys_present(self, *keys, msg):
        for key in keys:
            self.asserter.assert_true(key in self, "Expected key absent. " + msg)

    def matches_schema(self, schema):
        if isinstance(schema, JsonSchema):
            schema = schema.as_dict()
        from jsonschema import Draft7Validator
        validator = Draft7Validator(schema)
        errors = []
        for error in sorted(validator.iter_errors(self.store), key=str):
            errors.append("Key >>{}<<: {}".format(".".join(error.path), error.message))
        if errors:
            return False, errors
        else:
            return True, None

    def assert_schema(self, schema, *, msg):
        matched, errors = self.matches_schema(schema)
        if not matched:
            raise AssertionError("JsonDict does not match schema. Found the following errors. {}".format(". ".join(errors)))

    def assert_match_schema(self, jobj, *, msg):
        matched, errors = self.matches_schema(Json.extract_schema(jobj))
        if not matched:
            raise AssertionError("JsonDict does not match schema. Found the following errors. {}".format(". ".join(errors)))

    def assert_match(self, expected_dict, *, msg, ignore=None):
        if type(expected_dict) is dict:
            expected_dict = JsonDict(expected_dict)
        elif type(expected_dict) is JsonDict:
            pass
        else:
            raise Exception("JsonDict.assert_match expected_dict argument should be a dictionary or a JsonDict object.")
        if ignore is None:
            ignore = set()
        elif type(ignore) in {set, dict, list, tuple}:
            ignore = set([i.lower() for i in ignore])
        else:
            ignore = {str(ignore).lower()}
        for k,v in self.items():
            if k.lower() not in ignore:
                self.asserter.assert_equal(Json.convert_to_json_element(v, allow_any=True), expected_dict[k], msg=msg)

    @property
    def schema(self):
        return Json.extract_schema(self)

    def __eq__(self, other):
        if type(other) is dict:
            pass
        elif type(other) is JsonDict:
            other = other.raw_object
        elif other is None:
            return False
        else:
            raise Exception("JsonDict == operator expects dict/JsonDict as right operand.")

        if len(self) != len(other):
            return False
        else:
            return self.raw_object == other

class Json:
    '''
        Helper class to create Arjuna's Json elements.
    '''

    @classmethod
    def convert_to_json_element(cls, jobj, allow_any=False):
        if type(jobj) is dict:
            return JsonDict(jobj)
        elif type(jobj) is list:
            return JsonList(jobj)

        if allow_any:
            return jobj
        else:
            raise Exception(f"Not able to convert provided string {jobj} into any appropriate Json element.")

    @classmethod
    def from_str(cls, json_str: str) -> 'JsonDictOrList':
        '''
            Creates a Json object from a JSON string.

            Arguments:
                file_path: Absolute path of the json file.

            Returns:
                Arjuna's `JsonDict` or `JsonList` object
        '''
        jobj = json.loads(json_str)
        return cls.convert_to_json_element(jobj)


    @classmethod
    def from_file(cls, file_path: str) -> 'JsonDictOrList':
        '''
            Creates a Json object from file.

            Arguments:
                file_path: Absolute path of the json file.

            Returns:
                Arjuna's `JsonDict` or `JsonList` object
        '''

        with open(file_path, 'r') as f:
            return cls.from_str(f.read())

    @classmethod
    def from_map(cls, map: dict) -> JsonDict:
        '''
            Creates a JsonDict object from Python dictionary.

            Arguments:
                map: Python dict

            Returns:
                Arjuna's `JsonDict` object
        '''

        return JsonDict(d)

    @classmethod
    def from_iter(cls, iter) -> JsonList:
        '''
            Creates a Json object from Python dictionary.

            Arguments:
                iter: Python iterable

            Returns:
                Arjuna's `JsonList` object
        '''

        return JsonList(list(iter))

    @classmethod
    def assert_list_type(cls, obj):
        if not isinstance(obj, list) and not isinstance(obj, JsonList):
            raise AssertionError("Object {} is not a list.".format(str(obj)))

    @classmethod
    def assert_dict_type(cls, obj):
        if not isinstance(obj, dict) and not isinstance(obj, JsonDict):
            raise AssertionError("Object {} is not a dict.".format(str(obj)))

    @classmethod
    def extract_schema(cls, jobj_or_str):
        if type(jobj_or_str) is str:
            jobj = cls.from_str(jobj_or_str.strip())
        else:
            jobj = jobj_or_str
        from genson import SchemaBuilder
        builder = SchemaBuilder()
        if type(jobj) in {JsonDict, JsonList}:
            builder.add_object(jobj.raw_object)
        else:
            builder.add_object(jobj)
        return JsonSchema(builder.to_schema())

    
