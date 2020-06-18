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
Arjuna Types

Contains many general purpose type abstractions.
'''

import abc
import pprint
from collections import OrderedDict, namedtuple
from typing import Callable
import abc

from arjuna.tpi.tracker import track

class _ArDict(metaclass=abc.ABCMeta):

    def __init__(self, d=None):
        self.__store = dict()
        self.__key_map = dict()
        if d:
            self.update(d)

    @property
    def orig_dict(self):
        return self.__create_orig_dict()

    @property
    def store(self):
        return self.__store

    def __create_orig_dict(self):
        return {self.__key_map[k]: v for k,v in self.store.items()}

    def __process_key_wrapper(self, key):
        revised_key = self._process_key(key)
        if revised_key not in self.__key_map:
            self.__key_map[revised_key] = key
        return revised_key

    @abc.abstractmethod
    def _process_key(self, key):
        pass

    def __getitem__(self, key):
        return self.__store[self.__process_key_wrapper(key)]

    def pop(self, key):
        return self.__store.pop(self.__process_key_wrapper(key))

    def __setitem__(self, key, value):
        self.__store[self.__process_key_wrapper(key)] = value

    def __delitem__(self, key):
        del self.__store[self.__process_key_wrapper(key)]

    def _update(self, d):
        if not d: return
        for k,v in d.items():
            self[self.__process_key_wrapper(k)] = v

    def update(self, d):
        self._update(d)

    def has_key(self, key):
        return self.__process_key_wrapper(key) in self.__store

    def keys(self):
        return self.__create_orig_dict().keys()

    def __getattr__(self, attr):
        try:
            return self.__store[attr]
        except KeyError:
            raise AttributeError(f"No attribute/key with name {attr}.")

    def __len__(self):
        return len(self.__store.keys())

    def __str__(self):
        if not self.__store:
            return "<empty>"
        else:
            return str(self.__create_orig_dict())

    def __iter__(self):
        return iter(self.__create_orig_dict())

    def clone(self):
        return self._clone()

    def items(self):
        return self.__create_orig_dict().items()

    def is_empty(self):
        return len(self.__store) == 0

    def _get_orig_dict(self):
        return self.__create_orig_dict()


class CIStringDict(_ArDict):
    '''
        Dictionary with case-insensitive keys.

        Arguments:
            pydict: (Optional) A **dict** object.
    '''
    def __init__(self, pydict={}):
        super().__init__(pydict)

    def _process_key(self, key):
        return key.lower()

    def _clone(self):
        return CIStringDict(self._get_orig_dict())

    def __str__(self):
        return "CIStringDict: " + super().__str__()
        

class ProcessedKeyDict(_ArDict):
    '''
        Dictionary with case-insensitive keys.

        Arguments:
            processor: A callable for processing the dictionary key.
            pydict: (Optional) A **dict** object.
    '''

    def __init__(self, *, processor: Callable, pydict: dict={}):
        self.__processor = processor
        super().__init__(pydict)

    def _process_key(self, key):
        return self.__processor(key)  

    def _clone(self):
        return ProcessedKeyDict(self.__processor, self.__store)  

@track("trace")
class OnceOnlyKeyCIStringDict(CIStringDict):
    '''
        Dictionary with case-insensitive keys that allows for immutable key-value pairs.

        Arguments:
            processor: A callable for processing the dictionary key.
            pydict: (Optional) A **dict** object.
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


@track("trace")
class Dictable(metaclass=abc.ABCMeta):
    '''
        Abstract class. Any object which has a method **as_dict** is a **Dictable**.
    '''

    @abc.abstractmethod
    def _as_dict(self):
        pass

    def as_dict(self) -> dict:
        '''
            Dictionary representation of this object.

            Returns:
                A **dict** object.
        '''
        retval = self._as_dict()
        if type(retval) is not dict:
            raise Exception("_as_dict must return a dict type. Got {} of type {}".format(retval, type(retval)))
        return retval

class Point(Dictable):
    '''
        Represents an XY coordinate.

        Args:
            x: X co-ordinate
            y: Y co-ordinate
    '''

    def __init__(self, x, y):
        self.__x = x
        self.__y = y

    @property
    def location(self):
        '''
            Get XY co-ordinates as a tuple -> (x,y)
        '''
        return (self.__x, self.__y)

    def _as_dict(self):
        return {"x": self.__x, "y":self.__y}

class Offset(Point):
    '''
        Represents an offset from current **Point** on **Screen** in terms of XY coordinates.

        Args:
            x: X co-ordinate
            y: Y co-ordinate
    '''

    def __init__(self, x, y):
        super().__init__(x,y)

@track("trace")
class Screen:
    '''
        Represents Gui Screen in terms of its XY coordinates.
    '''

    @staticmethod
    def xy(x:int, y:int) -> Point:
        '''
            Create a **Point** on Gui Screen in terms of its XY coordinates.
        '''
        #return  _Point(x,y)
        raise NotImplementedError()

    @staticmethod
    def offset(x, y) -> Offset:
        '''
            Create a **Offset** on Gui Screen in terms of its XY coordinates.
        '''
        # return _Offset(x,y)
        raise NotImplementedError()

@track("trace")
class NVPair(Dictable):
    '''
        Encapsulates a name-value pair. It is an implementation of **Dictable**.

        Args:
            name: Name of this object
            value: Value of this object
    '''

    def __init__(self, name, value):
        self.__name = name
        self.__value = value

    @property
    def name(self):
        '''
        Name of this object.
        '''
        return self.__name

    @property
    def value(self):
        '''
        Value of this object.
        '''
        return self.__value

    def _as_dict(self):
        return {"name" : self.__name, "value": self.__value}


@track("trace")
class Attr(NVPair):
    '''
        A name-value pair with an associated optional tag name. It is an implementation of **Dictable**.

        Keyword Arguments:
            name: (Mandatory) Name of this object
            value: (Mandatory) Value of this object
            tag: Tag associated with this object
    '''

    def __init__(self, *, name, value, tag=None):
        super().__init__(name, value)
        self.__tag = tag

    def _as_dict(self):
        d = super()._as_dict()
        d["tag"] = self.__tag
        return d


@track("trace")
class NVPairs(Dictable):
    '''
        Encapsulates arbitrary name-value pairs. It is an implementation of **Dictable**.

        Keyword Arguments:
            **nvpairs: Arbitrary name-value pairs passed as keyword arguments.
    '''

    def __init__(self, **nvpairs):
        self.__kwargs = nvpairs

    def _as_dict(self):
        return self.__kwargs


NetworkPacketInfo = namedtuple("NetworkPacketInfo", "label request response sub_network_packets")