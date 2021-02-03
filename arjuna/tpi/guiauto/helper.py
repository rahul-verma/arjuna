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

from enum import Enum, auto

from arjuna.core.constant import GuiInteractionConfigType
from arjuna.tpi.helper.arjtype import Dictable
from arjuna.tpi.tracker import track


class _GuiInteractionConfigBuilder:

    def __init__(self):
        self.__settings = dict()

    def check_type(self, flag):
        self.__settings[GuiInteractionConfigType.CHECK_TYPE] = flag
        return self

    def check_pre_state(self, flag):
        self.__settings[GuiInteractionConfigType.CHECK_PRE_STATE] = flag
        return self

    def check_post_state(self, flag):
        self.__settings[GuiInteractionConfigType.CHECK_POST_STATE] = flag
        return self

    def scroll_to_view(self, flag):
        self.__settings[GuiInteractionConfigType.SCROLL_TO_VIEW] = flag
        return self

    def build(self):
        return GuiInteractionConfig(self.__settings)


class _GuiInteractionConfig:
    '''
        Stores configured values for behavior of actions on a given GuiElement.
    '''

    def __init__(self, settings):
        '''
            settings is a dict of dict of GuiInteractionConfigType key/value pairs
        '''
        # 
        self.__settings = settings

    @property
    def settings(self):
        '''
            Returns the dictionary of configured values for actions configuration.
        '''
        return self.__settings

    @staticmethod
    def builder():
        '''
            Returns a builder object to construct object of this class incrementally.
        '''
        return _GuiInteractionConfigBuilder()


@track("trace")
class GuiDriverExtendedConfig:

    def __init__(self, capabilities, browser_args, browser_prefs, browser_exts):
        self.__capabilities = capabilities
        self.__browser_args = browser_args
        self.__browser_prefs = browser_prefs
        self.__browser_exts = browser_exts

    @property
    def config(self):
        '''
            Returns all configuration settings as a single dictionary.
        '''
        map = dict()
        map["driverCapabilities"] = self.__capabilities
        map["browserArgs"] = self.__browser_args 
        map["browserPreferences"] = self.__browser_prefs
        map["browserExtensions"] = self.__browser_exts
        return map

@track("trace")
class GuiDriverExtendedConfigBuilder:

    def __init__(self):
        self.__capabilities = dict() 
        self.__browser_args = []
        self.__browser_prefs = dict()
        self.__browser_exts = []

    def capability(self, name, value):
        self.__capabilities[name] = value
        return self

    def browser_arg(self, arg):
        self.__browser_args.append(arg)
        return self

    def browser_pref(self, name, value):
        self.__browser_prefs[name] = value
        return self

    def browser_ext(self, path):
        self.__browser_exts.append(path)
        return self

    def build(self):
        return GuiDriverExtendedConfig(self.__capabilities, self.__browser_args, self.__browser_prefs, self.__browser_exts)


class Keys:

    class KeyChord:

        def __init__(self):
            self.__parts = []

        def text(self, text):
            self.__parts.append(text)
            return self

        def __getattr__(self, name):
            from selenium.webdriver.common.keys import Keys
            try:
                key_str = getattr(Keys, name.upper())
            except:
                raise AttributeError("There is no key with name {} defined.".format(name))
            else:
                def _dyn_key():
                    self.__parts.append(key_str)
                    return self
                return _dyn_key

        def key(self, key):
            self.__parts.append(key.name)
            return self

        @property
        def _parts(self):
            return self.__parts

    @classmethod
    def chord(cls):
        '''
            Returns a new KeyChord object.
        '''
        return cls.KeyChord()
