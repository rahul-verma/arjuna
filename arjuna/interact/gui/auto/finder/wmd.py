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
from collections import namedtuple

from .meta import Meta
from .enums import WithType
from ._with import With, ImplWith, Locator, GuiGenericLocator
from .translator import LocatorTranslator
from arjuna.core.utils.repr_utils import repr_dict
from arjuna.tpi.tracker import track

@track("trace")
class GuiWidgetMetaData:

    def __init__(self, locators, meta=None, process=True):
        self.__locators = None
        self.__meta = Meta(meta)
        if process:
            self.__raw_locators = locators
            self.__locators = []
            for raw_locator in self.__raw_locators:
                self.locators.append(LocatorTranslator.translate(raw_locator))
        else:
            self.__locators = locators

    @property
    def meta(self):
        return self.__meta

    @property
    def max_wait(self):
        return self.meta.max_wait

    def __str__(self):
        return repr_dict({
            "locators" : [str(l) for l in self.__locators],
            "meta" : str(self.__meta)
        })

    def print_locators(self):
        print(str(self))

    @property
    def locators(self):
        return self.__locators

    @property
    def raw_locators(self):
        return self.__raw_locators

    def create_formatted_wmd(self, **fargs):
        formatted_locators = []
        for locator in self.locators:
            formatted_locator = locator.create_formatted_locator(**fargs)
            formatted_locators.append(formatted_locator)
        return GuiWidgetMetaData(formatted_locators, meta=self.meta, process=False)

    @classmethod
    def __process_single_raw_locator(cls, impl_locator):
        ltype = impl_locator.wtype
        lvalue = impl_locator.wvalue
        p_locator = Locator(ltype=ltype, lvalue=lvalue)
        return p_locator

    @classmethod
    def convert_to_impl_with_locators(cls, *with_locators):
        out_list = []
        for locator in with_locators:
            l = isinstance(locator, ImplWith) and locator or locator.as_impl_locator()
            out_list.append(l)
        return out_list

    @classmethod
    def create_wmd(cls, *locators, meta=None):
        impl_locators = cls.convert_to_impl_with_locators(*locators)
        processed_locators = []
        for locator in impl_locators:
            ltype = locator.wtype.lower()
            if ltype == "content_locator":
                CONTENT_LOCATOR = cls.create_wmd(locator.wvalue)
                p_locator = Locator(ltype=locator.wtype, lvalue=CONTENT_LOCATOR)
            else:
                p_locator = cls.__process_single_raw_locator(locator)
            processed_locators.append(p_locator)
        return GuiWidgetMetaData(processed_locators, meta)

    @staticmethod
    def locators_as_str(locators):
        if not locators:
            return list()

        from arjuna.interact.gui.auto.finder._with import With
        out_list = []
        for l in locators:
            if isinstance(l, GuiGenericLocator) or isinstance(l, With):
                out_list.append(l.as_map())
            else:
                out_list.append(str(l))
        return out_list

class SimpleGuiWidgetMetaData(GuiWidgetMetaData):

    def __init__(self, locator_type, locator_value=dict()):
        super().__init__([Locator(ltype=locator_type, lvalue=locator_value)])
