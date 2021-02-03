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

import re
import abc

from arjuna.core.utils import data_utils

class UnsupportedRepresentationException(Exception):

    def __init__(self, strSourceValue, targetValueType):
        super().__init__("Value: Can not represent value >>{}<< as {}.".format(strSourceValue, targetValueType))


class Value:
    TRUES = {"YES", "TRUE", "ON", "1"}
    FALSES = {"NO", "FALSE", "OFF", "0"}

    @classmethod
    def is_set(cls, val):
        return not val.upper().strip().equals("NOT_SET")

    @classmethod
    def is_not_set(cls, val):
        return val.upper().strip().equals("NOT_SET")

    @classmethod
    def is_none(cls, val):
        return val == None

    is_null = is_none

    @classmethod
    def is_na(cls, val):
        return val.upper().strip().equals("NA")

    @classmethod
    def __wrong_repr(cls, val, target):
        raise UnsupportedRepresentationException(val, target)

    @classmethod
    def as_enum(cls, val, enum_class):
        try:
            return enum_class[val]
        except:
            cls.__wrong_repr(val, "enum constant of type " + enum_class.__name__)

    @classmethod
    def as_bool(cls, val):
        fstr = str(val)
        if fstr in cls.TRUES:
            return True
        elif fstr in cls.FALSES:
            return False
        cls.__wrong_repr(val, "boolean")

    @classmethod
    def as_number(cls, val):
        fstr = str(val)
        if re.match(r"(\-)?[0-9\.]+", fstr):
            return float(fstr)
        elif re.match("(\-)?[0-9]+", fstr):
            return int(fstr)
        else:
            cls.__wrong_repr(val, "number")

    @classmethod
    def as_int(cls, val):
        try:
            return int(float(str(val)))
        except:
            cls.__wrong_repr(val, "int")

    @classmethod
    def as_float(cls, val):
        try:
            return float(str(val))
        except:
            cls.__wrong_repr(val, "float")

    @classmethod
    def as_enum_list(cls, val, enum_class):
        try:
            if type(val) is list:
                return [enum_class[i.upper()] for i in val]
            else:
                return [cls.as_enum(val, enum_class)]
        except:
            cls.__wrong_repr(val, "enum constant list of type " + enum_class.__name__)

    @classmethod
    def as_number_list(cls, val):
        try:
            return [cls.as_number(val)]
        except:
            cls.__wrong_repr(val, "number list")
    
    @classmethod
    def as_int_list(cls, val):
        try:
            return [cls.as_int(val)]
        except:
            cls.__wrong_repr(val, "int list")
    
    @classmethod
    def as_str_list(cls, val):
        try:
            return [str(val)]
        except:
            cls.__wrong_repr(val, "string list")

    @classmethod
    def split_as_str_list(cls, val, delimiter=","):
        try:
            return data_utils.split(str(val), delimiter=delimiter)
        except:
            cls.__wrong_repr(val, "string list")

