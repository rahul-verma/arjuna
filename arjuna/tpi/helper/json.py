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

@track("debug")
class Json(_ArDict):
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

    @classmethod
    def from_file(cls, file_path: str) -> 'Json':
        '''
            Creates a Json object from file.

            Arguments:
                file_path: Absolute path of the json file.

            Returns:
                Arjuna's `Json` object
        '''

        with open(file_path, 'r') as f:
            jobj = json.load(f)
            return Json(jobj)

    @classmethod
    def from_map(cls, map):
        '''
            Creates a Json object from Python dictionary.

            Arguments:
                map: Python dict

            Returns:
                Arjuna's `Json` object
        '''

        return Json(d)

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

    
