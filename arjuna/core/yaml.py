import os
import yaml

from arjuna.tpi.helper.arjtype import CIStringDict
from arjuna.core.error import YamlError, YamlUndefinedSectionError

class Yaml:

    def __init__(self, *, name, pydict, file_path=None):
        self.__name = name
        self.__ydict = pydict is not None and pydict or dict()
        self.__sections = tuple(self.__ydict.keys())
        self.__ydict = CIStringDict(self.__ydict)
        self.__file_path = file_path

    @property
    def name(self):
        return self.__name

    @property
    def file_path(self):
        return self.__file_path

    def is_empty(self):
        return not self.__ydict

    def get_section(self, name, *, strict=True):
        val = self.get_value(name, strict=strict)
        if val is not None and type(val) is not dict:
            raise YamlError(f"Section content must be a dictionary. Found content >>{val}<< in {name} section.")
        return Yaml(name=name, pydict=val, file_path=self.file_path)

    def get_value(self, name, *, strict=True, as_yaml_str=False):
        if self.has_section(name):
            if as_yaml_str:
                return yaml.dump(self.__ydict[name])
            else:
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

    @classmethod
    def from_file(cls, *, file_path):
        yaml_name = os.path.basename(file_path).split(".yaml")[0]
        f = open(file_path, "r")
        ydict = yaml.load(f, Loader=yaml.SafeLoader)
        f.close()
        return Yaml(name=yaml_name, pydict=ydict, file_path=file_path)

    @classmethod
    def from_str(cls, *, name, contents):
        return Yaml(name=name, pydict=yaml.safe_load(contents))

    def as_str(self):
        return yaml.dump(self.__ydict)



    

    