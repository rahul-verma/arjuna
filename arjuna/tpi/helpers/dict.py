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
Arjuna Dictionaries

Contains many custom implementations of a dict type.
'''

import abc
import pprint
from collections import OrderedDict
from typing import Callable

class _ArDict(metaclass=abc.ABCMeta):
    '''

    '''

    def __init__(self, d=None):
        self.__store = dict()
        if d:
            self.update(d)

    @property
    def store(self):
        return self.__store

    @abc.abstractmethod
    def _process_key(self, key):
        pass

    def __getitem__(self, key):
        return self.__store[self._process_key(key)]

    def pop(self, key):
        return self.__store.pop(self._process_key(key))

    def __setitem__(self, key, value):
        self.__store[self._process_key(key)] = value

    def __delitem__(self, key):
        del self.__store[self._process_key(key)]

    def _update(self, d):
        if not d: return
        for k,v in d.items():
            self[self._process_key(k)] = v

    def update(self, d):
        self._update(d)

    def has_key(self, key):
        return self._process_key(key) in self.__store

    def keys(self):
        return self.__store.keys()

    def __getattr__(self, attr):
        return getattr(self.__store, attr)

    def __len__(self):
        return len(self.__store.keys())

    def __str__(self):
        if not self.__store:
            return "<empty>"
        else:
            return str(self.__store)

    def __iter__(self):
        return iter(self.__store)

    def clone(self):
        return self._clone()

    def items(self):
        return self.__store.items()

    def is_empty(self):
        return len(self.__store) == 0

class CIStringDict(_ArDict):
    '''
        Dictionary with case-insensitive keys.

        Arguments:
            pydict: (Optional) A `dict` object.
    '''
    def __init__(self, pydict={}):
        super().__init__(pydict)

    def _process_key(self, key):
        return key.lower()

    def _clone(self):
        return CIStringDict(self.__store)


class ProcessedKeyDict(_ArDict):
    '''
        Dictionary with case-insensitive keys.

        Arguments:
            processor: A callable for processing the dictionary key.
            pydict: (Optional) A `dict` object.
    '''

    def __init__(self, *, processor: Callable, pydict: dict={}):
        self.__processor = processor
        super().__init__(pydict)

    def _process_key(self, key):
        return self.__processor(key)  

    def _clone(self):
        return ProcessedKeyDict(self.__processor, self.__store)  


class OnceOnlyKeyCIStringDict(CIStringDict):
    '''
        Dictionary with case-insensitive keys that allows for immutable key-value pairs.

        Arguments:
            processor: A callable for processing the dictionary key.
            pydict: (Optional) A `dict` object.
    '''

    def __init__(self, d={}):
        super().__init__(d)

    def __setitem__(self, key, value):
        if self.has_key(key):
            raise Exception("You can not change the value once set.")
        super().__setitem__(key, value)

    def _update(self, d):
        if not d: return
        as_dict = dict(d)
        for k in as_dict:
            self[k] = as_dict.get(k)

    def __iter__(self):
        return super().__iter__()

    def _clone(self):
        return OnceOnlyKeyCIStringDict(self.items())