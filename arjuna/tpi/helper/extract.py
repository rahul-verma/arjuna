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

import abc
import random
from enum import Enum, auto

from arjuna.tpi.tracker import track

class pos:
    '''
        Factory Class with various factory methods to create objects for a single position and multiple positions.
    '''

    @classmethod
    def _create_extractor(cls, etype, *vargs, **kwargs):
        return getattr(cls, etype.lower())(*vargs, **kwargs)

    @classmethod
    def at(cls, *pos, strict: bool=True):
        '''
            Create Extractor object to extract objects at one or more positions from tuple/list.

            Args:
                pos: (int) Arbitrary positions in a sequence

            Keyword Arguments:
                strict: If True, exception is raised if no element is found at provided position.
        ''' 
        if len(pos) == 1:
            return _AtPositionExtractor(pos[0], strict=strict)
        else:
            return _AtPositionsExtractor(*pos, strict=strict)

    @classmethod
    def first(cls, strict: bool=True):
        '''
            Create Extractor object to extract objects at first position from tuple/list.

            Keyword Arguments:
                strict: If True, exception is raised if no element is found at provided position.
        ''' 
        return _FirstPositionExtractor(strict=strict)

    @classmethod
    def last(cls, strict: bool=True):
        '''
            Create Extractor object to extract objects at last position from tuple/list.

            Keyword Arguments:
                strict: If True, exception is raised if no element is found at provided position.
        ''' 
        return _LastPositionExtractor(strict=strict)


    @classmethod
    def random(cls, count=1, strict: bool=True):
        '''
            Create Extractor object to extract objects at random position(s) fom tuple/list.

            Arguments:
                count: Number of unique random positions to be used.
            
            Keyword Arguments:
                strict: If True, exception is raised if input sequence is empty or number of random samples requested > length of sequence.
        ''' 
        count = int(count)
        if count == 1:
            return _RandomPositionExtractor(strict=strict)
        else:
            return _RandomPositionsExtractor(count=count, strict=strict)

    @classmethod
    def slice(cls, *vargs, strict: bool=True, **kwargs):
        '''
            Create Extractor object to extract a slice of the provided tuple/list.

            Args:
                *vargs: (int) 1,2,or 3 arguments are accepted. See Notes.

            Keyword Arguments:
                kwargs: One or more of start/stop/step passed as keyword argument.
                strict: If True, exception is raised if extracted sequence is empty.

            Note:
                Following is the meaning of 1,2,3 arg signatures:

                .. code-block:: python

                    slice(stop)
                    slice(start, stop)
                    slice(start, stop, step)

                You can also use the keyword arguments instead of positional arguments:

                .. code-block:: python

                    slice(stop=4)
                    slice(start=2, stop=4)
                    slice(start=2, stop=7, step=2)

                You can not mix these styles of calling. Either use vargs or kwargs, else an Exception is raised.
        ''' 
        if vargs and kwargs:
            raise Exception("You can either use positional args or keword args to create a slice. These styles can not be mixed.")
        if not vargs and not kwargs:
            return _SlicedPositionsExtractor(strict=strict)
        if vargs:
            if len(vargs) > 3:
                raise Exception(f"Invalid positional arguments provided. Refer doc for 1,2,3 positional arg signature of this method. Args provided: {vargs}")
            
            vargs = [int(v) for v in vargs]
            if len(vargs) == 1:
                return _SlicedPositionsExtractor(stop=vargs[0], strict=strict)
            elif len(vargs) == 2:
                return _SlicedPositionsExtractor(start=vargs[0], stop=vargs[1], strict=strict)
            else:
                return _SlicedPositionsExtractor(start=vargs[0], stop=vargs[1], step=vargs[2], strict=strict)

        if kwargs:
            for k in kwargs:
                if k.lower() not in {"start", "stop", "step"}:
                    raise Exception(f"Invalid kwyword arguments provided. Only start/stop/step args are supported. Args provided: {kwargs}")
            kwargs = {k: k in {"start", "stop", "step"} and int(v) or v for k,v in kwargs.items()}
            return _SlicedPositionsExtractor(strict=strict, **kwargs)
                    

    @classmethod
    def odd(cls, strict: bool=True):
        '''
            Create Extractor object to extract objects at odd positions from given tuple/list.

            Keyword Arguments:
                strict: If True, exception is raised if extracted sequence is empty.
        ''' 
        return _OddPositionsExtractor(strict=strict)


    @classmethod
    def even(cls, strict: bool=True):
        '''
            Create Extractor object to extract objects at even positions from given tuple/list.

            Keyword Arguments:
                strict: If True, exception is raised if extracted sequence is empty.
        ''' 
        return _EvenPositionsExtractor(strict=strict)

@track("trace")
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


class _PositionExtractor(Extractor):
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

class _AtPositionExtractor(_PositionExtractor):
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

class _FirstPositionExtractor(_AtPositionExtractor):
    '''
    Extracts object at first position.

    Keyword Arguments:
        strict: If True, exception is raised if sequence is empty.
    ''' 

    def __init__(self, *, strict: bool=True):
        super().__init__(1, strict=strict)

class _LastPositionExtractor(_PositionExtractor):
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

class _RandomPositionExtractor(_PositionExtractor):
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

class _PositionsExtractor(Extractor):
    '''
        Represents positions based extractor objects for Tuples and Lists. Positions are considered in human counting (index + 1).

        Keyword Arguments:
            strict: If True, exception is raised if the extracted sequence is empty.
    '''

    def __init__(self, *, strict: bool):
        super().__init__(strict=strict, target_types={list, tuple})

    def _validated_output(self, sequence, out):
        if self.is_strict and not out:
            raise Exception("The extracted sequence is empty.")
        return out

class _AtPositionsExtractor(_PositionsExtractor):
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

class _SlicedPositionsExtractor(_PositionsExtractor):
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


class _OddPositionsExtractor(_SlicedPositionsExtractor):
    '''
        Represents odd positions extracttor object which provides entries at odd positions.

        Keyword Args:
            strict: If True, exception is raised if output sequence is empty. Default is True.
    ''' 

    def __init__(self, *, strict: bool=True):
        super().__init__(start=1, step=2, strict=strict)

class _EvenPositionsExtractor(_SlicedPositionsExtractor):
    '''
        Represents odd positions extractor object which provides entries at even positions.

        Keyword Args:
            strict: If True, exception is raised if output sequence is empty. Default is True.
    ''' 

    def __init__(self, *, strict: bool=True):
        super().__init__(start=2, step=2, strict=strict)

class _RandomPositionsExtractor(_PositionExtractor):
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