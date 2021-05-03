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

import types
from arjuna.core.value import Value


class DataRecord:
    '''
        Represents a single Data Record

        When you use drive_with argument in @test decorator to associate a Data Source, the test function is repeated as many times as there are data records. For each such iteration, a **DataRecord** object is passed to the **data** argument of test function.

        Note:
            For retrieving indexed objects you have to use **[] notation** (just like a list or tuple), for example

            .. code-block:: python

                record[1]

            For retrieving named objects, you can either use **. notation** or **[] notation** (just like a dict), for example

            .. code-block:: python

                record.obj_name
                record[obj_name]
    '''

    def __init__(self, *vargs, context, process=True, **kwargs):
        self.__indexed = None
        self.__named = None
        if process:
            self.__indexed = tuple(vargs)
            self.__orig_values = types.MappingProxyType(kwargs)
            self.__named = types.MappingProxyType({i.lower(): j for i, j in kwargs.items()})
        else:
            self.__indexed = tuple()
            self.__named = types.MappingProxyType({}) 
        self.__context = context

    def __getitem__(self, i):
        if type(i) is int:
            return self.__indexed[i]
        else:
            return self.__named[i.lower()]

    def __getattr__(self, i):
        if type(i) is str and not i.startswith('__'):
            return self[i]
        else:
            super().__getattr__(i)

    def _should_exclude(self):
        if "exclude" in self.__named:
            if self.__named["exclude"].lower() in {"y","yes","true","1"}:
                return True

    @property
    def indexed_values(self) -> tuple:
        '''
            Get all indexed/positional objects
        '''
        return self.__indexed

    @property
    def indexed_values_as_json(self) -> 'JsonList':
        '''
        Get the indexed values in this Data Record as a JsonList.
        '''
        from arjuna import Json, Http
        from arjuna.core.fmt import arj_convert
        #return Json.from_str(Http.content.json(self.indexed_values).content)
        return Json.from_object(arj_convert(self.indexed_values))

    @property
    def named_values(self) -> dict:
        '''
            Get all named objects
        '''
        return dict(self.__orig_values)

    @property
    def named_values_as_json(self) -> 'JsonDict':
        '''
        Get the named values in this Data Record as a JsonDict.
        '''
        from arjuna import Json, Http
        from arjuna.core.fmt import arj_convert
        return Json.from_object(arj_convert(self.named_values))

    def is_empty(self) -> bool:
        '''
            Check if **DataRecord** has not indexed or named objects.

            Returns:
                True/False
        '''
        return not self.indexed_values() and not self.named_values()

    def has_key(self, key):
        '''
            Check if **DataRecord** has a key/name for which an object is present.

            Returns:
                True/False
        '''
        return key.lower() in self.__named

    def has_index(self, index):
        '''
            Check if **DataRecord** has an index for which an object is present.

            Returns:
                True/False
        '''
        return len(self.__indexed) > index

    def __str__(self):
        if not self.indexed_values and not self.named_values:
            return ""
        if self.indexed_values:
            indexed = " Indexed:{}".format(str([i for i in self.indexed_values]))
        else:
            indexed = ""
        if self.named_values:
            named =  " Named:{{{}}}".format(', '.join(['{0}={1}'.format(k, v) for k,v in self.named_values.items()]))
        else:
            named = ""
        return "{}Data->{}{}".format(self.__context, indexed, named)

