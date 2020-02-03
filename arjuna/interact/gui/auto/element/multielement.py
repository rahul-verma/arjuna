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

import random
import os

# Selenium construct. Needs to create wrapper exception and use in dispatcher.
from selenium.common.exceptions import StaleElementReferenceException


from arjuna.interact.gui.auto.base.locatable import Locatable
from arjuna.interact.gui.auto.base.dispatchable import Dispatchable
from arjuna.interact.gui.auto.base.configurable import Configurable
from arjuna.interact.gui.auto.element.guielement import GuiElement
from arjuna.interact.gui.auto.source.parser import *

class _GuiPartialElement(GuiElement):

    def __init__(self, gui, multi_element, index: int, dispatcher_element, iconfig=None):
        super().__init__(gui, multi_element.lmd, iconfig=iconfig)
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

class GuiMultiElement(Locatable,Dispatchable,Configurable):
    
    def __init__(self, gui, lmd, iconfig=None, elements=None): #, parent=None):
        Locatable.__init__(self, gui, lmd) #, parent)
        Dispatchable.__init__(self)
        Configurable.__init__(self, gui, iconfig)
        if elements:
            self.__elements = elements
        else:
            self.__elements = list()   
        self.__source_parser = None

    # def configure_partial_elements(self, elem_config):
    #     '''
    #         This method is supposed to be called when multielement identification is completed.
    #         This is not used for usual multi-element.
    #         It is used by RadioGroup or DropDown etc which are higher level abstractions that use ME.
    #     '''
    #     for instance in self.__elements:
    #         instance.configure(elem_config)

    # def find(self):
    #     self.parent_container.find_multielement(self)
    #     self.__load_source_parser()

    # #Override
    # def find_if_not_found(self):
    #     if not self.is_found():
    #         self.find()

    def load_source_parser(self):
        self.__source_parser = MultiElementSource()
        self.__source_parser.load(self.__elements)

    def __getitem__(self, index):
        # self.find_if_not_found()
        return self.__elements[index]

    @property
    def size(self):
        # self.find_if_not_found()
        return len(self.__elements)

    @size.setter
    def size(self, count):
        # The logic ignores stale elements 
        for i in range(count):
            try:
                e = _GuiPartialElement(self.gui, self, i, self.dispatcher.get_element_at_index(i), iconfig=self.settings)
                self.__elements.append(e)
            except StaleElementReferenceException as e:
                pass

    length = size

    @property
    def random_element(self):
        # self.find_if_not_found()
        return self[random.randint(0, self.size-1)]

    @property
    def first_element(self):
        return self[0]

    @property
    def last_element(self):
        return self[self.length-1]

    def get_element_at_ordinal(self, ordinal):
        # self.find_if_not_found()
        return self.__elements[ordinal-1]

    def get_instance_by_visible_text(self, text):
        texts = self.__get_all_texts()
        first_index = self.__find_first_text_index(texts, text)
        return self[first_index]

    def get_instance_by_value(self, value):
        values = self.__get_all_values()
        first_index = self.__find_first_value_index(values, value)
        return self[first_index]

    def wait_until_visible(self):
        self.find_if_not_found()
        # Should the logic be keptin Setu itself for this????

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
        # self.find_if_not_found()
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
        # self.find_if_not_found()
        self.load_source_parser()
        texts = self.__source_parser.get_text_contents()
        return texts

    def __find_first_text_index(self, texts, text):
        first_index = texts.index(text)
        if first_index == -1:
            raise Exception("No option with {} visible text present in drop down.".format(text))
        return first_index

    def __get_all_values(self):
        # self.find_if_not_found()
        self.load_source_parser()
        values = self.__source_parser.get_values()
        return values

    def __find_first_value_index(self, values, value):
        first_index = values.index(value)
        if first_index == -1:
            raise Exception("No option with {} value present in drop down.".format(value))
        return first_index

    def get_first_selected_instance(self):
        # self.find_if_not_found()
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
        self.__lmd = gui_multi_element.lmd
        self.__iconfig = gui_multi_element.settings
        self.__elements = gui_multi_element.elements
        self.__filtered_elements = self.__elements

    def build(self):
        me = GuiMultiElement(self.__gui, self.__lmd, iconfig=self.__iconfig, elements=self.__filtered_elements)
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

    