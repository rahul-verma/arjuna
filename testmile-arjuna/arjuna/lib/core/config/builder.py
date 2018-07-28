'''
This file is a part of Test Mile Arjuna
Copyright 2018 Test Mile Software Testing Pvt Ltd

Website: www.TestMile.com
Email: support [at] testmile.com
Creator: Rahul Verma

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

from arjuna.lib.core.config.property import *


class ConfigPropertyBuilder:
    def __init__(self):
        self.__reset()

    def __reset(self):
        self.__definer = "User_defined"
        self.__code = None
        self.__path = None
        self.__level = ConfigPropertyLevelEnum.CENTRAL
        self.__text = None
        self.__overridable = True
        self.__visible = True
        self.__value = None
        self.__value_type = ValueTypeEnum.STRING

    def code(self, code):
        self.__code = str(code)
        self.__definer = code.__class__.__name__
        return self

    def path(self, path):
        self.__path = path
        if self.__text is None:
            self.__text = self.__path.upper()
        return self

    def level(self, level):
        self.__level = level
        return self

    def text(self, text):
        self.__text = text
        return self

    def overridable(self, override):
        self.__overridable = override
        return self

    def visible(self, visible):
        self.__visible = visible
        return self

    def value(self, value):
        self.__value = value
        return self

    def value_type(self, v_type):
        self.__value_type = v_type
        return self

    def build(self):
        prop = ConfigProperty(self.__code, self.__path, self.__value, self.__text,
                              self.__visible, self.__value_type,
                              self.__level, self.__definer, self.__overridable)
        self.__reset()
        return prop
