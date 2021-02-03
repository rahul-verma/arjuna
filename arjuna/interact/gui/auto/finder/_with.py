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

import re

from .enums import WithType, GenericLocateWith
from arjuna.core.utils.repr_utils import repr_dict

class _WithXMetaClass(type):

    def __getattr__(cls, mname):
        from arjuna import Arjuna 
        withx_ref = Arjuna.get_withx_ref()
        if not withx_ref.has_locator(mname):
            raise Exception("There is no built-in or extended locator available as With.{}".format(mname))

        def withx(*vargs, **kwargs): 
            wtype, wvalue = withx_ref.format_args(mname, vargs, kwargs)
            return getattr(With, wtype.lower())(wvalue)
        return withx


class With(metaclass=_WithXMetaClass):

    def __init__(self, with_type, with_value):
        '''

        :param with_type: an enum constant of type WithType
        :param with_value: a string or int or a With object.
        '''
        self.__with_type = with_type
        self.__with_value = None
        self.__has_content_locator = False
        self.__content_locator = None

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

    @wvalue.setter
    def wvalue(self, value):
        self.__with_value = value

    def as_impl_locator(self):

        impl_with = ImplWith(
            wtype = self.__with_type.name,
            wvalue = self.__has_content_locator and self.__content_locator.as_impl_locator() or self.__with_value,
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
        
        return map

    @classmethod
    def id(cls, id):
        return With(WithType.ID, id)

    @classmethod
    def name(cls, name):
        return With(WithType.NAME, name)

    @classmethod
    def classes(cls, *names):
        return With(WithType.CLASSES, names)

    @classmethod
    def link(cls, text):
        return With(WithType.LINK, text)

    @classmethod
    def flink(cls, text):
        return With(WithType.FLINK, text)

    @classmethod
    def selector(cls, selector):
        return With(WithType.SELECTOR, selector)

    @classmethod
    def tags(cls, selector):
        return With(WithType.TAGS, selector)

    @classmethod
    def xpath(cls, xpath):
        return With(WithType.XPATH, xpath)

    @classmethod
    def text(cls, text):
        return With(WithType.TEXT, text)

    @classmethod
    def ftext(cls, text):
        return With(WithType.FTEXT, text)

    @classmethod
    def btext(cls, text):
        return With(WithType.BTEXT, text)

    # Can not be supported as XPath for ends-with does not work in browsers yet.
    # @classmethod
    # def etext(cls, text):
    #     return With(WithType.ETEXT, text)

    @classmethod
    def title(cls, title):
        return With(WithType.TITLE, title)

    @classmethod
    def __validate_attr_map(self, map):
        try:
            rmap = {k.lower():v for k,v in map.items()}
            rmap["name"]
            rmap["value"]
            return rmap
        except:
            raise Exception("Name and value must be supplied. Got: {}".format(map))

    @classmethod
    def _attr(cls, map):
        map = cls.__validate_attr_map(map)
        return With(WithType.ATTR, map)

    @classmethod
    def _fattr(cls, map):
        map = cls.__validate_attr_map(map)
        return With(WithType.FATTR, map)

    @classmethod
    def _battr(cls, map):
        map = cls.__validate_attr_map(map)
        return With(WithType.BATTR, map)

    @classmethod
    def _eattr(cls, map):
        map = cls.__validate_attr_map(map)
        return With(WithType.EATTR, map)   

    @classmethod
    def attr(cls, map):
        return cls._attr(map)

    @classmethod
    def fattr(cls, map):
        return cls._fattr(map)

    @classmethod
    def battr(cls, map):
        return cls._battr(map)

    @classmethod
    def eattr(cls, map):
        return cls._eattr(map)

    @classmethod
    def node(cls, map):
        return With(WithType.NODE, map)

    @classmethod
    def fnode(cls, map):
        return With(WithType.FNODE, map)

    @classmethod
    def bnode(cls, map):
        return With(WithType.BNODE, map)

    @classmethod
    def axes(cls, map):
        return With(WithType.AXES, map)

    @classmethod
    def value(cls, value):
        return With(WithType.VALUE, value)

    @classmethod
    def point(cls, point):
        return With(WithType.POINT, point)

    @classmethod
    def js(cls, js):
        return With(WithType.JS, js)

    @classmethod
    def index(cls, index):
        return With(WithType.INDEX, index)

    @classmethod
    def window_title(cls, title):
        return With(WithType.WINDOW_TITLE, title)

    @classmethod
    def window_ptitle(cls, ptitle):
        return With(WithType.WINDOW_PTITLE, ptitle)

    @classmethod
    def element(cls, with_obj):
        return With(WithType.ELEMENT, with_obj)

    @classmethod
    def label(cls, name):
        return With(WithType.LABEL, name)

class ImplWith:
    
    def __init__(self, *, wtype, wvalue, has_content_locator):
        self.wtype = wtype
        self.wvalue = wvalue
        self.has_content_locator = has_content_locator

    def __str__(self):
        return "ImplWith: {}".format(vars(self))


class Locator:

    def __init__(self, ltype, lvalue=None):
        self.ltype = ltype
        self.lvalue = lvalue

    def set_value(self, value):
        self.lvalue = value

    def create_formatted_locator(self, **fargs):

        def get_global_value(in_str):
            from arjuna import C, L, R
            gtype, query = in_str.split(".", 1)
            gtype = gtype.upper()
            return locals()[gtype](query)


        pattern = r"\$(\s*[\w\.]+?\s*)\$"
        repl_dict = {k.lower():v for k,v in fargs.items()}

        new_locator = Locator(self.ltype)

        if self.ltype == GenericLocateWith.ELEMENT:
            new_locator.set_value(locator.lvalue.create_formatted_locator(**fargs))
            return new_locator

        fmt_locator_value = str(self.lvalue).replace("\{", "__LB__").replace("}", "__RB__")

        # Find params
        matches = re.findall(pattern, fmt_locator_value)
        
        for match in matches:
            names_set = None
            target = "${}$".format(match)
            processed_name = match.lower().strip()
            repl_value = None
            if processed_name.startswith("c.") or processed_name.startswith("l.") or processed_name.startswith("r."):
                repl_value = get_global_value(processed_name)
            else:
                if processed_name not in repl_dict:
                    raise Exception("You must provide named arguments for custom placeholders in locator strings. Placeholder ${}$ does not have corresponding argument passed for locator string {}.".format(processed_name, self.lvalue))
                repl_value = repl_dict[processed_name]

            fmt_locator_value = fmt_locator_value.replace(target, str(repl_value))
            

        fmt_locator_value = fmt_locator_value.replace("__LB__", "{").replace("__RB__", "}")
        new_locator.set_value(fmt_locator_value)
        return new_locator

    def __str__(self):
        return repr_dict(vars(self), replace_value_enum=True)

    def is_layered_locator(self):
        return False

class GuiGenericLocator(Locator):

    def __init__(self, ltype, lvalue=None):
        super().__init__(ltype, lvalue)

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
#     def __init__(self, ltype, lvalue):
#         super().__init__(ltype, lvalue)
    
#     def set_value(self, value):
#         self.lvalue = value    

#     def is_layered_locator(self):
#         return True
