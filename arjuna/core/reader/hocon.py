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
import os

from pyhocon import ConfigFactory
from pyhocon import ConfigTree, config_tree

def escape_value(value):
    return value.replace('=', '\\=').replace('!', '\\!').replace('#', '\\#').replace('\n', '\\\n')


class HoconReader(metaclass=abc.ABCMeta):
    def __init__(self):
        self.__map = {}
        self.__conf = None

    def get_flat_map(self):
        return self.__map

    def get_map(self):
        return self.__conf

    @abc.abstractmethod
    def _load_config(self):
        pass

    def set_config(self, conf):
        self.__conf = conf
    #
    # def __get_primitive(self, config):
    #     return config
    #     # if isinstance(config, config_tree.NoneValue):
    #     #     return NONE
    #     # elif isinstance(config, list):
    #     #     return ObjectListValue(config)
    #     # elif isinstance(config, str):
    #     #     return StringValue(config)
    #     # elif isinstance(config, bool):
    #     #     return BooleanValue(config)
    #     # else:
    #     #     return NumberValue(config)

    # def process(self):
    #     def inner(config, od, key_stack=[], out=None):
    #         if isinstance(config, ConfigTree):
    #             for key, item in config.items():
    #                 if isinstance(item, ConfigTree):
    #                     od[key] = {}
    #                     d = od[key]
    #                 else:
    #                     d = od
    #                 inner(item, d, key_stack + [key], out)
    #         elif isinstance(config, list):
    #             k = key_stack[-1]
    #             out['.'.join(key_stack)] = []
    #             od[k] = []
    #             for index, item in enumerate(config):
    #                 to_append = None
    #                 if item is not None:
    #                     if isinstance(item, ConfigTree):
    #                         d = {}
    #                         inner(item, d, [], {})
    #                         to_append = d
    #                     else:
    #                         to_append = self.__get_primitive(item)
    #                 out['.'.join(key_stack)].append(to_append)
    #                 od[k].append(to_append)
    #         else:
    #             k = key_stack[-1]
    #             p = self.__get_primitive(config)
    #             od[k] = p
    #             # out is None only for the first time call
    #             # if out is empty, it needs to be populated, so DO NOT DO PY BOOL i.e. if out:
    #             if out is not None:
    #                 out['.'.join(key_stack)] = p
    #
    #     self._load_config()
    #     inner(self.__conf, self.__nested, [], self.__map)
    #     # ArjunaCore.console.display(self.__conf)
    #     # ArjunaCore.console.display(self.__map)


    ######################################################################
    # Modified version of to_properties from pychocon package.
    # License details for pyhocon are listed in license.txt file.
    ######################################################################

    def process(self):
        def inner(out, config, key_stack=[]):
            if isinstance(config, ConfigTree):
                for key, item in config.items():
                    if item is not None:
                        inner(out, item, key_stack + [key])
            elif isinstance(config, config_tree.NoneValue):
                out[".".join(key_stack)] = None
            else:
                out[".".join(key_stack)] = config

        self._load_config()
        inner(self.__map, self.__conf)

class HoconConfigDictReader(HoconReader):
    def __init__(self, conf):
        super().__init__()
        self.set_config(conf)

    def _load_config(self):
        pass


class HoconFileReader(HoconReader):
    def __init__(self, path):
        super().__init__()
        self.conf_path = path

    def _load_config(self):
        self.set_config(ConfigFactory.parse_file(self.conf_path))


class HoconResourceReader(HoconFileReader):
    def __init__(self, name):
        # ArjunaCore.console.display(os.path.abspath(os.path.join(os.path.dirname(__file__), os.sep.join(["../..", "res", name]))))
        super().__init__(os.path.abspath(os.path.join(os.path.dirname(__file__), os.sep.join(["../..", "res", name]))))


class HoconStringReader(HoconReader):
    def __init__(self, conf_string):
        super().__init__()
        self.conf_string = conf_string

    def _load_config(self):
        conf = ConfigFactory.parse_string(self.conf_string.replace("\\\\\\\\", "fourslash").replace("\\\\", "twoslash")
                                          .replace("\\", "\\\\")
                                          .replace("twoslash", "\\\\")
                                          .replace("fourslash", "\\\\\\\\"))
        self.set_config(conf)
