import os
import yaml

from arjuna.tpi.helper.arjtype import CIStringDict
from arjuna.tpi.error import YamlError

class Yaml:

    def __init__(self, *, name, pydict, creation_context=""):
        self.__name = name
        self.__ydict = pydict is not None and pydict or dict()
        self.__sections = tuple(self.__ydict.keys())
        self.__ydict = CIStringDict(self.__ydict)
        self.__creation_context = creation_context

    @property
    def name(self):
        return self.__name

    def is_empty(self):
        return not self.__ydict

    def get_section(self, name, *, strict=True):
        val = self.get_value(name, strict=strict)
        if val is not None and type(val) is not dict:
            raise YamlError(f"Section content must be a dictionary. Found content >>{val}<< in {name} section.", creation_context=self.__creation_context)
        return Yaml(name=name, pydict=val, creation_context=self.__creation_context)

    def get_value(self, name, *, strict=True):
        if self.has_section(name):
            return self.__ydict[name]
        else:
            if strict:
                raise YamlError(f"Yaml object does not have a section with the name: {name}", creation_context=self.__creation_context)
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
            raise YamlError(f"Yaml object does not contains mandatory sections: {absent_sections}", creation_context=self.__creation_context) 

    @classmethod
    def from_file(cls, *, file_path, creation_context=""):
        yaml_name = os.path.basename(file_path).split(".yaml")[0]
        f = open(file_path, "r")
        ydict = yaml.load(f, Loader=yaml.SafeLoader)
        f.close()
        return Yaml(name=yaml_name, pydict=ydict)

    @classmethod
    def from_str(cls, *, name, contents, creation_context=""):
        return Yaml(name=name, pydict=yaml.safe_load(contents))



    

    