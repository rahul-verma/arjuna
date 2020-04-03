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

from enum import Enum, auto

from arjuna.tpi.enums import GuiInteractionConfigType

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


class GuiInteractionConfig:
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


class Keyboard:

    class KeyChord:

        def __init__(self):
            self.__parts = []

        def text(self, text):
            self.__parts.append(text)
            return self

        def key(self, key):
            self.__parts.append(key.name)
            return self

        @property
        def parts(self):
            return self.__parts

    @classmethod
    def chord(self):
        '''
            Returns a new KeyChord object.
        '''
        return KeyChord()

class _Point:

    def __init__(self, x, y):
        self.__x = x
        self.__y = y

    @property
    def location(self):
        return (self.__x, self.__y)

class _Offset(_Point):

    def __init__(self, x, y):
        super().__init__(x,y)

class Screen:

    @staticmethod
    def xy(x, y):
        return _Point(x,y)

    @staticmethod
    def offset(x, y):
        return _Offset(x,y)


class Dictable:

    pass

class NV(Dictable):

    def __init__(self, name, value):
        self.__name = name
        self.__value = value

    def as_dict(self):
        return {"name" : self.__name, "value": self.__value}

class Attr(NV):

    def __init__(self, name, value, tag=None):
        super().__init__(name, value)
        self.__tag = tag

    def as_dict(self):
        d = super().as_dict()
        d["tag"] = self.__tag
        return d


class Point(Dictable):

    def __init__(self, x, y):
        self.__x = x
        self.__y = y

    def as_dict(self):
        return {"x": self.__x, "y":self.__y}

class Params(Dictable):

    def __init__(self, **kwargs):
        self.__kwargs = kwargs

    def as_dict(self):
        return self.__kwargs

class Formatter:

    def __init__(self, **kwargs):
        self.__fargs = kwargs

    def locator(self, template="element", **kwargs):
        return Locator(template=template, fmt_args=self.__fargs, **kwargs)

class Locator(Dictable):

    def __init__(self, template="element", fmt_args=None, **named_args):
        self.__template = template

        self.__fmt_args = fmt_args
        if self.__fmt_args is None:
            self.__fmt_args = dict()

        self.__named_args = named_args

        from arjuna.interact.gui.auto.finder.meta import Meta
        self.__meta = Meta({
            "template" : template,
        })

    @property
    def template(self):
        return self.__template

    @property
    def fmt_args(self):
        return self.__fmt_args

    @property
    def named_args(self):
        return self.__named_args

    def __str__(self):
        return str(
            {
                "template": self.template,
                "fmt_args": self.fmt_args,
                "meta": str(self.__meta)
            }
        )

    def as_raw_emd(self):
        from arjuna import Arjuna
        from arjuna.interact.gui.auto.finder._with import With
        from arjuna.interact.gui.auto.finder.enums import WithType
        with_list = []
        for k,v in self.__named_args.items():
            if k.upper() in WithType.__members__:
                if isinstance(v, Dictable):
                    v = v.as_dict()
                with_list.append(getattr(With, k.lower())(v))
            elif Arjuna.get_withx_ref().has_locator(k):
                if isinstance(v, Dictable):
                    v = v.as_dict()
                    with_list.append(getattr(With, k.lower())(**v))
                else:
                    with_list.append(getattr(With, k.lower())(v))
            else:
                self.__meta[k] = v
        if not with_list:
            raise Exception("You must provide atleast one locator.")
        from arjuna.interact.gui.auto.finder.emd import GuiElementMetaData
        return GuiElementMetaData.create_emd(*with_list, meta=self.__meta)

    def as_emd(self):
        emd = self.as_raw_emd()
        fmt_emd = emd.create_formatted_emd(**self.__fmt_args)
        return fmt_emd



