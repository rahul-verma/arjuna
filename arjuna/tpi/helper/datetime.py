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


from arjuna.tpi.constant import TimeUnit
from datetime import timedelta, datetime

_DEF_FORMAT = '%d.%m.%y %H:%M:%S'

class Time:

    def __init__(self, time_unit, value):
        self.__unit = time_unit
        self.__value = value

    @staticmethod
    def seconds(self, secs):
        return Time(TimeUnit.SECONDS, secs)

    @staticmethod
    def milli_seconds(self, ms):
        return Time(TimeUnit.MILLI_SECONDS, ms)

    @staticmethod
    def minutes(self, mins):
        return Time(TimeUnit.MINUTES, mins)


class DateTimeStepper:

    def __init__(self, start=None, delta=None, max_steps=100000, forward=True, format=None, as_str=True):
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

    def __init__(self, pydtobj, *, format=_DEF_FORMAT):
        self.__pydtobject = pydtobj
        self.__format = format

    @property
    def _value(self):
        return self.__pydtobject

    @property
    def _format(self):
        return self.__format

    def stepper(self, *, delta=None, max_steps=100000, forward=True):
        return DateTimeStepper(start=self, delta=delta, max_steps=max_steps, forward=forward)

    @classmethod
    def now(self, *, format=_DEF_FORMAT):
        return DateTime(datetime.today(), format=format)

    @classmethod
    def from_str(self, dtstr, *, format=_DEF_FORMAT):
        return DateTime(datetime.strptime(dtstr, format), format=format)

    def as_str(self, *, format=None):
        if format is None:
            format = self.__format
        return datetime.strftime(self.__pydtobject, format)

    def add(self, dtdelta):
        self.__pydtobject  = self.__pydtobject + dtdelta._value
        return self

    def sub(self, dtdelta):
        self.__pydtobject  = self.__pydtobject - dtdelta._value
        return self

    __add__ = add
    __sub__ = sub


class DateTimeDeltaBuilder:

    def __init__(self):
        self.__dtdelta_kwargs = dict()

    def weeks(self, count):
        self.__dtdelta_kwargs['weeks'] = count
        return self

    def days(self, count):
        self.__dtdelta_kwargs['days'] = count
        return self

    def hours(self, count):
        self.__dtdelta_kwargs['hours'] = count
        return self

    def minutes(self, count):
        self.__dtdelta_kwargs['minutes'] = count
        return self

    def seconds(self, count):
        self.__dtdelta_kwargs['seconds'] = count
        return self

    def milliseconds(self, count):
        self.__dtdelta_kwargs['milliseconds'] = count
        return self

    def microseconds(self, count):
        self.__dtdelta_kwargs['microseconds'] = count
        return self

    def build(self):
        return DateTimeDelta(**self.__dtdelta_kwargs)


class DateTimeDelta:

    def __init__(self, *, weeks=0, days=0, hours=0, minutes=0, seconds=0, milliseconds=0, microseconds=0):
        self.__delta = timedelta(weeks=weeks, days=days, hours=hours, minutes=minutes, seconds=seconds, milliseconds=milliseconds, microseconds=microseconds)

    @property
    def _value(self):
        return self.__delta

    @classmethod
    def builder(cls):
        return DateTimeDeltaBuilder()

    @classmethod
    def zero(cls):
        return DateTimeDelta()

    def from_now(self, *, forward=True):
        if forward:
            return DateTime(datetime.today() + self._value)
        else:
            return DateTime(datetime.today() - self._value)

