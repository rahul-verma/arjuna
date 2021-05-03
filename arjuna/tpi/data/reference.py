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

import os
import abc
import random

from arjuna.tpi.helper.arjtype import CIStringDict
from .record import DataRecord

def _get_file_name(path):
    name = os.path.basename(path)
    return os.path.splitext(name)[0]

class IndexedDataReference(metaclass=abc.ABCMeta):
    '''
        Base class for autoloaded Indexed Data References in Arjuna.

        Arguments:
            pydict: A python repr of a list with indices as keys.

        Note:
            It behaves like a Python tuple. So, you get items by index and loop over it.
    '''

    def __init__(self, pydict):
        self.__records = pydict
        self.__iter = None

    def __len__(self):
        return len(self.__records)

    def __getitem__(self, index):
        return self._record_for(index)

    def first(self):
        '''
        First item in this data reference.
        '''
        return self[0]

    def random(self):
        '''
        Random item in this data reference.
        '''
        index = random.randint(0, len(self) -1)
        return self[index]

    def last(self):
        '''
        Last item in this data reference.
        '''
        return self[-1]

    def _record_for(self, index):
        try:
            # To support negative indices
            indices = list(self.__records.keys())
            try:
                target_index = indices[index]
            except:
                raise KeyError()
            else:
                return self.__records[target_index]
        except KeyError:
            raise Exception("Index {} not found in data reference: {}.".format(index, self.__class__.__name__))

    def __str__(self):
        return str({k: str(v) for k,v in self.__records.items()})

    def enumerate(self):
        '''
        Print all items in this data reference.
        '''
        for k,v in self.__records.items():
            print(k, "::", type(v), str(v))

    def __iter__(self):
        self.__iter = iter(self.__records.values())
        return self

    def __next__(self):
        return next(self.__iter)


class ContextualDataReference(metaclass=abc.ABCMeta):
    '''
        Base class for autoloaded Contextual data references in Arjuna.

        Arguments:
            path: Path of the contextual data reference file.

        Note:
            It behaves like a Python dictionary. So, you get items by names/keys and loop over it.
    '''

    def __init__(self, path):
        self.__path = path
        self.__name = _get_file_name(path)
        self.__map = CIStringDict()
        self._populate()
        self.__iter = None

    def __iter__(self):
        self.__iter = iter(self.__map)
        return self

    def __next__(self):
        return next(self.__iter)

    def __len__(self):
        return len(self.__map)

    def __getitem__(self, context):
        return self._record_for(context)

    def keys(self):
        '''
        Names of contexts/keys in this reference.
        '''
        return self.__map.keys()

    def items(self):
        '''
        Items iterator for this reference.
        '''
        return self.__map.items()

    @property
    def _map(self):
        return self.__map

    @property
    def path(self):
        '''
        Path of this reference file.
        '''
        return self.__path

    @property
    def name(self):
        '''
        Name of this reference.
        '''
        return self.__name

    def _update(self, data_reference):
        for context, record in data_reference.map.items():
            if context not in self.map:
                self.__map[context] = CIStringDict()
            self.__map[context].update(record.named_values)

    def _update_from_dict(self, context, map):
        if context not in self.map:
            self.__map[context] = dict()
        self.__map[context].update(map)

    def _add_record(self, context, record):
        self.__map[context] = DataRecord(context="Ref-{}[{}]".format(self.name, context), **record)

    def _record_for(self, context):
        try:
            return self.__map[context]
        except:
            raise Exception("{} at {} does not contain {} context key.".format(self.__class__.__name__, self.path, context))

    def __str__(self):
        return str({k: str(v) for k,v in self.__map.items()})

    def enumerate(self):
        '''
        Print all items in this data reference.
        '''
        for k,v in self.__map.items():
            print(k, "::", type(v), str(v))

    @abc.abstractmethod
    def _populate(self):
        pass

    def as_json(self):
        from arjuna import Json, Http
        from arjuna.core.fmt import arj_convert
        return Json.from_object(arj_convert(self.named_values))