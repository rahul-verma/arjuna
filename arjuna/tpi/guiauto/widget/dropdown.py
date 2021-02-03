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

from arjuna.interact.gui.auto.finder.wmd import SimpleGuiWidgetMetaData
from arjuna.tpi.guiauto.meta.locator import GuiWidgetDefinition

from arjuna.tpi.guiauto.source.element import GuiElementSource
from arjuna.tpi.tracker import track

@track("debug")
class GuiDropDown:
    '''
        Represents a drop down list in th Gui.

        Not meant to be directly created. It is created using calls from **Gui** object or **GuiNamespace** object of **Gui**.

        Arguments:
            gui: **Gui** object containing this GuiDropDown.
            wmd: **GuiElementMetaData** object for this GuiDropDown.

        Keyword Arguments:
            parent: **GuiElement** in case it is found inside a **GuiElement**. Default is the **Gui** object.
    '''

    def __init__(self, gui, wmd, parent=None):
        self.__gui = gui
        self.__wmd = wmd
        self.__automator = gui._automator
        self.__finder = parent and parent or gui
        self._wrapped_main_element = self.__finder._wmd_finder.element(wmd)
        self.__found = False
        self.__options = None
        self.__option_locator = self._wmd.meta.option_locator is not None and self._wmd.meta.option_locator or GuiWidgetDefinition(type="multi_element", tags="option")

        # It is seen in some websites like Bootstrap based that both select and options are children of a main div element.
        self.__option_container_same_as_select = self._wmd.meta.option_container_locator is None and True or False
        if not self.__option_container_same_as_select:
            self.__option_container = self.__finder.element(self._wmd.meta.option_container_locator)

        self.__source_parser = None

        self.__find()

    @property
    def _wmd(self):
        return self.__wmd

    @property
    def gui(self) -> 'Gui':
        '''
            **Gui** object containing this GuiDropDown.
        '''
        return self.__gui
        
    def __validate_select_control(self, tag):
        if tag.lower() != "select":
            raise Exception("The element should have a 'select' tag for WebSelect element. Found: " + tag)
        self._multi = self.__is_multi_select()

    def __find(self):

        def check_type_if_configured(tag):
            if self.__wmd.meta.settings.should_check_type(): self.__validate_select_control(tag)

        def get_root_element():
            return self.__option_container_same_as_select and self._wrapped_main_element or self.__option_container

        def load_options():
            container = get_root_element()
            self.__options = container.locate(self.__option_locator)

        # self._wrapped_main_element.find()
        tag = self._wrapped_main_element.source.tag
        check_type_if_configured(tag)
        load_options()

    def __is_multi_select(self):
        source = self._wrapped_main_element.source
        return source.get_attr_value("multiple", optional=True) is True or source.get_attr_value("multi", optional=True) is True

    def is_multi_select(self) -> bool:
        '''
            Check if this GuiDropDown allows multiple selection of options.
        '''
        return self._multi

    def has_index_selected(self, index: int) -> bool:
        '''
            Check if this GuiDropDown has option selected at given index.

            Args:
                index: Target index.
        '''
        return self.__options[index].is_selected()

    def has_value_selected(self, value: str) -> bool:
        '''
            Check if this GuiDropDown has option with given value attribute content selected.

            Args:
                value: Exact content of value attribute.
        '''
        return self.__options.get_element_by_value(value).is_selected()

    def has_visible_text_selected(self, text: str) -> bool:
        '''
            Check if this GuiDropDown has option with visible text selected.

            Args:
                text: Exact visible text content.
        '''
        return self.__options.get_element_by_visible_text(text).is_selected()

    def __select_option(self, option):
        self._wrapped_main_element.click()
        option.select()
        if self.__wmd.meta.settings.should_check_post_state() and not option.is_selected():
            raise Exception("The attempt to select the dropdown option was not successful.")

    def select_index(self, index: int) -> None:
        '''
            Select option at given index.

            Args:
                index: Target index.
        '''
        option = self.__options[index]
        self.__select_option(option)

    def select_ordinal(self, ordinal: int) -> None:
        '''
            Select option at given ordinal.

            Ordinals are as per human counting. First element is at ordinal 1.

            Args:
                ordinal: Target ordinal.
        '''
        return self.select_by_index(ordinal-1)

    def select_text(self, text: str) -> None:
        '''
            Select option with given visible text.

            Args:
                text: Exact visible text content.
        '''
        option = self.__options.get_element_by_visible_text(text)
        self.__select_option(option)

    @property
    def text(self) -> str:
        '''
            Visible text of selected option

           Note:
           
            You can select an option with visible text of this GuiDropDown too using following Python code:
                .. code-block:: python

                    dropdown.text = "<some_text>"

            **Method used for this diffent from **select_text****. It uses **send_keys** to simulate this interaction instead of clicking an option.
            
            Waits for clickability.

            **ArjunaOption.GUIAUTO_MAX_WAIT** in associated configuration is used as the default. Can be overriden using **max_wait** argument in GuiWidgetDefinition or GNS file.
        '''
        option = self.__options.first_selected_element
        return option.text

    @text.setter
    def text(self, text):
        # Dropdown element does not support clear text.
        self._wrapped_main_element.enter_text(text)

    def select_value(self, value: str) -> None:
        '''
            Select option with given content of value attribute.

            Args:
                value: Exact content of value attribute.
        '''
        option = self.__options.get_element_by_value(value)
        self.__select_option(option)

    @property
    def value(self) -> str:
        '''
            Content of value attribute of selected option
        '''
        option = self.__options.first_selected_element
        return option.source.get_attr_value("value")

    @property
    def source(self) -> GuiElementSource:
        '''
            **GuiSource** for this GuiDropDown (source of root element).
        '''
        return self._wrapped_main_element.source

    def __validate_multi_select(self):
        if not self.is_multi_select():
            raise Exception("Deselect actions are allowed only for a multi-select dropdown.")

    def _deselect_by_value(self, value):
        self.__validate_multi_select()
        return self.__options.get_element_by_value(value).deselect()

    def _deselect_by_index(self, index):
        pass

    def _deselect_by_visible_text(self, text):
        pass

    def _get_selected_options(self):
        pass

    def _are_visible_texts_selected(self, text_list):
        pass

    def _are_values_selected(self, text_list):
        pass

    def _all_options(self):
        pass

    def _select_by_values(self, value_list):
        pass

    def _deselect_by_values(self, value_list):
        pass

    def _select_by_indices(self, indices):
        pass

    def _deselect_by_indices(self, indices):
        pass

    def _select_by_visible_texts(self, text_list):
        pass

    def _deselect_by_visible_texts(self, text_list):
        pass