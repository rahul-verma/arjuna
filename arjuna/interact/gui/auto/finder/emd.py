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

import re
from enum import Enum, auto
from collections import namedtuple

from arjuna.core.enums import GuiElementType

class ImplWith:
    
    def __init__(self, *, wtype, wvalue, named_args, has_content_locator):
        self.wtype = wtype
        self.wvalue = wvalue
        self.named_args = named_args
        self.has_content_locator = has_content_locator

class MobileNativeLocateWith(Enum):
    ID = auto()
    NAME = auto() 
    XPATH = auto() 
    CLASS_NAME = auto() 
    LINK_TEXT = auto() 
    LINK_PTEXT = auto() 
    TAG_NAME = auto()
    TEXT = auto() 
    TITLE = auto() 
    PARTIAL_TEXT = auto() 
    TYPE = auto() 
    VALUE = auto() 
    IMAGE_SRC = auto()

class MobileWebLocateWith(Enum):
    ID = auto()
    NAME = auto() 
    XPATH = auto() 
    CSS_SELECTOR = auto()
    CLASS_NAME = auto() 
    LINK_TEXT = auto() 
    LINK_PTEXT = auto() 
    TAG_NAME = auto()
    TEXT = auto() 
    TITLE = auto() 
    PARTIAL_TEXT = auto() 
    TYPE = auto() 
    VALUE = auto() 
    IMAGE_SRC = auto()

class NativeLocateWith(Enum):
    ID = auto()
    NAME = auto() 
    XPATH = auto() 
    CLASS_NAME = auto() 
    LINK_TEXT = auto() 
    LINK_PTEXT = auto() 
    TEXT = auto() 
    TITLE = auto() 
    PARTIAL_TEXT = auto() 
    TYPE = auto() 
    VALUE = auto() 
    IMAGE_SRC = auto()

class VisualLocateWith(Enum):
    IMAGE = auto()

class WebLocateWith(Enum):
    ID = auto()
    NAME = auto() 
    XPATH = auto() 
    CSS_SELECTOR = auto()
    CLASS_NAME = auto() 
    LINK_TEXT = auto() 
    LINK_PTEXT = auto() 
    TAG_NAME = auto()
    CLASS_NAMES = auto()
    TEXT = auto() 
    TITLE = auto() 
    PARTIAL_TEXT = auto() 
    ATTR_VALUE = auto()
    ATTR_PARTIAL_VALUE = auto()
    TYPE = auto() 
    VALUE = auto() 
    IMAGE_SRC = auto()
    WINDOW_TITLE = auto()
    PARTIAL_WINDOW_TITLE = auto()

class GenericLocateWith(Enum):
    ID = auto()
    NAME = auto() 
    XPATH = auto() 
    CSS_SELECTOR = auto()
    CLASS_NAME = auto() 
    LINK_TEXT = auto() 
    LINK_PTEXT = auto() 
    TAG_NAME = auto()

    INDEX = auto()
    WINDOW_TITLE = auto()
    WINDOW_PTITLE = auto()
    CONTENT_LOCATOR = auto()
    POINT = auto()
    JAVASCRIPT = auto()   

    #Translated to CSS Selectors
    COMPOUND_CLASS = auto()
    CLASS_NAMES = auto()

    # Translated to XPath
    TEXT = auto() 
    TITLE = auto() 
    PTEXT = auto() 
    TYPE = auto() 
    VALUE = auto() 
    ATTR_VALUE = auto()
    ATTR_PVALUE = auto()
    IMAGE_SRC = auto()
    IMAGE = auto()

    # These need to be translated to
    PARTIAL_LINK_TEXT = auto()

class Locator:

    def __init__(self, ltype, lvalue, named_args):
        self.ltype = ltype
        self.lvalue = lvalue
        self.__named_args = named_args

    def set_args(self,  named_args):
        self.__named_args = named_args

    @property
    def named_args(self):
        return self.__named_args

    def __str__(self):
        return str(vars(self))

    def is_layered_locator(self):
        return False

class GuiGenericLocator(Locator):

    def __init__(self, ltype, lvalue, named_args):
        super().__init__(ltype, lvalue, named_args)
    
    def set_value(self, value):
        self.lvalue = value

    def as_map(self):
        map = dict()
        map["withType"] = self.ltype.name
        if self.ltype.name.lower() != "content_locator":
            map["withValue"] = self.lvalue
        else:
            map["withValue"] = [l.as_map() for l in self.lvalue.locators]

        # if self.__named_args:
        #     map["named_args"] = self.__named_args
        
        return map

# class GuiGenericChildLocator(Locator):
#     def __init__(self, ltype, lvalue, named_args):
#         super().__init__(ltype, lvalue, named_args)
    
#     def set_value(self, value):
#         self.lvalue = value    

#     def is_layered_locator(self):
#         return True

class GuiElementMetaData:
    XPATH_TWO_ARG_VALUE_PATTERN = r'^\s*\[\s*(\w+)\s*\]\s*\[\s*(\w+)\s*\]$'

    BASIC_LOCATORS = {
        GenericLocateWith.ID,
        GenericLocateWith.NAME,
        GenericLocateWith.CLASS_NAME,
        GenericLocateWith.LINK_TEXT,
        GenericLocateWith.XPATH,
        GenericLocateWith.CSS_SELECTOR,
        GenericLocateWith.TAG_NAME,
        GenericLocateWith.IMAGE,
        GenericLocateWith.INDEX,
        GenericLocateWith.WINDOW_TITLE,
        GenericLocateWith.WINDOW_PTITLE,
        GenericLocateWith.POINT,
        GenericLocateWith.JAVASCRIPT,
    }

    NEED_TRANSLATION = {
        GenericLocateWith.LINK_PTEXT : GenericLocateWith.PARTIAL_LINK_TEXT
    }

    XTYPE_LOCATORS = {
        GuiElementType.TEXTBOX: "//input[@type='text']",
        GuiElementType.PASSWORD: "//input[@type='password']",
        GuiElementType.LINK: "//a",
        GuiElementType.BUTTON: "//input[@type='button']",
        GuiElementType.SUBMIT_BUTTON: "//input[@type='submit']",
        GuiElementType.DROPDOWN: "//select",
        GuiElementType.CHECKBOX: "//input[@type='checkbox']",
        GuiElementType.RADIO: "//input[@type='radio']",
        GuiElementType.IMAGE: "//img",
    }

    XPATH_LOCATORS = {
        GenericLocateWith.TEXT : "//*[text()='{}']",
        GenericLocateWith.PTEXT : "//*[contains(text(),'{}')]",
        GenericLocateWith.VALUE : "//*[@value='{}']",
        GenericLocateWith.TITLE : "//*[@title='{}']",
        GenericLocateWith.IMAGE_SRC : "//img[@src='{}']"
    }

    XPATH_TWO_ARG_LOCATORS = {
        GenericLocateWith.ATTR_VALUE : "//*[@{}='{}']",
        GenericLocateWith.ATTR_PVALUE : "//*[contains(@{},'{}')]"
    }

    def __init__(self, raw_locators, process_args=True):
        self.__raw_locators = raw_locators
        self.__locators = []
        self.__process()
        if process_args:
            self.process_args()

    def __str__(self):
        return str([str(l) for l in self.__locators])

    def print_locators(self):
        print(str(self))

    @property
    def locators(self):
        return self.__locators

    @property
    def raw_locators(self):
        return self.__raw_locators

    def __process(self):
        for raw_locator in self.__raw_locators:
            rltype = raw_locator.ltype
            rlvalue = raw_locator.lvalue
            named_args = raw_locator.named_args
            try:
                generic_locate_with = GenericLocateWith[rltype.upper()]
            except:
                raise Exception("Invalid locator across all automators: {}".format(rltype))
            else:
                if generic_locate_with == GenericLocateWith.CONTENT_LOCATOR:
                    self.__add_locator(generic_locate_with, rlvalue, named_args)
                elif generic_locate_with in self.BASIC_LOCATORS:
                    self.__add_locator(generic_locate_with, rlvalue, named_args)
                elif generic_locate_with in self.NEED_TRANSLATION:
                    self.__add_locator(self.NEED_TRANSLATION[generic_locate_with], rlvalue, named_args)
                elif generic_locate_with in self.XPATH_LOCATORS:
                    self.__add_locator(GenericLocateWith.XPATH, self.XPATH_LOCATORS[generic_locate_with].format(rlvalue), named_args)
                elif generic_locate_with in self.XPATH_TWO_ARG_LOCATORS:
                    parts = None
                    try:
                        parts =  re.search(GuiElementMetaData.XPATH_TWO_ARG_VALUE_PATTERN, rlvalue).groups()
                    except:
                        raise Exception("Value {} for {} is misformatted. Attribute name and attribute value should be supplied as: [<arg>][<value>]".format(rlvalue, rltype))
                    self.__add_locator(GenericLocateWith.XPATH, self.XPATH_TWO_ARG_LOCATORS[generic_locate_with].format(parts[0], parts[1]), named_args)
                elif generic_locate_with == GenericLocateWith.TYPE:
                    try:
                        elem_type = GuiElementType[rlvalue.upper()]
                    except:
                        raise Exception("Unsupported element type for XTYPE locator: " + rlvalue)
                    else:
                        self.__add_locator(GenericLocateWith.XPATH, self.XTYPE_LOCATORS[elem_type], named_args)
                elif generic_locate_with == GenericLocateWith.COMPOUND_CLASS:
                    self.__add_locator(GenericLocateWith.CSS_SELECTOR, re.sub(r'\s+', '.', "." + rlvalue.replace('.', ' ').strip()), named_args)
                elif generic_locate_with == GenericLocateWith.CLASS_NAMES:
                    self.__add_locator(GenericLocateWith.CSS_SELECTOR, "." + ".".join(rlvalue), named_args)
                else:
                    raise Exception("Locator not supported yet by Arjuna: " + rltype)

    def __add_locator(self, locator_type, locator_value, named_args):
        self.locators.append(GuiGenericLocator(locator_type, locator_value, named_args))

    def process_args(self):
        '''
            It consumes impl locator list.
        '''
        pattern = r"\$(\s*\w*?\s*)\$"
        for locator in self.locators:
            if locator.ltype == GenericLocateWith.CONTENT_LOCATOR:
                locator.lvalue.process_args()

            if not locator.named_args: continue

            fmt_locator_value = locator.lvalue.replace("\{", "__LB__").replace("}", "__RB__")

            # Find params
            matches = re.findall(pattern, fmt_locator_value)
            
            for match in matches:
                target = "${}$".format(match)
                repl = "{" + match.lower().strip() + "}"
                fmt_locator_value = fmt_locator_value.replace(target, repl)

            repl = {k.lower():v for k,v in locator.named_args.items()}
            fmt_locator_value = fmt_locator_value.format(**repl)
            fmt_locator_value = fmt_locator_value.replace("__LB__", "{").replace("__RB__", "}")
            locator.set_value(fmt_locator_value)


    @classmethod
    def __process_single_raw_locator(cls, impl_locator):
        ltype = impl_locator.wtype
        lvalue = impl_locator.wvalue
        p_locator = Locator(ltype=ltype, lvalue=lvalue, named_args=impl_locator.named_args)
        return p_locator

    @classmethod
    def convert_to_impl_with_locators(cls, *with_locators):
        out_list = []
        for locator in with_locators:
            l = isinstance(locator, ImplWith) and locator or locator.as_impl_locator()
            out_list.append(l)
        return out_list

    @classmethod
    def create_lmd(cls, *locators):
        impl_locators = cls.convert_to_impl_with_locators(*locators)
        processed_locators = []
        for locator in impl_locators:
            ltype = locator.wtype.lower()
            if ltype == "content_locator":
                CONTENT_LOCATOR = cls.create_lmd(locator.wvalue)
                p_locator = Locator(ltype=locator.wtype, lvalue=CONTENT_LOCATOR, named_args=None)
            else:
                p_locator = cls.__process_single_raw_locator(locator)
            processed_locators.append(p_locator)
        return GuiElementMetaData(processed_locators)

    @staticmethod
    def locators_as_str(locators):
        out_list = []
        for l in locators:
            if isinstance(l, GuiGenericLocator):
                out_list.append(l.as_map())
            else:
                out_list.append(str(l))
        return out_list

class SimpleGuiElementMetaData(GuiElementMetaData):

    def __init__(self, locator_type, locator_value, named_args=dict()):
        super().__init__([Locator(ltype=locator_type, lvalue=locator_value, named_args=named_args)])
