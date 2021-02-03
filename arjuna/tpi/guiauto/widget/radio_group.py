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

from arjuna.tpi.guiauto.source.multielement import GuiMultiElementSource
from arjuna.tpi.tracker import track

@track("debug")
class GuiRadioGroup:
    '''
        Represents a radio group in th Gui.

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
        self.__radios = None
        self.__find(self.__finder, wmd)

    @property
    def gui(self) -> 'Gui':
        '''
            **Gui** object containing this GuiDropDown.
        '''
        return self.__gui

    def __validate_radio_buttons(self, source):
        if [t for t in source.tag_names if t.strip().lower() != 'input']:
            raise Exception("Not a valid radio group. Contains non-input elements.")
        if [t for t in source.get_attr_values("type") if t.strip().lower() != 'radio']:
            raise Exception("Not a valid radio group. Contains non-radio elements.")
        names = source.get_attr_values("name")
        if len(set(names)) != 1:
            raise Exception("Not a valid radio group. Contains radio elements belonging to different radio groups.")

    def __check_type_if_configured(self, tags):
        if self.__wmd.meta.settings.should_check_type(): self.__validate_radio_buttons(tags)

    def __find(self, finder, wmd):
        # This would force the identification of partial elements in the wrapped multi-element.
        self.__radios = finder._wmd_finder.multi_element(wmd)
        self.__check_type_if_configured(self.source)

    def has_index_selected(self, index: int) -> bool:
        '''
            Check if this GuiRadioGroup has radio button selected at given index .

            Args:
                index: Target index.
        '''
        return self.__radios[index].is_selected()

    def has_value_selected(self, value: str) -> bool:
        '''
            Check if this GruiRadioGroup has radio button with given value attribute content selected.

            Args:
                value: Exact content of value attribute.
        '''
        return self.__radios.get_element_by_value(value).is_selected()

    @property
    def value(self) -> str:
        '''
            Content of value attribute of selected radio button.
        '''
        instance = self.__radios.first_selected_element
        return instance.source.get_attr_value("value")

    def __select_option(self, option):
        option.select()
        if self.__wmd.meta.settings.should_check_post_state() and not option.is_selected():
            raise Exception("The attempt to select the radio button was not successful.")

    def select_index(self, index: int) -> None:
        '''
            Select radio button at given index.

            Args:
                index: Target index.
        '''
        option = self.__radios[index]
        self.__select_option(option)

    def select_ordinal(self, ordinal: int) -> None:
        '''
            Select radio group at given ordinal.

            Ordinals are as per human counting. First element is at ordinal 1.

            Args:
                ordinal: Target ordinal.
        '''
        return self.select_by_index(ordinal-1)

    def select_value(self, value: str) -> None:
        '''
            Select radio button with given content of value attribute.

            Args:
                value: Exact content of value attribute.
        '''
        option = self.__radios.get_element_by_value(value)
        self.__select_option(option)

    @property
    def source(self) -> GuiMultiElementSource:
        '''
            **GuiMultiElementSource** for this GuiRadioGroup (source of associated GuiMultiElement)
        '''
        return self.__radios.source