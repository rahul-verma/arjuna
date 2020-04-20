import os
import yaml

from arjuna.tpi.helper.arjtype import CIStringDict

class Yaml:

    def __init__(self, name, ydict):
        self.__name = name
        self.__ydict = ydict is not None and ydict or dict()
        self.__sections = tuple(self.__ydict.keys())
        self.__ydict = CIStringDict(self.__ydict)

    @property
    def name(self):
        return self.__name

    def is_empty(self):
        return not self.__ydict

    def get_section(self, name):
        if not self.has_section(name):
            raise Exception(f"Yaml object does not have a section with the name: {name}")
        return Yaml(name, self.__ydict[name])

    def get_value(self, name):
        if not self.has_section(name):
            raise Exception(f"Yaml object does not have a section with the name: {name}")
        return self.__ydict[name]

    def as_map(self):
        return self.__ydict

    def has_section(self, name):
        return name in self.__ydict

    @property
    def section_names(self):
        return self.__ydict.keys()


class YamlFile(Yaml):

    def __init__(self, fpath):
        yaml_name = os.path.basename(fpath).split(".yaml")[0]
        f = open(fpath, "r")
        ydict = yaml.load(f, Loader=yaml.SafeLoader)
        f.close()
        super().__init__(yaml_name, ydict)

    

    