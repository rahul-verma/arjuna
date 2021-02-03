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
Arjuna Date Time Helper Classes

Contains many general purpose type abstractions.
'''


from arjuna.tpi.constant import TimeUnit
from datetime import timedelta, datetime

_DEF_FORMAT = '%d.%m.%y %H:%M:%S'

class Time:
    '''
        A time object.

        Arguments:
            time_unit: TimeUnit enum value.
            value: An integer representing this time value.
    '''

    def __init__(self, time_unit, value):
        self.__unit = time_unit
        self.__value = value

    @classmethod
    def seconds(cls, value):
        '''
            Factory method to a create a Time object for seconds.

            Arguments:
                value: Number of seconds
        '''
        return Time(TimeUnit.SECONDS, value)

    @classmethod
    def milliseconds(cls, value):
        '''
            Factory method to a create a Time object for milliseconds.

            Arguments:
                value: Number of milliseconds
        '''
        return Time(TimeUnit.MILLI_SECONDS, value)

    @classmethod
    def minutes(cls, value):
        '''
            Factory method to a create a Time object for minutes.

            Arguments:
                value: Number of minutes
        '''
        return Time(TimeUnit.MINUTES, value)


class DateTimeStepper:
    '''
        An iterable object that returns DateTime objects or strings as per provided arguments.

        Keyword Arguments:
            start: Arjuna DateTime object to start stepping. If not supplied current date & time is used. Returned as first value.
            delta: A DateTimeDelta object used to create next date time object. If not provided, a delta of 1 second is used.
            max_steps: Maximum number of steps or iterations of this object. Default is 100000.
            forward: Boolen value that sets the direction of date time. If True steps are directed towards future else towards past. Default is True.
            format: String format to represent the generated date time object. If not provided, it is taken from start argument. If start argument is not provided it defaults to '%d.%m.%y %H:%M:%S'.
            as_str: Boolena value that controls the return type on next calls. If True, the iterable returns the data time object as a string else DateTime object is returned. Default is True.

        Note:
            You can make next() call to get next DateTime object or string:

            .. code-block:: python

                dtstepperDateTimeStepper()
                dt = dtstepper.next()

            If you have explcitly set max_steps, a better usage pattern is to use this object in a Python for loop:

            .. code-block:: python

                for dt in DateTimeStepper(max_steps=25):
                    # Do something
                    print(dt)
    '''

    def __init__(self, *, start: 'DateTime'=None, delta: 'DateTimeDelta'=None, max_steps: int=100000, forward: bool=True, format: str=None, as_str: bool=True):
        if start is not None:
            self.__start = start
            if format is not None:
                self.__format = format
            else:
                self.__format = start._format
        else:
            if format is not None:
                self.__start = DateTime(datetime.today(), format=format)
                self.__format = format
            else:
                self.__start = DateTime(datetime.today(), format=_DEF_FORMAT)
                self.__format = _DEF_FORMAT

        self.__delta = delta is not None and delta or DateTimeDeltaBuilder().seconds(1).build()
        self.__max_steps = max_steps
        self.__forward = forward
        self.__as_str = as_str
        self.__current = DateTime(self.__start._value, format=self.__format)
        self.__counter = 0

    def __iter__(self):
        return self

    def next(self):
        '''
            Returns next DateTime object or string.
        '''
        self.__counter += 1
        if self.__counter > self.__max_steps:
            raise StopIteration("Finished all steps.")
        if self.__counter != 1:
            if self.__forward:
                self.__current = DateTime((self.__current + self.__delta)._value)
            else:
                self.__current = DateTime((self.__current - self.__delta)._value)
                
        return self.__as_str and self.__current.as_str(format=self.__format) or self.__current

    __next__ = next

class DateTime:
    '''
        Represents a (mutable) date time object.

        Arguments:
            pydtobj: Python datetime object.
            format: String representation. Default is '%d.%m.%y %H:%M:%S'.

        Note:

            You can use + and - operators with DateTime and DateTimeDelta objects.

            .. code-block:: python

                dtobj + dtdelta
                dtobj - dtdelta

            Although reassignment is not necessary, you can also do

            .. code-block:: python

                dtobj = dtobj + dtdelta
                dtobj = dtobj - dtdelta
    '''

    def __init__(self, pydtobj, *, format=_DEF_FORMAT):
        self.__pydtobject = pydtobj
        self.__format = format

    @property
    def _value(self):
        return self.__pydtobject

    @property
    def _format(self):
        return self.__format

    def stepper(self, *, delta: 'DateTimeDelta'=None, max_steps: int=100000, forward: bool=True, format: str=None, as_str: bool=True):
        '''
            Factory method to create DateTimeStepper object which takes this DateTime as starting point.

            Keyword Arguments:
                delta: A DateTimeDelta object used to create next date time object. If not provided, a delta of 1 second is used.
                max_steps: Maximum number of steps or iterations of this object. Default is 100000.
                forward: Boolean value that sets the direction of date time. If True steps are directed towards future else towards past. Default is True.
                format: String format to represent the generated date time object. If not provided, it is taken from this DateTime object.
                as_str: Boolean value that controls the return type on next calls. If True, the iterable returns the data time object as a string else DateTime object is returned. Default is True.
        '''
        return DateTimeStepper(start=self, delta=delta, max_steps=max_steps, forward=forward, format=format, as_str=as_str)

    @classmethod
    def now(self, *, format: str=_DEF_FORMAT):
        '''
            Factory method to create a DateTime object representing current date and time.

            Keyword Arguments:
                format: String format to represent the generated date time object. Default is '%d.%m.%y %H:%M:%S'.
        '''
        return DateTime(datetime.today(), format=format)

    @classmethod
    def from_str(self, dtstr: str, *, format: str=_DEF_FORMAT):
        '''
            Factory method to create a DateTime object from provided date time string.

            Arguments:
                dtstr: Date Time string

            Keyword Arguments:
                format: String format to parse the provided date time string. Default is '%d.%m.%y %H:%M:%S'.
        '''
        return DateTime(datetime.strptime(dtstr, format), format=format)

    @classmethod
    def convert(self, dtstr: str, *, from_format: str=_DEF_FORMAT, to_format: str=_DEF_FORMAT):
        '''
            Factory method to create a DateTime object from provided date time string.

            Arguments:
                dtstr: Date Time string

            Keyword Arguments:
                from_format: String format to parse the provided date time string. Default is '%d.%m.%y %H:%M:%S'.
                to_format: String format to create the converted date time string. Default is '%d.%m.%y %H:%M:%S'.

            Returns:
                Date Time string as per to_format
        '''
        return DateTime.from_str(dtstr, format=from_format).as_str(format=to_format)  

    def as_str(self, *, format=None):
        '''
            String representation of this DateTime object.

            Keyword Arguments:
                format: String format to represent the provided date time object. If not provided format set during construction of this object is used.
        '''
        if format is None:
            format = self.__format
        return datetime.strftime(self.__pydtobject, format)

    def add(self, dtdelta):
        '''
            Add a DateTimeDelta object to this object. Modifies current object.

            Arguments:
                dtdelta: DateTimeDelta Object.

            Returns:
                This DateTime object (Self)
        '''
        self.__pydtobject  = self.__pydtobject + dtdelta._value
        return self

    def sub(self, dtdelta):
        '''
            Add a DateTimeDelta object to this object. Modifies current object.

            Arguments:
                dtdelta: DateTimeDelta Object.

            Returns:
                This DateTime object (Self)
        '''
        self.__pydtobject  = self.__pydtobject - dtdelta._value
        return self

    __add__ = add
    __sub__ = sub


class DateTimeDeltaBuilder:
    '''
        Builder class to flexibly build a DateTimeDelta object.
    '''

    def __init__(self):
        self.__dtdelta_kwargs = dict()

    def weeks(self, count: int):
        '''
            Set number of detla weeks.

            Arguments:
                count: Number of weeks
        '''
        self.__dtdelta_kwargs['weeks'] = count
        return self

    def days(self, count: int):
        '''
            Set number of detla days.

            Arguments:
                count: Number of days
        '''
        self.__dtdelta_kwargs['days'] = count
        return self

    def hours(self, count: int):
        '''
            Set number of detla hours.

            Arguments:
                count: Number of hours
        '''
        self.__dtdelta_kwargs['hours'] = count
        return self

    def minutes(self, count: int):
        '''
            Set number of detla minutes.

            Arguments:
                count: Number of minutes
        '''
        self.__dtdelta_kwargs['minutes'] = count
        return self

    def seconds(self, count: int):
        '''
            Set number of detla seconds.

            Arguments:
                count: Number of seconds
        '''
        self.__dtdelta_kwargs['seconds'] = count
        return self

    def milliseconds(self, count: int):
        '''
            Set number of detla miliseconds.

            Arguments:
                count: Number of milliseconds
        '''
        self.__dtdelta_kwargs['milliseconds'] = count
        return self

    def microseconds(self, count: int):
        '''
            Set number of detla microseconds.

            Arguments:
                count: Number of microseconds
        '''
        self.__dtdelta_kwargs['microseconds'] = count
        return self

    def build(self):
        '''
            Build a DateTimeDelta object as per values set in builder.

            Returns:
                DateTimeDelta object.
        '''
        return DateTimeDelta(**self.__dtdelta_kwargs)


class DateTimeDelta:
    '''
        Represents a delta (difference) in date time.

        Keyword Arguments:
            weeks: Delta number of weeks.
            days: Delta number of days.
            hours: Delta number of hours.
            minutes: Delta number of minutes.
            seconds: Delta number of seconds.
            miliseconds: Delta number of miliseconds.
            microseconds: Delta number of microseconds.
    '''

    def __init__(self, *, weeks: int=0, days: int=0, hours: int=0, minutes: int=0, seconds: int=0, milliseconds: int=0, microseconds: int=0):
        self.__delta = timedelta(weeks=weeks, days=days, hours=hours, minutes=minutes, seconds=seconds, milliseconds=milliseconds, microseconds=microseconds)

    @property
    def _value(self):
        return self.__delta

    @classmethod
    def builder(cls):
        '''
            Create a DateTimeDeltaBuilder object.

            Returns:
                DateTimeDeltaBuilder object
        '''
        return DateTimeDeltaBuilder()

    @classmethod
    def zero(cls):
        '''
            Create a DateTimeDelta object which represents no change in date time.

            Returns:
                DateTimeDelta object.
        '''
        return DateTimeDelta()

    def from_now(self, *, forward: bool=True, format: str=_DEF_FORMAT):
        '''
            Keyword Arguments:
                forward: Boolen value that sets the direction of date time. If True delta is added else it is subtracted. Default is True.
                format: String format to represent the generated date time object. Default is '%d.%m.%y %H:%M:%S'.
        '''
        if forward:
            return DateTime(datetime.today() + self._value, format=format)
        else:
            return DateTime(datetime.today() - self._value, format=format)

