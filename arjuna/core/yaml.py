import yaml

from arjuna.tpi.helpers.types import CIStringDict

class Yaml:

    def __init__(self, ydict):
        self.__ydict = ydict is not None and ydict or dict()
        self.__sections = tuple(self.__ydict.keys())
        self.__ydict = CIStringDict(self.__ydict)

    def is_empty(self):
        return not self.__ydict

    def get_section(self, name):
        if not self.has_section(name):
            raise Exception(f"Yaml object does not have a section with the name: {name}")
        return Yaml(self.__ydict[name])

    def as_map(self):
        return self.__ydict

    def has_section(self, name):
        return name in self.__ydict


class YamlFile(Yaml):

    def __init__(self, fpath):
        f = open(fpath, "r")
        ydict = yaml.load(f, Loader=yaml.SafeLoader)
        f.close()
        super().__init__(ydict)

    

    