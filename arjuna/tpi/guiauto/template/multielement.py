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

import random
import os

# Selenium construct. Needs to create wrapper exception and use in dispatcher.
from selenium.common.exceptions import StaleElementReferenceException


from arjuna.interact.gui.auto.base.locatable import Locatable
from arjuna.interact.gui.auto.base.dispatchable import Dispatchable
from arjuna.tpi.guiauto.element import GuiElement
from arjuna.tpi.guiauto.source import *
from arjuna.tpi.engine.asserter import AsserterMixIn

class GuiPartialElement(GuiElement):

    def __init__(self, gui, multi_element, index: int, dispatcher_element):
        super().__init__(gui, multi_element.emd)
        self.__multi_element = multi_element
        self.__index = index
        self.dispatcher = dispatcher_element
        self.load_source_parser()

    def create_dispatcher(self):
        pass

    def _is_partial_element(self):
        return True

    @property
    def index(self):
        return self.__index

class GuiMultiElement(AsserterMixIn, Locatable,Dispatchable):
    
    def __init__(self, gui, emd, elements=None): #, parent=None):
        AsserterMixIn.__init__(self)
        Locatable.__init__(self, gui, emd) #, parent)
        Dispatchable.__init__(self)
        if elements:
            self.__elements = elements
        else:
            self.__elements = list()   
        self.load_source_parser()

    def configure_partial_elements(self, elem_config):
        '''
            This method is supposed to be called when multielement identification is completed.
            This is not used for usual multi-element.
            It is used by RadioGroup or DropDown etc which are higher level abstractions that use ME.
        '''
        for instance in self.__elements:
            instance.configure(elem_config)

    def load_source_parser(self):
        self.__source_parser = MultiElementSource(self.elements)

    def __getitem__(self, index):
        return self.__elements[index]

    @property
    def size(self):
        return len(self.__elements)

    length = size

    def __len__(self):
        return self.size

    def assert_size(self, size, obj_name, msg=None):
        self.asserter.assert_equal(self.size, size, msg="{} should have exactly {} elements, but was found to have {} elements.".format(obj_name, size, self.size, self.asserter.format_msg(msg)))

    def assert_min_size(self, size, obj_name, msg=None):
        self.asserter.assert_min(self.size, size, msg="{} should have minimum of {} elements, but was found to have {} elements.".format(obj_name, size, self.size, self.asserter.format_msg(msg)))
    
    def assert_max_size(self, size, obj_name, msg=None):
        self.asserter.assert_max(self.size, size, msg="{} should have maximum of {} elements, but was found to have {} elements.".format(obj_name, size, self.size, self.asserter.format_msg(msg)))

    def assert_empty(self, obj_name, msg=None):
        self.asserter.assert_equal(self.size, 0, msg="{} should be empty, but was found to have {} elements.".format(obj_name, self.size, self.asserter.format_msg(msg)))

    def assert_not_empty(self, obj_name, msg=None):
        self.asserter.assert_greater(self.size, 0, msg="{} is expected to have atleat 1 element, but was found to be empty.{}".format(obj_name, self.size, self.asserter.format_msg(msg)))

    @size.setter
    def size(self, count):
        # The logic ignores stale elements 
        for i in range(count):
            try:
                e = GuiPartialElement(self.gui, self, i, self.dispatcher.get_element_at_index(i))
                self.__elements.append(e)
            except StaleElementReferenceException as e:
                pass

    @property
    def random_element(self):
        return self[random.randint(0, self.size-1)]

    @property
    def first_element(self):
        return self[0]

    @property
    def last_element(self):
        return self[len(self)-1]

    def get_element_at_ordinal(self, ordinal):
        return self.__elements[ordinal-1]

    def get_element_by_visible_text(self, text):
        texts = self.__get_all_texts()
        first_index = self.__find_first_text_index(texts, text)
        return self[first_index]

    def get_element_by_value(self, value):
        values = self.__get_all_values()
        first_index = self.__find_first_value_index(values, value)
        return self[first_index]

    def __return_attr_values(self, response):
        if "data" in response and "attrValues" in response["data"]:
            return response["data"]["attrValues"]
        else:
            return None

    def are_selected(self):
        return [instance.is_selected() for instance in self.__elements]

    # getting index attribute when it does not exist retursn value attribute.
    # So, not going the Selenium way. Setu would treat index as computer counting.
    def has_index_selected(self, index):
        return self[index].is_selected()

    # Ordinal is human counting
    def has_ordinal_selected(self, ordinal):
        return self.has_index_selected(ordinal-1)

    def __find_first_match_index(self, in_sequence, to_match):
        try:
            return in_sequence.index(to_match)
        except:
            return -1

    def __get_all_texts(self):
        self.load_source_parser()
        texts = self.__source_parser.get_text_contents()
        return texts

    def __find_first_text_index(self, texts, text):
        first_index = texts.index(text)
        if first_index == -1:
            raise Exception("No option with {} visible text present in drop down.".format(text))
        return first_index

    def __get_all_values(self):
        self.load_source_parser()
        values = self.__source_parser.get_values()
        return values

    def __find_first_value_index(self, values, value):
        first_index = values.index(value)
        if first_index == -1:
            raise Exception("No option with {} value present in drop down.".format(value))
        return first_index

    def get_first_selected_instance(self):
        self.load_source_parser()
        booleans = self.are_selected()
        first_index = None
        try:
            first_index = booleans.index(True)
        except:
            raise Exception("No option in drop down is currenlty selected.")
        else:
            return self[first_index]

    @property
    def source(self):
        return self.__source_parser

    @property
    def elements(self):
        return self.__elements

    @property
    def filter(self):
        return ElementFilter(self)


class ElementFilter:

    def __init__(self, gui_multi_element):
        self.__gui = gui_multi_element.gui
        self.__emd = gui_multi_element.emd
        self.__elements = gui_multi_element.elements
        self.__filtered_elements = self.__elements

    def build(self):
        me = GuiMultiElement(self.__gui, self.__emd, elements=self.__filtered_elements)
        self.__filtered_elements = self.__elements
        return me

    def active(self):
        out = list()
        for e in self.__filtered_elements:
            try:
                e.get_html()
                out.append(e)
            except StaleElementReferenceException as e:
                pass
        self.__filtered_elements = out
        return self

    def visible(self):
        self.__filtered_elements = [
            e for e in self.__filtered_elements
            if e.is_visible()
        ]
        return self

    def attr(self, name):
        self.__filtered_elements = [
            e for e in self.__filtered_elements
            if e.source.is_attr_present(name)
        ]
        return self        

    def attr_value(self, name, value):
        self.__filtered_elements = [
            e for e in self.__filtered_elements
            if e.source.get_attr_value(name) == value
        ]
        return self

    def value(self, value):
        self.__filtered_elements = [
            e for e in self.__filtered_elements
            if e.source.get_value("value") == str(value)
        ]
        return self

    def text_content(self, text):
        self.__filtered_elements = [
            e for e in self.__filtered_elements
            if text in e.text
        ]
        return self     

    