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
from arjuna.tpi.helper.arjtype import _ArDict
from jsonpath_rw import jsonpath, parse
from typing import Any

from arjuna.tpi.tracker import track

class JsonList:
    '''
        Arjuna's Json List object.
    '''

    def __init__(self, pylist: list=None):
        self.__list = pylist

@track("debug")
class JsonDict(_ArDict):
    '''
        Arjuna's Json Object.

        Supports dictionary methods as well as **.** access for key.

        Arguments:
            pydict: Python dict.
    '''

    def __init__(self, pydict: dict=None):
        super().__init__(pydict)

    def _process_key(self, key: str):
        return key

    def find(self, query) -> Any:
        '''
            Find element(s) with JsonPath.

            Arguments:
                map: Python dict

            Returns:
                Any object depending on the query.
        '''

        jsonpath_expr = parse(query)
        return [match.value for match in jsonpath_expr.find(self.store)]

    def __getitem__(self, query):
        return self.find(query)

class Json:
    '''
        Helper class to create Arjuna's Json object or list.
    '''

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
        if type(jobj) is dict:
            return JsonDict(jobj)
        elif type(jobj) is list:
            return JsonList(jobj)
        elif jobj is None:
            return JsonDict()

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



    
