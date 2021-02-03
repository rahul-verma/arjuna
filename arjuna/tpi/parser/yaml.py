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
Classes to assist in YAML Parsing. 
'''

import os
import yaml
import abc
import copy
from json import JSONEncoder

from arjuna.tpi.helper.arjtype import CIStringDict
from arjuna.core.error import YamlError, YamlUndefinedSectionError, YamlListIndexError

# Custom tag handlers
def join_tag(loader, node):
    seq = loader.construct_sequence(node)
    return ''.join([str(i) for i in seq])

# register tag handlers
yaml.add_constructor('!join', join_tag, Loader=yaml.SafeLoader)

class YamlElement(metaclass=abc.ABCMeta):
    '''
        Abstract Json Element. Base class for YamlList and YamlDict.
    '''

    def __init__(self, pydict_or_list):
        super().__init__()
        self.__pyobj = pydict_or_list

    def is_empty(self):
        return not self.store

    def as_str(self):
        '''
            Get string representation of this Yaml Element.
        '''
        return yaml.dump(self.__pyobj).replace("_ArDict__store:\n","")

    __str__ = as_str 
    

    def __repr__(self):
        return "Yaml as PyObj: " + str(self.__pyobj)

    def _get_item(self, name, *, strict=True, as_yaml_str=False, allow_any=False):
        val = self._get_value(name, strict=strict)
        if as_yaml_str:
            return yaml.dump(val)
        return Yaml.from_object(val, allow_any=allow_any)

    @abc.abstractmethod
    def _get_value(self, name_or_index, *, strict=True):
        pass

class YamlList(YamlElement, JSONEncoder):
    '''
        Encapsulates a list object in YAML.

        Arguments:
            pylist: Python list

        Note:
            Supports indexing just like a Python list.

            Also supports == operator. Right operand can be a Python list or a `YamlList` object.
    '''

    def __init__(self, pylist):
        self.__ylist = pylist is not None and pylist or list()
        YamlElement.__init__(self, self.__ylist)
        JSONEncoder.__init__(self)
        self.__iter = None   

    def __len__(self):
        return len(self.__ylist)

    def default(self, o):
        return self.raw_object

    @property
    def size(self):
        '''
            Number of objects in this list.
        '''
        return len(self)

    @property
    def raw_object(self):
        '''
            A copy of the Python list that this object wraps.
        '''
        return copy.deepcopy(self.__ylist)

    def __str__(self):
        return str(self.__ylist)

    def __getitem__(self, index):
        return self.__ylist[index] 

    def __iter__(self):
        self.__iter = iter(self.__ylist)
        return self

    def __next__(self):
        return Yaml.from_object(next(self.__iter), allow_any=True)

    def _get_value(self, index, *, strict=True):
        if len(self.__ylist) < index:
            return self.__ylist[index]
        else:
            if strict:
                raise YamlListIndexError(f"YamlList does not contain index: {index}. List: {self.__ylist}")
            else:
                return None 

    def __eq__(self, other):
        if type(other) is list:
            pass
        elif type(other) is YamlList:
            other = other.raw_object
        elif other is None:
            return False
        else:
            raise Exception("YamlList == operator expects list/YamlList as right operand.")

        if len(self) != len(other):
            return False
        else:
            return self.raw_object == other


class YamlDict(CIStringDict, YamlElement):
    '''
        Encapsulates Dictionary object in Json.

        Arguments:
            pydict: Python dict.

        Note:
            Supports dictionary methods as well as **.** access for key.

            Also supports == operator. Right operand can be a Python dict or a `YamlDict` object.
    '''

    def __init__(self, pydict):
        CIStringDict.__init__(self, pydict)
        YamlElement.__init__(self, self.orig_dict)
        self.__sections = tuple(self.keys())
        self.__iter = None

    @property
    def size(self):
        '''
            Number of key-value pairs in this object.
        '''
        return len(self)

    @property
    def raw_object(self):
        '''
            A copy of the Python dict that this object wraps.
        '''
        return dict(super().items())

    def __getitem__(self, key):
        return self.get_section(key, allow_any=True)

    def items(self):
        '''
            dictitems object containing key-value pairs in this object.
        '''
        return {i:self.get_section(i, allow_any=True) for i in self.orig_dict}.items()

    def __iter__(self):
        self.__iter = iter(self.orig_dict)
        return self

    def __next__(self):
        return Yaml.from_object(next(self.__iter), allow_any=True)

    def get_section(self, name, *, strict=True, as_yaml_str=False, allow_any=False):
        '''
            Get Yaml object for a section/key name.

            Arguments:
                name: Name of section/key

            Keyword Arguments:
                strict: If True, raises Exception when name is not present, else returns None. Default is True.
        '''
        val = self._get_value(name, strict=strict)
        if as_yaml_str:
            return yaml.dump(val)
        return Yaml.from_object(val, allow_any=allow_any)

    def _get_value(self, name, *, strict=True):
        if self.has_section(name):
            return super().__getitem__(name)
        else:
            if strict:
                raise YamlUndefinedSectionError(f"YamlDict object does not have a section with the name: {name}. Dict: {self.orig_dict}")
            else:
                return None

    def as_map(self):
        '''
            A copy of the Python dict that this object wraps.
        '''
        return dict(super().items())

    def has_section(self, name):
        '''
            Check if a key/section name is present. You can also use the 'in' operator instead, like a Python dict.
        '''
        return name in self

    @property
    def section_names(self):
        '''
            All section/key names in this object.
        '''
        return self.keys()

    def validate_sections_present(*section_names, atleast_one=False):
        '''
            Validate the presence of arbitrary section/key names.

            Arguments:
                section_names: arbitrary section/key names

            Keyword Arguments:
                atleast_one: If True, it is expected that atleast one of the sections is present, else all are expected to be present.
        '''
        absent_sections = []
        present_section_names = self.section_names
        for section_name in section_names:
            if section_name not in present_section_names:
                absent_sections.append(section_name)

        if len(absent_sections) == section_names or (len(absent_sections) < len(section_names) and not atleast_one):
            raise YamlUndefinedSectionError(f"Yaml object does not contains mandatory sections: {absent_sections}") 

    def __eq__(self, other):
        if type(other) is dict:
            pass
        elif type(other) is YamlDict:
            other = other.store
        elif other is None:
            return False
        else:
            raise Exception("YamlDict == operator expects dict/YamlDict as right operand. Provided {} of type {}".format(other, type(other)))

        if len(self) != len(other):
            return False
        else:
            return self.store == other

class Yaml:

    @classmethod
    def from_object(cls, yobj, *, allow_any=False):
        '''
            Convert a Python object to a YamlDict/YamlList object if applicable.

            Any iterable which is not a dict is converted to a YamlList.

            Arguments:
                yobj: dict or list or a compatible Python object.

            Keyword Arguments:
                allow_any: If True, if the object can not be coverted, same object is returned, else an Exception is raised.
        '''
        if type(yobj) is dict:
            return YamlDict(yobj)
        elif type(yobj) is list:
            return YamlList(yobj)
        elif type(yobj) is not str:
            try:
                iter(yobj)
                return YamlList(yobj)
            except:
                pass

            if allow_any:
                return yobj
            else:
                raise Exception("Unknown object type for Yaml: {}".format(type(yobj)))
        else:
            if allow_any:
                return yobj
            else:
                raise Exception("Unknown object type for Yaml: {}".format(type(yobj)))            

    @classmethod
    def from_file(cls, file_path, *, allow_any=False):
        '''
            Creates a Yaml object from file.

            Arguments:
                file_path: Absolute path of the yaml file.

            Keyword Arguments:
                allow_any: If True, if the object can not be coverted to a YamlDict/YamlList, same object is returned, else an Exception is raised.

            Returns:
                Arjuna's `YamlDict` or `YamlList` object or the same object for allow_any = True
        '''
        yaml_name = os.path.basename(file_path).split(".yaml")[0]
        f = open(file_path, "r", encoding="utf-8")
        ydict = yaml.load(f, Loader=yaml.SafeLoader)
        f.close()
        return cls.from_object(ydict, allow_any=allow_any)

    @classmethod
    def from_str(cls, ystr, *, name="yaml", allow_any=False):
        '''
            Creates a Yaml object from a YAML string.

            Arguments:
                ystr: A string representing a compatible Python object.

            Keyword Arguments:
                allow_any: If True, if the object can not be coverted to a YamlDict/YamlList, same object is returned, else an Exception is raised.

            Returns:
                Arjuna's `YamlDict` or `YamlList` object or the same object for allow_any = True
        '''
        return cls.from_object(yaml.safe_load(ystr), allow_any=allow_any)



    

    