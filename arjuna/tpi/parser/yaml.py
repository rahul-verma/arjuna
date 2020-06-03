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


import os
import yaml

from arjuna.tpi.helper.arjtype import CIStringDict
from arjuna.core.error import YamlError, YamlUndefinedSectionError

class YamlElement:

    def __init__(self, pydict_or_list, *, name="yaml", file_path=None):
        self.__pyobj = pydict_or_list
        self.__name = name
        self.__file_path = file_path

    @property
    def name(self):
        return self.__name

    @property
    def file_path(self):
        return self.__file_path

    def is_empty(self):
        return not self.__ydict

    def as_str(self):
        return yaml.dump(self.__pyobj).replace("_ArDict__store:\n","")

    def __str__(self):
        return self.as_str()

class YamlList(YamlElement):

    def __init__(self, pylist, *, name="yaml", file_path=None):
        self.__ylist = pylist is not None and pylist or list()
        super().__init__(self.__ylist, name=name, file_path=file_path)
        self.__iter = None    

    def __iter__(self):
        self.__iter = iter(self.__ylist)
        return self

    def __next__(self):
        return self.get_section(next(self.__iter), allow_any=True)    


class YamlDict(YamlElement):

    def __init__(self, pydict, *, name="yaml", file_path=None):
        self.__ydict = pydict is not None and pydict or dict()
        self.__sections = tuple(self.__ydict.keys())
        self.__ydict = CIStringDict(self.__ydict)
        super().__init__(self.__ydict, name=name, file_path=file_path)
        self.__iter = None

    def __iter__(self):
        self.__iter = iter(self.__ydict)
        return self

    def __next__(self):
        return self.get_section(next(self.__iter), allow_any=True)

    def get_section(self, name, *, strict=True, as_yaml_str=False, allow_any=False):
        val = self.__get_value(name, strict=strict)
        if as_yaml_str:
            return yaml.dump(val)
        return Yaml.from_object(val, name=name, file_path=self.file_path, allow_any=allow_any)

    def __get_value(self, name, *, strict=True):
        if self.has_section(name):
            return self.__ydict[name]
        else:
            if strict:
                raise YamlUndefinedSectionError(f"Yaml object does not have a section with the name: {name}")
            else:
                return None

    def as_map(self):
        return self.__ydict

    def has_section(self, name):
        return name in self.__ydict

    @property
    def section_names(self):
        return self.__ydict.keys()

    def validate_sections_present(*section_names, atleast_one=False):
        absent_sections = []
        present_section_names = self.section_names
        for section_name in section_names:
            if section_name not in present_section_names:
                absent_sections.append(section_name)

        if len(absent_sections) == section_names or (len(absent_sections) < len(section_names) and not atleast_one):
            raise YamlUndefinedSectionError(f"Yaml object does not contains mandatory sections: {absent_sections}") 

class Yaml:

    @classmethod
    def from_object(cls, pyobj, *, name="yaml", file_path=None, allow_any=False):
        if type(pyobj) is dict:
            return YamlDict(pyobj, name=name, file_path=file_path)
        elif type(pyobj) is list:
            return YamlList(pyobj, name=name, file_path=file_path)
        else:
            if allow_any:
                return pyobj
            else:
                raise Exception("Unknown object type for Yaml: {}".format(type(pyobj)))

    @classmethod
    def from_file(cls, *, file_path, allow_any=False):
        yaml_name = os.path.basename(file_path).split(".yaml")[0]
        f = open(file_path, "r")
        ydict = yaml.load(f, Loader=yaml.SafeLoader)
        f.close()
        return cls.from_object(ydict, name=yaml_name, file_path=file_path, allow_any=allow_any)

    @classmethod
    def from_str(cls, contents, *, name="yaml", allow_any=False):
        return cls.from_object(yaml.safe_load(contents), name=name, allow_any=allow_any)



    

    