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

from enum import Enum, auto

from arjuna.core.enums import GuiInteractionConfigType
from arjuna.interact.gui.auto.finder.emd import ImplWith

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

    @staticmethod
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

class WithType(Enum):
    ID = auto()
    NAME = auto()
    CLASSES = auto()
    LINK = auto()
    FLINK = auto()
    TAG = auto()
    XPATH = auto()
    SELECTOR = auto()

    TEXT = auto()
    FTEXT = auto()
    BTEXT = auto()
    ETEXT = auto()
    TITLE = auto()
    ATTR = auto()
    FATTR = auto()
    BATTR = auto()
    EATTR = auto()
    ATTR_WORD = auto()
    TYPE = auto()
    VALUE = auto()
    POINT = auto()
    JS = auto()

    INDEX = auto()
    WINDOW_TITLE = auto()
    WINDOW_PTITLE = auto()
    ELEMENT = auto()
    META = auto()

class With:

    def __init__(self, with_type, with_value):
        '''

        :param with_type: an enum constant of type WithType
        :param with_value: a string or int or a With object.
        '''
        self.__with_type = with_type
        self.__with_value = None
        self.__has_content_locator = False
        self.__content_locator = None
        self.__format_called = False
        self.__named_args = None

        if with_type == WithType.ELEMENT:
            if not isinstance(with_value, With):
                raise Exception("For identification with element locator, the argument must be a With object.")
            else:
                self.__has_content_locator = True
                self.__content_locator = with_value
        else:
            self.__with_value = with_value

    @property
    def wtype(self):
        return self.__with_type

    @property
    def wvalue(self):
        return self.__with_value

    @property
    def named_args(self):
        return self.__named_args

    def raise_format_exc(self):
        if (self.__format_called):
            raise Exception("You can not format a With object more than once.")

    def format(self, **kwargs):
        self.raise_format_exc()
        self.__format_called = True
        self.__named_args = kwargs
        return self

    def as_impl_locator(self):

        impl_with = ImplWith(
            wtype = self.__with_type.name,
            wvalue = self.__has_content_locator and self.__content_locator.as_impl_locator() or self.__with_value,
            named_args = self.__named_args,
            has_content_locator = self.__has_content_locator
        )

        return impl_with

    def as_map(self):
        map = dict()
        map["withType"] = self.__with_type.name
        if not self.__has_content_locator:
            map["withValue"] = self.__with_value
        else:
            map["withValue"] = self.__content_locator.as_map()

        if self.__named_args:
            map["named_args"] = self.__named_args
        
        return map

    @staticmethod
    def id(id):
        return With(WithType.ID, id)

    @staticmethod
    def name(name):
        return With(WithType.NAME, name)

    @staticmethod
    def classes(*names):
        return With(WithType.CLASSES, names)

    @staticmethod
    def link(text):
        return With(WithType.LINK, text)

    @staticmethod
    def flink(text):
        return With(WithType.FLINK, text)

    @staticmethod
    def selector(selector):
        return With(WithType.SELECTOR, selector)

    @staticmethod
    def tag(selector):
        return With(WithType.TAG, selector)

    @staticmethod
    def xpath(xpath):
        return With(WithType.XPATH, xpath)

    @staticmethod
    def text(text):
        return With(WithType.TEXT, text)

    @staticmethod
    def ftext(text):
        return With(WithType.FTEXT, text)

    @staticmethod
    def btext(text):
        return With(WithType.BTEXT, text)

    @staticmethod
    def etext(text):
        return With(WithType.ETEXT, text)

    @staticmethod
    def title(title):
        return With(WithType.TITLE, title)

    @staticmethod
    def attr(attr, value):
        return With(WithType.ATTR, "[{}][{}]".format(attr, value))

    @staticmethod
    def fattr(attr, content):
        return With(WithType.FATTR, "[{}][{}]".format(attr, content))

    @staticmethod
    def battr(attr, content):
        return With(WithType.BATTR, "[{}][{}]".format(attr, content))

    @staticmethod
    def eattr(attr, content):
        return With(WithType.EATTR, "[{}][{}]".format(attr, content))

    @staticmethod
    def value(value):
        return With(WithType.VALUE, value)

    @staticmethod
    def type(type):
        return With(WithType.TYPE, type)

    @staticmethod
    def point(point):
        return With(WithType.POINT, point.location)

    @staticmethod
    def js(js):
        return With(WithType.JS, js)

    @staticmethod
    def index(index):
        return With(WithType.INDEX, index)

    @staticmethod
    def window_title(title):
        return With(WithType.WINDOW_TITLE, title)

    @staticmethod
    def window_ptitle(ptitle):
        return With(WithType.WINDOW_PTITLE, ptitle)

    @staticmethod
    def element(with_obj):
        return With(WithType.ELEMENT, with_obj)

    @staticmethod
    def meta(name):
        return With(WithType.META, name)