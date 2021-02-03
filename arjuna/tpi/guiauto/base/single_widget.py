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

import abc
from arjuna.interact.gui.auto.base.dispatchable import _Dispatchable
from arjuna.tpi.guiauto.source.element import GuiElementSource
from arjuna.core.error import GuiWidgetTextNotSetError
from arjuna.tpi.tracker import track

@track("debug")
class SingleGuiWidget(_Dispatchable, metaclass=abc.ABCMeta):
    '''
        Abstract claas for a single GuiWidget in the Gui.

        Arguments:
            gui: Gui containing this GuiWidget.
            wmd: GuiWidgetMetaData of this GuiWidget.
    '''

    def __init__(self, gui, wmd): #, parent=None, find=True):
        self.__config = gui._automator.config
        self.__wmd = wmd
        _Dispatchable.__init__(self)
        self.__source = None
        from arjuna.interact.gui.auto.condition.element_conditions import GuiElementConditions, GuiElementLenientInteraction
        self.__conditions_handler = GuiElementConditions(self)
        self.__interaction_handler = GuiElementLenientInteraction(self)
        self.__source_parser = None

    @property
    def config(self):
        '''
            **Configuration** object associated with this GuiWidget.
        '''
        return self.__config

    def __get_attr_value_from_remote(self, attr, optional=False):
        return self.__return_attr_value(self.dispatcher.get_attr_value(attr, optional))

    def _get_html(self):
        return self.__get_attr_value_from_remote("outerHTML")

    def _load_source_parser(self):
        raw_source = self._get_html()
        self.__source_parser = GuiElementSource(raw_source)
        self.__source_parser._load()

    def _is_partial_element(self):
        return False

    def _get_instance_number(self):
        raise Exception("Instance number is applicable only for partial gui elements.")

    def _only_send_text(self, text):
        self.dispatcher.send_text(text)

    def _only_set_text(self, text):
        self._only_clear_text()
        self._only_send_text(text)
        entered_text = self.dispatcher.get_attr_value("value")
        if entered_text != text:
            raise GuiWidgetTextNotSetError("Expected text: {}. Actual text is {}".format(text, entered_text))

    def _only_click(self):
        # if self._should_scroll_to_view():
        #     self.dispatcher.scroll_to_view()
        self.dispatcher.click()

    def __return_attr_value(self, result):
        return result and result or None

    def scroll_full_height(self) -> None:
        '''
            Scroll full height of a GuiWidget. Applicable when it represents scrollable widgets in a Gui.
        '''
        self.dispatcher.scroll_full_height()

    def click(self):
        '''
            Click on this GuiWidget.

            Waits for clickability. Waits for click to succeed.

            **ArjunaOption.GUIAUTO_MAX_WAIT** in associated configuration is used as the default. Can be overriden using **max_wait** argument in GuiWidgetDefinition or GNS file.
        '''
        self.__wait_until_clickable_if_configured()
        self._interactions.Click().wait()
        #self._only_click()

    def __only_hover(self):
        self.dispatcher.hover()

    def hover(self):
        '''
            Mouse hover on this GuiWidget.

            Waits for clickability.

            **ArjunaOption.GUIAUTO_MAX_WAIT** in associated configuration is used as the default. Can be overriden using **max_wait** argument in GuiWidgetDefinition or GNS file.
        '''
        self.__wait_until_clickable_if_configured()
        self.__only_hover()

    def hover_and_click(self):
        '''
            Mouse hover and click on this GuiWidget.

            Waits for clickability.

            **ArjunaOption.GUIAUTO_MAX_WAIT** in associated configuration is used as the default. Can be overriden using **max_wait** argument in GuiWidgetDefinition or GNS file.
        '''
        self.__only_hover()
        self.__wait_until_clickable_if_configured()
        self.dispatcher.mouse_click()

    def double_click(self):
        '''
            Mouse double click.

            Waits for clickability.

            **ArjunaOption.GUIAUTO_MAX_WAIT** in associated configuration is used as the default. Can be overriden using **max_wait** argument in GuiWidgetDefinition or GNS file.
        '''
        self.__wait_until_clickable_if_configured()
        self.dispatcher.double_click()

    def __conditional_selected_state_click(self, condition_state):
        selected = self.is_selected()
        if selected == condition_state:
            self.__wait_until_clickable_if_configured()
            self._only_click()

    def select(self):
        '''
            Select this GuiWidget.

            Waits for clickability. Click happens only if it is currently deselected.

            **ArjunaOption.GUIAUTO_MAX_WAIT** in associated configuration is used as the default. Can be overriden using **max_wait** argument in GuiWidgetDefinition or GNS file.
        '''
        self.__conditional_selected_state_click(False)

    def deselect(self):
        '''
            De-select this GuiWidget.

            Waits for clickability. Click happens only if it is currently selected.

            **ArjunaOption.GUIAUTO_MAX_WAIT** in associated configuration is used as the default. Can be overriden using **max_wait** argument in GuiWidgetDefinition or GNS file.
        '''
        self.__conditional_selected_state_click(True)

    def wait_until_visible(self):
        '''
            Wait until visibility of this Gui Widget.

            **ArjunaOption.GUIAUTO_MAX_WAIT** in associated configuration is used as the default. Can be overriden using **max_wait** argument in GuiWidgetDefinition or GNS file.
        '''
        self._conditions.IsVisible().wait()

    def wait_until_clickable(self):
        '''
            Wait for clickability of this Gui Widget.

            **ArjunaOption.GUIAUTO_MAX_WAIT** in associated configuration is used as the default. Can be overriden using **max_wait** argument in GuiWidgetDefinition or GNS file.
        '''
        self._conditions.IsClickable().wait()

    def wait_until_selected(self):
        '''
            Wait for selected state of this Gui Widget.

            **ArjunaOption.GUIAUTO_MAX_WAIT** in associated configuration is used as the default. Can be overriden using **max_wait** argument in GuiWidgetDefinition or GNS file.
        '''
        self._conditions.IsSelected().wait()

    #################################
    ### State Checking
    #################################
    def is_selected(self):
        '''
            Check whether GuiWidget is selected. No dynamic waiting.
        '''
        return self.dispatcher.is_selected()

    def is_visible(self):
        '''
            Check whether GuiWidget is visible. No dynamic waiting.
        '''
        return self.dispatcher.is_visible()

    def is_clickable(self):
        '''
            Check whether GuiWidget is clickable. No dynamic waiting.
        '''
        return self.dispatcher.is_clickable()

    @property
    def _conditions(self):
        return self.__conditions_handler

    @property
    def _interactions(self):
        return self.__interaction_handler

    def __wait_until_clickable_if_configured(self):
        if self.__wmd.meta.settings.should_check_pre_state(): self.wait_until_clickable()

    # Properties
    @property
    def source(self) -> GuiElementSource:
        '''
           **GuiSource** object for this **GuiWidget**.
        '''
        return self.__source_parser

    @property
    def text(self):
        '''
           Text contained in this **GuiWidget**. It is a settable property.

           Note:
           
            You can set text of this GuiWidget (Clears and enters text.) using following Python code:
                .. code-block:: python

                    element.text = "<some_text>"

            Waits for clickability. Waits for text to be set as expected.

            **ArjunaOption.GUIAUTO_MAX_WAIT** in associated configuration is used as the default. Can be overriden using **max_wait** argument in GuiWidgetDefinition or GNS file.
        '''
        return self.source.content.text

    # Textbox abstraction
    @text.setter
    def text(self, text):
        self.__wait_until_clickable_if_configured()
        self._only_click()
        self._only_clear_text()
        self._interactions.SetText(text).wait()

    def clear_text(self):
        '''
           Clear text of this GuiWidget.
           
           Waits for clickability. 
        '''
        self.__wait_until_clickable_if_configured()
        self._only_click()
        self._only_clear_text()

    def send_text(self, text):
        '''
           Send text to this GuiWidget.

           Waits for clickability. **Click on GuiWidget is NOT executed before send keys operation**.

           **ArjunaOption.GUIAUTO_MAX_WAIT** in associated configuration is used as the default. Can be overriden using **max_wait** argument in GuiWidgetDefinition or GNS file.
        '''
        self.__wait_until_clickable_if_configured()
        self._only_enter_text(text)

    def send_keys(self, key_chord, wait_clickable=True):
        '''
           Send KeyChord to this GuiWidget.

           Waits for clickability. **Click on GuiWidget is NOT executed before send keys operation**.

           **ArjunaOption.GUIAUTO_MAX_WAIT** in associated configuration is used as the default. Can be overriden using **max_wait** argument in GuiWidgetDefinition or GNS file.
        '''
        keys = ""
        for key in key_chord._parts:
            keys = keys + key
        if wait_clickable:
            self.__wait_until_clickable_if_configured()
        self._only_enter_text(keys)

    def enter_text(self, text):
        '''
           Send text to this GuiWidget.

           Waits for clickability. **Click on GuiWidget is executed before send keys operation**.

           **ArjunaOption.GUIAUTO_MAX_WAIT** in associated configuration is used as the default. Can be overriden using **max_wait** argument in GuiWidgetDefinition or GNS file.
        '''
        self.__wait_until_clickable_if_configured()
        self._only_click()
        self._only_enter_text(text)

    def _only_clear_text(self):
        self.dispatcher.clear_text()

    def _only_enter_text(self, text):
        self._only_send_text(text)

    def _has_entered_text(self, text):
        pass

    def _has_entered_partial_text(self, text):
        pass

    # Checkbox abstraction
    def check(self):
        '''
            Check this GuiWidget.

            Waits for clickability. Click happens only if it is currently unchecked.

            **ArjunaOption.GUIAUTO_MAX_WAIT** in associated configuration is used as the default. Can be overriden using **max_wait** argument in GuiWidgetDefinition or GNS file.
        '''
        self.select()

    def uncheck(self):
        '''
            Uncheck this GuiWidget.

            Waits for clickability. Click happens only if it is currently checked.

            **ArjunaOption.GUIAUTO_MAX_WAIT** in associated configuration is used as the default. Can be overriden using **max_wait** argument in GuiWidgetDefinition or GNS file.
        '''
        self.deselect()

    def toggle(self):
        '''
            Toggle the selected/checked stage of a GuiWidget.

            Waits for clickability. Waits for click to succeed.

            **ArjunaOption.GUIAUTO_MAX_WAIT** in associated configuration is used as the default. Can be overriden using **max_wait** argument in GuiWidgetDefinition or GNS file.
        '''
        self.click()

    def is_checked(self):
        '''
            Check whether GuiWidget is checked. No dynamic waiting.
        '''
        return self.is_selected()

    def get_property(self, name):
        '''
            Get value of a property for this GuiWidget.
        '''
        return self.__get_attr_value_from_remote(name)

    def get_attr(self, name):
        '''
            Get value of an attribute for this GuiWidget.
        '''
        return self.__get_attr_value_from_remote(name)

    def _perform_action_chain(self, single_action_chain):
        from arjuna.interact.gui.auto.automator.actions import SingleActionChain
        action_chain = SingleActionChain(self.__automator, element=self)
        action_chain.perform(single_action_chain)
