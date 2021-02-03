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
import pprint
from enum import Enum
from arjuna.tpi.helper.arjtype import *
from functools import partial

from weakref import WeakKeyDictionary


class EnumSwitch:
    def __init__(self, cases, const_args):
        self.dispatch_dict = cases
        self.const_args = const_args

    def __call__(self, econst):
        if econst in self.dispatch_dict:
            f_tuple = self.dispatch_dict[econst]
            arg_list = list(self.const_args) + list(f_tuple[1:])
            return f_tuple[0](*arg_list)



class PropertyEnum(Enum):
    pass
    # def _generate_next_value_(name, start, count, last_values):
    #     return ".".join(name.lower().split("_"))


class Descriptor(metaclass=abc.ABCMeta):
    def __init__(self):
        self._name = None
        self._values = WeakKeyDictionary()

    def __get__(self, instance, cls):
        return self._values.get(instance)

    def __set__(self, instance, value):
        self.validate(instance, value)
        if instance in self._values:
            self._values[instance].set_value(value)
        else:
            self._values[instance] = self._create_value(value)

    def set_name(self, name):
        self._name = name

    @abc.abstractmethod
    def _create_value(self, value):
        pass

    def validate(self, instance, value):
        self._values[instance].validate(value)

class Decorator(metaclass=abc.ABCMeta):
    def __new__(cls, *args, **kwargs):
        if cls.__name__ == "Decorator":
            raise Exception("Decorator is an abstract class. Inherit to implement a concrete decorator.")
        else:
            return super().__new__(cls)

    def __init__(self, **dkwargs):
        super().__init__()
        self.__args = CIStringAttrDict(dkwargs)
        self.__kallable = None

    def __call__(self, kallable):
        self.__kallable = kallable
        return partial(self._decorated, self.__args, self.__kallable)

    @abc.abstractmethod
    def _decorated(self, dargs, kallable, *fvargs, **fkwargs):
        pass

# helpers
def dynamic_load(global_dict, all_list, names):
    for n, b, d in names:
        global_dict[n] = type(n, b, d)
        all_list.append(n)

def prepare_locals(l):
    return {i: j for i, j in l.items() if i not in ['self', '__class__']}