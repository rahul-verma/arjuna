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

import random
import os

# Selenium construct. Needs to create wrapper exception and use in dispatcher.
from selenium.common.exceptions import StaleElementReferenceException


from arjuna.tpi.guiauto.base.locatable import Locatable
from arjuna.interact.gui.auto.base.dispatchable import _Dispatchable
from arjuna.tpi.guiauto.widget.element import GuiElement
from arjuna.tpi.engine.asserter import AsserterMixIn, IterableAsserterMixin
from arjuna.tpi.guiauto.source.multielement import GuiMultiElementSource
from arjuna.tpi.tracker import track

@track("debug")
class _GuiPartialElement(GuiElement):

    def __init__(self, gui, multi_element, index: int, dispatcher_element):
        super().__init__(gui, multi_element._wmd)
        self.__multi_element = multi_element
        self.__index = index
        self._dispatcher = dispatcher_element
        self._load_source_parser()

    def create_dispatcher(self):
        pass

    def _is_partial_element(self):
        return True

    @property
    def index(self):
        return self.__index

class GuiMultiElement(AsserterMixIn, IterableAsserterMixin, Locatable,_Dispatchable):
    '''
        Represents multiple GuiElements found using a same GuiWidgetDefinition.

        Not meant to be directly created. It is created using calls from **Gui** object or **GuiNamespace** object of **Gui**.

        Arguments:
            gui: **Gui** object containing this GuiMultiElement.
            wmd: GuiElementMetaData object.
            elements: (optional) List of GuiElements to populate this object instead of locating it.

        Note:
            It supports an index based retrieval of a contained GuiElement:

                .. code-block:: python

                    multielement[<index>]

            It also supports looping:

                .. code-block:: python

                    for element in multi_element:
                        some element code
    '''
    
    def __init__(self, gui, wmd, elements=None, dispatcher=None): #, parent=None):
        AsserterMixIn.__init__(self)
        IterableAsserterMixin.__init__(self)
        Locatable.__init__(self, gui, wmd) #, parent)
        _Dispatchable.__init__(self)
        # When a mulit-element is created using a filter.
        if dispatcher is not None:
            self._dispatcher = dispatcher
        if not elements:
            self.__elements = list()
        else:
            self.__elements = list()
            self._size = len(elements)

        self._container = self.__elements

        self._load_source_parser()

    def _configure_partial_elements(self, elem_config):
        '''
            This method is supposed to be called when multielement identification is completed.
            This is not used for usual multi-element.
            It is used by RadioGroup or DropDown etc which are higher level abstractions that use ME.
        '''
        for instance in self.__elements:
            instance.configure(elem_config)

    def _load_source_parser(self):
        self.__source_parser = GuiMultiElementSource(self.elements)

    def __getitem__(self, index):
        return self.__elements[index]

    @property
    def size(self) -> int:
        '''
            Number of GuiElements in this object.
        '''
        return len(self.__elements)

    @property
    def length(self) -> int:
        '''
            Number of GuiElements in this object.
        '''
        return len(self.__elements)

    def __len__(self) -> int:
        return self.size

    @size.setter
    def _size(self, count):
        # The logic ignores stale elements 
        for i in range(count):
            try:
                e = _GuiPartialElement(self.gui, self, i, self.dispatcher.get_element_at_index(i))
                self.__elements.append(e)
            except StaleElementReferenceException as e:
                pass

    @property
    def random_element(self) -> GuiElement:
        '''
            A GuiElement chosen at random from GuiElments in this GuiMultiElement.
        '''
        return self[random.randint(0, self.size-1)]

    @property
    def first_element(self) -> GuiElement:
        '''
            First GuiElement in this GuiMultiElement.
        '''
        return self[0]

    @property
    def last_element(self) -> GuiElement:
        '''
            Last GuiElement in this GuiMultiElement.
        '''
        return self[len(self)-1]

    def get_element_at_ordinal(self, ordinal: int) -> GuiElement:
        '''
            Get GuiElement at an ordinal (position) in this GuiMultiElement.

            Ordinals are as per human counting. First element is at ordinal 1.
        '''
        return self.__elements[ordinal-1]

    def get_element_by_visible_text(self, text: str) -> GuiElement:
        '''
            Get GuiElement in this GuiMultiElement whose text is as supplied.

            Args:
                text: Text of this target GuiElement.
        '''
        texts = self.__get_all_texts()
        first_index = self.__find_first_text_index(texts, text)
        return self[first_index]

    def get_element_by_value(self, value: str) -> GuiElement:
        '''
            Get GuiElement in this GuiMultiElement whose value attribute content is as supplied.

            Args:
                value: Value attribute content of this target GuiElement.
        '''
        values = self.__get_all_values()
        first_index = self.__find_first_value_index(values, value)
        return self[first_index]

    def __return_attr_values(self, response):
        if "data" in response and "attrValues" in response["data"]:
            return response["data"]["attrValues"]
        else:
            return None

    def are_selected(self) -> bool:
        '''
            Check if all GuiElements in this GuiMultiElement are in selected state.
        '''
        return [instance.is_selected() for instance in self.__elements]

    # getting index attribute when it does not exist returns value attribute.
    # So, not going the Selenium way. Setu would treat index as computer counting.
    def has_index_selected(self, index: int) -> GuiElement:
        '''
            Check if GuiElement at the given index is in selected state.
        '''
        return self[index].is_selected()

    # Ordinal is human counting
    def has_ordinal_selected(self, ordinal):
        '''
            Check if GuiElement at the given ordinal is in selected state.
            
            Ordinals are as per human counting. First element is at ordinal 1.
        '''
        return self.has_index_selected(ordinal-1)

    def __find_first_match_index(self, in_sequence, to_match):
        try:
            return in_sequence.index(to_match)
        except:
            return -1

    def __get_all_texts(self):
        self._load_source_parser()
        texts = self.__source_parser.texts
        return texts

    def __find_first_text_index(self, texts, text):
        first_index = texts.index(text)
        if first_index == -1:
            raise Exception("No option with {} visible text present in drop down.".format(text))
        return first_index

    def __get_all_values(self):
        self._load_source_parser()
        values = self.__source_parser.values
        return values

    def __find_first_value_index(self, values, value):
        first_index = values.index(value)
        if first_index == -1:
            raise Exception("No option with {} value present in drop down.".format(value))
        return first_index

    @property
    def first_selected_element(self) -> GuiElement:
        '''
            First GuiElement which is in selected state.
        '''
        self._load_source_parser()
        booleans = self.are_selected()
        first_index = None
        try:
            first_index = booleans.index(True)
        except:
            raise Exception("No option in drop down is currenlty selected.")
        else:
            return self[first_index]

    @property
    def source(self) -> GuiMultiElementSource:
        '''
            **GuiSource** for this GuiMultiElement.
        '''
        return self.__source_parser

    @property
    def elements(self):
        '''
            List of GuiElements in this GuiMultiElement
        '''
        return self.__elements

    @property
    def filter(self):
        '''
            GuiMultiElementFilter object for this GuiMultiElement
        '''
        return GuiMultiElementFilter(self)


class GuiMultiElementFilter:
    '''
        Build a new GuiMultiElement by filtering an existing one.

        Arguments:
            gui_multi_element: Existing **GuiMultiElement** object.
    '''

    def __init__(self, gui_multi_element):
        self.__source_gui_multielement = gui_multi_element
        self.__gui = gui_multi_element.gui
        self.__wmd = gui_multi_element._wmd
        self.__elements = gui_multi_element.elements
        self.__filtered_elements = self.__elements

    def build(self) -> GuiMultiElement:
        '''
            Build a new `GuiMultiElement`.
        '''
        me = GuiMultiElement(self.__gui, self.__wmd, elements=self.__filtered_elements, dispatcher=self.__source_gui_multielement.dispatcher)
        self.__filtered_elements = self.__elements
        return me

    def active(self) -> 'self':
        '''
            Choose only active/non-stale `GuiElement` s. 

            Returns:
                Current `GuiMultiElementFilter` object
        '''
        out = list()
        for e in self.__filtered_elements:
            try:
                e._get_html()
                out.append(e)
            except StaleElementReferenceException as e:
                pass
        self.__filtered_elements = out
        return self

    def visible(self) -> 'self':
        '''
            Choose only visible `GuiElement` objects. 

            Returns:
                Current `GuiMultiElementFilter` object
        '''
        self.__filtered_elements = [
            e for e in self.__filtered_elements
            if e.is_visible()
        ]
        return self

    def attr(self, name) -> 'self':
        '''
            Choose only `GuiElement` objects which contain the given attribute.

            Arguments:
                name: Name of attribute

            Returns:
                Current `GuiMultiElementFilter` object
        '''
        self.__filtered_elements = [
            e for e in self.__filtered_elements
            if e.source.is_attr_present(name)
        ]
        return self        

    def attr_value(self, name, value) -> 'self':
        '''
            Choose only `GuiElement` objects which contain the given attribute and its value.

            Arguments:
                name: Name of attribute
                value: Full or partial content of the given attribute

            Returns:
                Current `GuiMultiElementFilter` object
        '''
        self.__filtered_elements = [
            e for e in self.__filtered_elements
            if value in e.source.get_attr_value(name)
        ]
        return self

    def value(self, value) -> 'self':
        '''
            Choose only `GuiElement` objects whose value attribute matches the value argument provided.

            Arguments:
                value: Full or partial content of value attribute.

            Returns:
                Current `GuiMultiElementFilter` object
        '''
        self.__filtered_elements = [
            e for e in self.__filtered_elements
            if str(value) in e.source.get_value("value")
        ]
        return self

    def text(self, text) -> 'self':
        '''
            Choose only `GuiElement` objects whose text contains the text provided.

            Arguments:
                text: Full or partial text.

            Returns:
                Current `GuiMultiElementFilter` object
        '''
        self.__filtered_elements = [
            e for e in self.__filtered_elements
            if text in e.text
        ]
        return self     

    