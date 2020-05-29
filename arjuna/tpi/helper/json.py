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

'''
Classes to assist in JSON Parsing. 
'''

import json
import copy
from arjuna.tpi.helper.arjtype import _ArDict
from jsonpath_rw import jsonpath, parse
from typing import Any

from arjuna.tpi.tracker import track
from arjuna.tpi.engine.asserter import AsserterMixIn, IterableAsserterMixin

@track("trace")
class JsonList(AsserterMixIn, IterableAsserterMixin):
    '''
        Encapsulates a list object in Json.

        Arguments:
            list: Python list

        Note:
            Supports indexing just like a Python list.

            Also supports == operator. Right operand can be a Python list or a `JsonList` object.
    '''

    def __init__(self, pylist: list):
        AsserterMixIn.__init__(self)
        IterableAsserterMixin.__init__(self)
        self.__list = pylist
        if pylist is None:
            self.__list = list()
        self._container = self.__list

    def __getitem__(self, index):
        return Json.from_object(self.__list[index], allow_any=True)

    @property
    def size(self):
        '''
            Number of objects in this list.
        '''
        return len(self)

    @property
    def raw_object(self):
        '''
            A copy of the Python list that this object wraps.
        '''
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
    '''
        Encapsulates Json Schema which can be used to validate Json objects.
    '''

    def __init__(self, schema_dict):
        self.__dict = schema_dict

    def mark_optional(self, *keys):
        '''
            Mark the provided keys as optional in the root of Json Schema.

            Arguments:
                *keys: Arbitrary key names
        '''

        for key in keys:
            if 'required' in self.__dict:
                try:
                    self.__dict['required'].remove(key)
                except ValueError:
                    pass

    def allow_null(self, *keys):
        '''
            Allow None as a value type for the provided keys in the root of Json Schema.

            Arguments:
                *keys: Arbitrary key names
        '''

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

    def as_dict(self) -> dict:
        '''
            Get this object as a Python dict.
        '''
        return self.__dict

    def __str__(self):
        return json.dumps(self.__dict, indent=2)


@track("trace")
class JsonDict(_ArDict, AsserterMixIn, IterableAsserterMixin):
    '''
        Encapsualtes Dictionary object in Json.

        Arguments:
            pydict: Python dict.

        Note:
            Supports dictionary methods as well as **.** access for key.

            Also supports == operator. Right operand can be a Python dict or a `JsonDict` object.

    '''

    def __init__(self, pydict: dict=None):
        _ArDict.__init__(self, pydict)
        AsserterMixIn.__init__(self)
        IterableAsserterMixin.__init__(self)
        self._container = self

    @property
    def size(self):
        '''
            Number of key-value pairs in this object.
        '''
        return len(self)

    @property
    def raw_object(self):
        '''
            A copy of the Python dict that this object wraps.
        '''
        return dict(super().items())

    def _process_key(self, key: str):
        return key

    def findall(self, query) -> list:
        '''
            Find all elements with JsonPath query.

            Arguments:
                query: JsonPath Query string

            Returns:
                python list of found Json elements.
        '''

        jsonpath_expr = parse(query)
        return [Json.from_object(match.value, allow_any=True) for match in jsonpath_expr.find(self.store)]


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

    def assert_contents(self, *, msg, **key_values):
        '''
            Assert that the values of provided keys match in the root of this dict.

            Arguments:
                msg: Purpose of this assertion.
                **key_values: Arbitrary key-value pairs to match in the root of this dict.

        '''
        for k,v in key_values.items():
            self.asserter.assert_equal(Json.from_object(self[k], allow_any=True), v, msg=msg)

    def assert_keys_present(self, *keys, msg):
        '''
            Assert that the provided keys are present in the root of this dict.

            Arguments:
                msg: Purpose of this assertion.
                **keys: Key names to assert
        '''
        for key in keys:
            self.asserter.assert_true(key in self, "Expected key absent. " + msg)

    def matches_schema(self, schema):
        '''
            Check if this JsonDict matches the provided schema

            Arguments:
                schema: Python dict schema or `JsonSchema` object.

            Returns:
                A 2-element tuple (True/False, List of error strings in matching)
        '''
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
        '''
            Assert that this JsonDict matches the provided schema.

            Arguments:
                schema: Python dict schema or `JsonSchema` object.

            Keyword Args:
                msg: Purpose of this assertion.
        '''
        matched, errors = self.matches_schema(schema)
        if not matched:
            raise AssertionError("JsonDict does not match schema. Found the following errors. {}".format(". ".join(errors)))

    def assert_match_schema(self, jobj, *, msg):
        '''
            Assert that this JsonDict matches the schema of provided object.

            Arguments:
                jobj: Json string or Python dict/JsonDict

            Keyword Args:
                msg: Purpose of this assertion.
        '''
        matched, errors = self.matches_schema(Json.extract_schema(jobj))
        if not matched:
            raise AssertionError("JsonDict does not match schema. Found the following errors. {}".format(". ".join(errors)))

    def assert_match(self, jobj, *, msg, ignore_keys=None):
        '''
            Assert that this JsonDict matches the provided object.

            Arguments:
                jobj: Python dict/JsonDict

            Keyword Args:
                msg: Purpose of this assertion.
                ignore_keys: Keys to be ignored while matching
        '''
        if type(jobj) is dict:
            jobj = JsonDict(jobj)
        elif type(jobj) is JsonDict:
            pass
        else:
            raise Exception("JsonDict.assert_match expected_dict argument should be a dictionary or a JsonDict object.")
        if ignore_keys is None:
            ignore_keys = set()
        elif type(ignore_keys) in {set, dict, list, tuple}:
            ignore_keys = set([i.lower() for i in ignore_keys])
        else:
            ignore_keys = {str(ignore_keys).lower()}
        for k,v in self.items():
            if k.lower() not in ignore_keys:
                self.asserter.assert_equal(Json.from_object(v, allow_any=True), jobj[k], msg=msg)

    @property
    def schema(self) -> 'JsonSchema':
        '''
            Schema of this object.
        '''
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
    def from_object(cls, jobj, *, allow_any=False):
        '''
            Convert a Python object to a JsonDict/JsonList object if applicable.

            Keyword Arguments:
                allow_any: If True, if the object can not be coverted, same object is returned, else an Exception is raised.
        '''
        if type(jobj) is dict:
            return JsonDict(jobj)
        elif type(jobj) is list:
            return JsonList(jobj)

        if allow_any:
            return jobj
        else:
            raise Exception(f"Not able to convert provided string {jobj} into any appropriate Json element.")

    @classmethod
    def from_str(cls, json_str: str, allow_any: bool=False) -> 'JsonDictOrList':
        '''
            Creates a Json object from a JSON string.

            Arguments:
                file_path: Absolute path of the json file.
                allow_any: If True, if the object can not be coverted to a JsonDict/JsonList, same object is returned, else an Exception is raised.

            Returns:
                Arjuna's `JsonDict` or `JsonList` object
        '''
        jobj = json.loads(json_str)
        return cls.from_object(jobj, allow_any=allow_any)

    @classmethod
    def from_file(cls, file_path: str, allow_any: bool=False) -> 'JsonDictOrList':
        '''
            Creates a Json object from file.

            Arguments:
                file_path: Absolute path of the json file.
                allow_any: If True, if the object can not be coverted to a JsonDict/JsonList, same object is returned, else an Exception is raised.

            Returns:
                Arjuna's `JsonDict` or `JsonList` object
        '''

        with open(file_path, 'r') as f:
            return cls.from_str(f.read(), allow_any=allow_any)

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
    def assert_list_type(cls, obj, *, msg):
        '''
            Assert that the provided object is a Python list or `JsonList` object.

            Keyword Args:
                msg: Purpose of this assertion.
        '''
        if not isinstance(obj, list) and not isinstance(obj, JsonList):
            raise AssertionError("Object {} is not a list. {}".format(str(obj), msg))

    @classmethod
    def assert_dict_type(cls, obj, *, msg):
        '''
            Assert that the provided object is a Python dict or `JsonDict` object.

            Keyword Args:
                msg: Purpose of this assertion.
        '''
        if not isinstance(obj, dict) and not isinstance(obj, JsonDict):
            raise AssertionError("Object {} is not a dict. {}".format(str(obj), msg))

    @classmethod
    def extract_schema(cls, jobj_or_str) -> JsonSchema:
        '''
            Extracts schema from provide Json object or string to create a `JsonSchema` object.

            Arguments:
                jobj_or_str: JsonDict/JsonList or a Python str/list/dict.

        '''
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

    
