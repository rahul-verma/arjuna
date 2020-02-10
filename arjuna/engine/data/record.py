'''
This file is a part of Arjuna
Copyright 2015-2020 Rahul Verma

Website: www.RahulVerma.net

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

  http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
'''

import types
from arjuna.core.value import AnyRefValue


class DataRecord:

    def __init__(self, *vargs, **kwargs):
        self.__indexed = tuple([AnyRefValue(v) for v in vargs])
        self.__named = types.MappingProxyType({i.lower(): AnyRefValue(j) for i, j in kwargs.items()})

    def __getitem__(self, i):
        if type(i) is int:
            return self.__indexed[i]
        else:
            return self.__named[i]

    def __getattr__(self, i):
        if type(i) is str and not i.startswith('__'):
            return self[i]
        else:
            super().__getattr__(i)

    def value_named(self, name):
        return self.__named[name.lower()]

    @property
    def indexed_values(self):
        return self.__indexed

    @property
    def named_values(self):
        return self.__named

    def __str__(self):
        parts = ["Indexed"]
        if not self.indexed_values():
            parts.append("<empty>")
        else:
            for i,v in enumerate(self.indexed_values()):
                parts.append("[{}] {}".format(i, v.as_string()))
        parts.append("Named")
        if not self.named_values():
            parts.append("<empty>")
        else:
            for i,v in self.named_values().items():
                parts.append("[{}] {}".format(i, v.as_string()))
        return "\n".join(parts)

    def is_empty(self):
        return not self.indexed_values() and not self.named_values()

    def is_list_empty(self):
        return not self.indexed_values()

    def is_map_empty(self):
        return not self.named_values()

    def has_key(self, key):
        return key.lower() in self.__named

    def string(self, key):
        return self.value_named(key).as_string()

    def has_index(self, index):
        return len(self.__indexed) > index

class ListDataRecord:

    def __init__(self, data_record):
        self.__data_record = data_record

    @property
    def record(self):
        return self.__data_record

class DummyDataRecord(ListDataRecord):
    
    def __init__(self):
        super().__init__(None)


class MapDataRecord:

    def __init__(self, data_record):
        self.__data_record = {i.lower():j for i,j in dict(data_record).items()}

    @property
    def record(self):
        return self.__data_record

    def should_exclude(self):
        if "exclude" not in self.__data_record:
            return False

        exclude = self.__data_record['exclude']
        if exclude.upper() in constants.TRUES:
            return True
        else:
            del self.__data_record["exclude"]
            return False