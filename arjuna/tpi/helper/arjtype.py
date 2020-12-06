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
import random
from collections import OrderedDict, namedtuple
from typing import Callable
import abc
from enum import Enum, auto

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
class node(nvpairs):

    def __init__(self, **nvpairs):
        '''
            Represents a Node in HTML/XML/DOM described by name-value pairs.

            Keyword Arguments:
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

class pos:
    '''
        Factory Class with various factory methods to create objects for a single position and multiple positions.
    '''

    @classmethod
    def create_extractor(cls, etype, *vargs, **kwargs):
        return getattr(cls, etype.lower())(*vargs, **kwargs)

    @classmethod
    def at(cls, *pos, strict: bool=True):
        '''
            Returns AtPositionExtractor or AtPositionsExtractor object depending on whether one or multiple positions are provided.

            Args:
                pos: (int) Arbitrary positions in a sequence

            Keyword Arguments:
                strict: If True, exception is raised if no element is found at provided position.
        ''' 
        if len(pos) == 1:
            return AtPositionExtractor(pos[0], strict=strict)
        else:
            return AtPositionsExtractor(*pos, strict=strict)

    @classmethod
    def first(cls, strict: bool=True):
        '''
            Returns FirstPositionExtractor object.

            Keyword Arguments:
                strict: If True, exception is raised if no element is found at provided position.
        ''' 
        return FirstPositionExtractor(strict=strict)

    @classmethod
    def last(cls, strict: bool=True):
        '''
            Returns FirstPositionExtractor object.

            Keyword Arguments:
                strict: If True, exception is raised if no element is found at provided position.
        ''' 
        return LastPositionExtractor(strict=strict)


    @classmethod
    def random(cls, count=1, strict: bool=True):
        '''
            Returns RandomPositionExtractor or RandomPositionsExtractor object depending on whether count is 1 or > 1.

            Keyword Arguments:
                count: Number of unique random positions to be used.
                strict: If True, exception is raised if no element is found at provided position.
        ''' 
        if count == 1:
            return RandomPositionExtractor(strict=strict)
        else:
            return RandomPositionsExtractor(count=count, strict=strict)

    @classmethod
    def slice(cls, *vargs, strict: bool=True):
        '''
            Returns SlicedPositionsExtractor object.

            Args:
                *vargs: (int) 1,2,or 3 arguments are accepted. See Notes.

            Note:
                Following is the meaning of 1,2,3 arg signatures:

                slice(stop)
                slice(start, stop)
                slice(start, stop, step)

            Keyword Arguments:
                strict: If True, exception is raised if out list is empty.
        ''' 
        if len(vargs) > 3 or not vargs:
            raise Exception(f"Invalid positional arguments provided. Refer doc for 1,2,3 positional arg signature of this method. Args provided: {vargs}")
        elif len(vargs) == 1:
            return SlicedPositionsExtractor(stop=vargs[0], strict=strict)
        elif len(vargs) == 2:
            return SlicedPositionsExtractor(start=vargs[0], stop=vargs[1], strict=strict)
        else:
            return SlicedPositionsExtractor(start=vargs[0], stop=vargs[1], step=vargs[2], strict=strict)

    @classmethod
    def odd(cls, strict: bool=True):
        '''
            Returns OddPositionsFilter object which provides entries at odd positions.

            Keyword Arguments:
                strict: If True, exception is raised if out list is empty.
        ''' 
        return OddPositionsExtractor(strict=strict)


    @classmethod
    def even(cls, strict: bool=True):
        '''
            Returns EvenPositionsFilter object which provides entries at odd positions.

            Keyword Arguments:
                strict: If True, exception is raised if out list is empty.
        ''' 
        return EvenPositionsExtractor(strict=strict)

@track("debug")
class Extractor(metaclass=abc.ABCMeta):
    '''
        Abstract class for extractors. Given an object, a concrete implementation extracts objects from the given object.

        Keyword Arguments:
            strict: The extractors can choose what strict mode means for them and related behavior. For strict mode, in certain situations, exception is raised by an exractor.

        Note:
            In strict mode, Exception is raised if the target object is empty (returns bool(obj) is False)
    '''

    def __init__(self, *, strict=True, target_types):
        self.__target_types = target_types
        self.__strict = strict

    @property
    def is_strict(self):
        '''
            Bool property that indicates whether this extractor is in strict mode or not.
        '''
        return self.__strict

    def extract(self, obj):
        '''
            Extracts objects from the given object as per concrete Extractor implementations.

            Arguments:
                obj: Extraction target.
        '''
        self.__validate(obj)  
        return self._extract(obj)           

    @abc.abstractmethod
    def _extract(self, obj):
        pass

    def __validate(self, obj):
        if type(obj) not in self.__target_types:
            raise Exception("Target object type mismatch. Provided {} of type {}. Should be one of {} for Extractor type: {}".format(obj, type(obj), self.__target_types, self.__class__.__name__))
        
        if self.is_strict and not obj:
            raise Exception("Provided target object is empty.")   


class PositionExtractor(Extractor):
    '''
        Represents position based extractor objects for Tuples and Lists. Positions are considered in human counting (index + 1).

        Keyword Arguments:
            strict: If True, exception is raised if no element is found at provided position.
    '''

    def __init__(self, *, strict: bool):
        super().__init__(strict=strict, target_types={list, tuple})

    def __validate_seq_type(cls, sequence):
        if type(sequence) not in {tuple, list}:
            raise Exception(f"position extractors support only tuples and lists. Provided {sequence} of type {t}")

class AtPositionExtractor(PositionExtractor):
    '''
    Extracts object at a given position.

    Args:
        pos: (int) positions in an sequence

    Keyword Arguments:
        strict: If True, exception is raised if no element is found at provided position.
    ''' 
    def __init__(self, pos: int, strict=True):
        super().__init__(strict=strict)
        self.__index = pos - 1

    def _extract(self, sequence):
        return sequence[self.__index]

class FirstPositionExtractor(AtPositionExtractor):
    '''
    Extracts object at first position.

    Keyword Arguments:
        strict: If True, exception is raised if sequence is empty.
    ''' 

    def __init__(self, *, strict: bool=True):
        super().__init__(1, strict=strict)

class LastPositionExtractor(PositionExtractor):
    '''
    Extracts object at last position.

    Keyword Arguments:
        strict: If True, exception is raised if sequence is empty.
    ''' 

    def __init__(self, strict=True):
        super().__init__(strict=strict)
        self.__index = -1

    def _extract(self, sequence):
        return sequence[self.__index]

class RandomPositionExtractor(PositionExtractor):
    '''
    Extracts object at last position.

    Keyword Arguments:
        strict: If True, exception is raised if sequence is empty.
    ''' 

    def __init__(self, strict=True):
        super().__init__(strict=strict)
        self.__index = -1

    def _extract(self, sequence):
        return sequence[random.randint(0, len(sequence)-1)]

class PositionsExtractor(Extractor):
    '''
        Represents positions based extractor objects for Tuples and Lists. Positions are considered in human counting (index + 1).

        Keyword Arguments:
            strict: If True, exception is raised if the out list is empty.
    '''

    def __init__(self, *, strict: bool):
        super().__init__(strict=strict, target_types={list, tuple})

    def _validated_output(self, sequence, out):
        if self.is_strict and not out:
            raise Exception("The extracted sequence is empty.")
        return out

class AtPositionsExtractor(PositionsExtractor):
    '''
        Represents fixed positions extractor object.

        Args:
            *pos: (int) positions in an sequence

        Keyword Arguments:
            strict: If True, exception is raised if for any of the provided positions, there is no entry in sequence. Default is True.
    ''' 

    def __init__(self, *pos, strict=True):
        super().__init__(strict=strict)
        self.__indices = [v-1 for v in pos]

    def _extract(self, sequence):
        out = []
        for i in self.__indices:
            try:
                out.append(sequence[i])
            except IndexError:
                if self.is_strict:
                    raise Exception("No entry found at pos {} in {}".format(i+1, sequence))
                else:
                    out.append(None)
        return self._validated_output(sequence, out)

class SlicedPositionsExtractor(PositionsExtractor):
    '''
        Represents sliced positions extractor object.

        Keyword Args:
            stop: Optional. Stop position. Default is end of sequence.
            start: Optional. Start position. Default is 1. 
            step: Optional. Position delta between two successive values.
            strict: If True, exception is raised if output sequence is empty. Default is True.

        Note:
            If not argument is provided, then all elements are included.
    ''' 

    def __init__(self, *, stop: int=None, start: int=1, step: int=1, strict: bool=True):
        super().__init__(strict=strict)
        if start is not None:
            start = start - 1
        # Python slices don't contain right boundary. So, no need to subtract 1 from stop.
        self.__slice = slice(start, stop, step)

    def _extract(self, sequence):
        return self._validated_output(sequence, sequence[self.__slice])


class OddPositionsExtractor(SlicedPositionsExtractor):
    '''
        Represents odd positions extracttor object which provides entries at odd positions.

        Keyword Args:
            strict: If True, exception is raised if output sequence is empty. Default is True.
    ''' 

    def __init__(self, *, strict: bool=True):
        super().__init__(start=1, step=2, strict=strict)

class EvenPositionsExtractor(SlicedPositionsExtractor):
    '''
        Represents odd positions extractor object which provides entries at even positions.

        Keyword Args:
            strict: If True, exception is raised if output sequence is empty. Default is True.
    ''' 

    def __init__(self, *, strict: bool=True):
        super().__init__(start=2, step=2, strict=strict)

class RandomPositionsExtractor(PositionExtractor):
    '''
    Extracts object at last position.

    Keyword Arguments:
        count: Number of unique random positions to be used.
        strict: If True, exception is raised if output sequence is empty or count is greater than sequence size. Default is True.
    ''' 
    def __init__(self, *, count, strict=True):
        super().__init__(strict=strict)
        self.__count = count

    def _extract(self, sequence):
        if len(sequence) < self.__count:
            if self.is_strict:
                raise Exception("Sequence {} is shorter than number of positions: {}".format(sequence, count))
            else:
                return [i for i in sequence]
        elif len(sequence) == self.__count:
            return [i for i in sequence]
        else:
            return random.sample(sequence, self.__count)

NetworkPacketInfo = namedtuple("NetworkPacketInfo", "label request response sub_network_packets")