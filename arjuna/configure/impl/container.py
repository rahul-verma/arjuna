'''
This file is a part of Arjuna
Copyright 2015-2020 Rahul Verma

Website: www.RahulVerma.net

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

  http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
'''

from arjuna.core.value import AbstractValueMap, StringKeyValueMap
from arjuna import ArjunaOption

from .config import Config

class ArjunaOptionMap(AbstractValueMap):

    def __init__(self, object_map=None, headers=None, objects=None):
        super().__init__(object_map, headers, objects)

    def _format_key_as_str(self, key):
        return str(key)

class ConfigContainer:

    def __init__(self):
        self.__arjuna_options = ArjunaOptionMap()
        self.__user_options = StringKeyValueMap()

    @property
    def arjuna_options(self):
        return self.__arjuna_options

    @property
    def user_options(self):
        return self.__user_options

    def set_arjuna_option(self, arjuna_option, obj):
        if isinstance(arjuna_option, ArjunaOption):
            self.__arjuna_options.add_object(arjuna_option.name, obj)
        else:
            normalized_option = Config.normalize_option_str(arjuna_option)
            self.__arjuna_options.add_object(ArjunaOption[normalized_option], obj)
        return self

    def set_user_option(self, option, obj):
        self.__user_options.add_object(Config.normalize_option_str(option), obj)
        return self

    def set_option(self, option, obj):
        normalized_option = Config.normalize_option_str(option)
        try:
            arj_option = ArjunaOption[normalized_option]
            self.set_arjuna_option(arj_option, obj)
        except:
            self.set_user_option(option, obj)
        return self

    def add_options(self, options):
        for option, obj in options.items():
            self.set_option(option, obj)
        return self

    def is_empty(self):
        if not self.arjuna_options and not self.user_options:
            return True
        return False