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

'''
Arjuna Types

Contains many general purpose type abstractions.
'''

import abc
import pprint
import random
from collections import OrderedDict, namedtuple
from typing import Callable
from enum import Enum, auto

from arjuna.tpi.tracker import track
from arjuna.tpi.constant import DomDirection, DomNodeType

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

class oneof:
    '''
        Represents the given sequence as choices.

        Args:
            choices: Arbitrary objects as choices.
    '''

    def __init__(self, *choices):
        self.__choices = choices

    def as_list(self):
        return list(self.__choices)

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
class nvpair(Dictable):
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
class attr(nvpair):
    '''
        A name-value pair with an associated optional tag name. It is an implementation of **Dictable**.

        Keyword Arguments:
            attr_name_value: (Mandatory) Key-Value pair representing name and value of attribute.

        Note:
            In case the attribute name conflicts with a Python language keyword, you can prefix it with '__' i.e. two underscores. These underscores are removed while processing the attribute name.

            For example, '__for' will become 'for' to avoid conflict with Python's **for** keyword.
    '''

    def __init__(self, **attr_name_value):
        if len(attr_name_value) > 1:
            raise Exception("attr specification must contain a single key value pair for attribute name and value")
        if len(attr_name_value) > 1:
            raise Exception("attr/fattr/battr/eattr specification should contain only a single key value pair for attribute name and value")
        name = list(attr_name_value.keys())[0]
        if name.startswith('__'):
            name = name[2:]
        value = list(attr_name_value.values())[0]
        super().__init__(name, value)

    def _as_dict(self):
        d = super()._as_dict()
        return d


@track("trace")
class nvpairs(Dictable):
    '''
        Encapsulates arbitrary name-value pairs. It is an implementation of **Dictable**.

        Keyword Arguments:
            **nvpairs: Arbitrary name-value pairs passed as keyword arguments.
    '''
    def __init__(self, **nvpairs):
        self.__kwargs = nvpairs

    def _as_dict(self):
        return self.__kwargs


@track("trace")
class withx(nvpairs):
    '''
        Encapsulates arbitrary name-value pairs. It is an implementation of **Dictable**.

        This is to be used when using withx locators progammaitcally.

        Keyword Arguments:
            **nvpairs: Arbitrary name-value pairs passed as keyword arguments.
    '''
    pass

@track("trace")
class Node(nvpairs):

    def __init__(self, *, type, **nvpairs):
        '''
            Represents a Node in HTML/XML/DOM described by name-value pairs.

            Keyword Arguments:
                type: (Mandatory) DomNodeType - NODE/FNODE/BNODE determines how attribute content is matched:
                    * NODE: Partial Content
                    * FNODE: Full Content
                    * BNODE: Partial Content at Beginning
                **nvpairs: Special and Arbitrary name-value pairs passed as keyword arguments.

            Note:
                Following keywords have special meaning:

                    * tag - Represents tag name of node
                    * classes - Passed as a string or list/tuple represents one or more classes in class attribute of node (order does not matter)
                    * text - Represents text content
                    * star_text - It is equivalent of *//text() in XPath
                    * dot_text - It is equivalent of . in XPath
                    * attrs - It is a dictionary of attributes. Can be used when names can not be passed as keywords.
                        * Names conflict with Python keywords. For example: 'for'
                        * '.text' for dot_text
                        * '*text' for star_text

                All other key value pairs are assumed to be attribute names and corresponding values.

                If any keyword is preceded with '__' (double underscores), the underscores are removed at the time of definition generation. This can be used to avoid conflict of attribute names with Python keywords.
        '''
        super().__init__(**nvpairs)
        self.__type = type
    
    @property
    def ntype(self):
        return self.__type

    def _as_dict(self):
        out_dict = dict()
        d = super()._as_dict()
        if 'attrs' in d:
            for k,v in d['attrs'].items():
                if k.startswith('__'):
                    k = k[2:]
                out_dict[k] = v
        for k,v in d.items():
            if k == 'attrs': continue
            if k.startswith('__'):
                k = k[2:]
            out_dict[k] = v
        return out_dict

@track("trace")
class node(Node):

    def __init__(self, **nvpairs):
        super().__init__(type=DomNodeType.NODE, **nvpairs)

@track("trace")
class fnode(Node):

    def __init__(self, **nvpairs):
        super().__init__(type=DomNodeType.FNODE, **nvpairs)

@track("trace")
class bnode(Node):

    def __init__(self, **nvpairs):
        super().__init__(type=DomNodeType.BNODE, **nvpairs)

@track("trace")
class _Axis:

    def __init__(self, direction, node):
        self.__direction = direction
        self.__node = node

    @property
    def direction(self):
        return self.__direction

    @property
    def node(self):
        return self.__node


@track("trace")
class axes:
    '''
        Represents a DOM axes with a starting node and then as per axis objects sequence.

        Arguments:
            start: Starting point as a node object
    '''

    def __init__(self, start):
        self.__start = start
        self.__axes = list()

    @property
    def _start(self):
        return self.__start

    @property
    def _axes(self):
        return self.__axes

    @classmethod
    def _from_dict(cls, axes_dict):
        axes_dict = {k.lower():v for k,v in axes_dict.items()}
        axes_obj = axes(node(**axes_dict['start']))
        del axes_dict['start']
        for k,v in axes_dict.items():
            getattr(axes_obj, k)(node(**v))
        return axes_obj

    @classmethod
    def _from_list(cls, axes_list):
        start = None
        axes_entries = []

        for entry in axes_list:
            if len(entry) > 1:
                raise Exception("If axes specification is of list type, each list item must be a single key value pair. Wrong axes definition found: {}".format(axes_list))
            name = list(entry.keys())[0].lower()
            value = list(entry.values())[0]
            if name == "start":
                if start is None:
                    start = node(**value)
                else:
                    raise Exception("Duplicate definition of start key found in axes def: {}".format(axes_list))
            else:
                axes_entries.append((name, node(**value)))
        
        if start is None:
            raise Exception("axes definition must have start key. Wrong axes def: {}".format(axes_list))

        axes_obj = axes(start)
        for direction, n in axes_entries:
            getattr(axes_obj, direction)(n)
        return axes_obj

    def up(self, node):
        '''
        Move towards node definition in the direction of Ancestors.
        '''
        self.__axes.append(_Axis(DomDirection.UP, node))
        return self

    def down(self, node):
        '''
        Move towards node definition in the direction of Descendants.
        '''
        self.__axes.append(_Axis(DomDirection.DOWN, node))
        return self

    def left(self, node):
        '''
        Move towards node definition in the direction of Previous Siblings.
        '''
        self.__axes.append(_Axis(DomDirection.LEFT, node))
        return self

    def right(self, node):
        '''
        Move towards node definition in the direction of Forward Siblings.
        '''
        self.__axes.append(_Axis(DomDirection.RIGHT, node))
        return self

class NotFound:
    '''
    To differentiate a not found object from Python's None.

    Always evalutes to False in a boolean context.
    '''
    
    def __bool__(self):
        return False

NetworkPacketInfo = namedtuple("NetworkPacketInfo", "label request response sub_network_packets")