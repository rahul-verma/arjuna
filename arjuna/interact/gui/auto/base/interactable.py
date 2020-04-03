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

from arjuna.interact.gui.auto.base.dispatchable import Dispatchable
from arjuna.tpi.guiauto.source import ElementXMLSourceParser
from arjuna.tpi.exceptions import GuiElementTextNotSetError

class Interactable(Dispatchable):

    def __init__(self, gui, emd): #, parent=None, find=True):
        self.__config = gui.automator.config
        self.__emd = emd
        Dispatchable.__init__(self)
        self.__source = None

        #self.__automator = automator
        from arjuna.interact.gui.auto.condition.element_conditions import GuiElementConditions, GuiElementLenientInteraction
        self.__conditions_handler = GuiElementConditions(self)
        self.__interaction_handler = GuiElementLenientInteraction(self)
        self.__source_parser = None

        # # For partial element find is False
        # if find:
        #     self.find()

    @property
    def config(self):
        return self.__config

    def __get_attr_value_from_remote(self, attr, optional=False):
        return self.__return_attr_value(self.dispatcher.get_attr_value(attr, optional))

    def get_html(self):
        return self.__get_attr_value_from_remote("outerHTML")

    def load_source_parser(self):
        raw_source = self.get_html()
        self.__source_parser = ElementXMLSourceParser(raw_source)
        self.__source_parser.load()

    # def find(self):
    #     self.parent_container.find_element(self)
    #     self.load_source_parser()

    # def find_without_wait(self):
    #     self.parent_container.find_element_without_wait(self)

    # identify = find
    # reset = find

    def _is_partial_element(self):
        return False

    def _get_instance_number(self):
        raise Exception("Instance number is applicable only for partial gui elements.")

    # def _kwargs(self, **kwargs):
    #     return self.__append_instance_number(kwargs)

    # def _noargs(self):
    #     return self.__append_instance_number({})

    def _only_send_text(self, text):
        self.dispatcher.send_text(text)

    def _only_set_text(self, text):
        self._only_clear_text()
        self._only_send_text(text)
        entered_text = self.dispatcher.get_attr_value("value")
        if entered_text != text:
            raise GuiElementTextNotSetError("Expected text: {}. Actual text is {}".format(text, entered_text))

    def _only_click(self):
        # if self._should_scroll_to_view():
        #     self.dispatcher.scroll_to_view()
        self.dispatcher.click()

    def __return_attr_value(self, result):
        return result and result or None

    def scroll_full_height(self):
        self.dispatcher.scroll_full_height()

    def click(self):
        self.__wait_until_clickable_if_configured()
        self.interactions.Click().wait()
        #self._only_click()

    def __only_hover(self):
        self.dispatcher.hover()

    def hover(self):
        self.__wait_until_clickable_if_configured()
        self.__only_hover()

    def hover_and_click(self):
        self.__only_hover()
        self.__wait_until_clickable_if_configured()
        self.dispatcher.mouse_click()

    def __conditional_selected_state_click(self, condition_state):
        selected = self.is_selected()
        if selected == condition_state:
            self.__wait_until_clickable_if_configured()
            self._only_click()

    def select(self):
        self.__conditional_selected_state_click(False)

    def deselect(self):
        self.__conditional_selected_state_click(True)

    # def reload(self):
    #     pass

    # wait_until_present = reload

    def wait_until_visible(self):
        self.conditions.IsVisible().wait()

    def wait_until_clickable(self):
        self.conditions.IsClickable().wait()

    def wait_until_selected(self):
        self.conditions.IsSelected().wait()

    #################################
    ### State Checking
    #################################
    def is_selected(self):
        return self.dispatcher.is_selected()

    def is_visible(self):
        return self.dispatcher.is_visible()

    def is_clickable(self):
        return self.dispatcher.is_clickable()

    @property
    def conditions(self):
        return self.__conditions_handler

    @property
    def interactions(self):
        return self.__interaction_handler

    def __wait_until_clickable_if_configured(self):
        if self.__emd.meta.settings.should_check_pre_state(): self.wait_until_clickable()

    # Properties
    @property
    def source(self): # OLD: refind=True, reload=True
        return self.__source_parser

    @property
    def text(self):
        return self.source.content.text

    # Textbox abstraction
    @text.setter
    def text(self, text):
        self.__wait_until_clickable_if_configured()
        self._only_click()
        self._only_clear_text()
        self.interactions.SetText(text).wait()

    def clear_text(self):
        self.__wait_until_clickable_if_configured()
        self._only_click()
        self._only_clear_text()

    def send_text(self, text):
        self.__wait_until_clickable_if_configured()
        self._only_enter_text(text)

    def enter_text(self, text):
        self.__wait_until_clickable_if_configured()
        self._only_click()
        self._only_enter_text(text)

    def _only_clear_text(self):
        self.dispatcher.clear_text()

    def _only_enter_text(self, text):
        self._only_send_text(text)

    def has_entered_text(self, text):
        pass

    def has_entered_partial_text(self, text):
        pass

    # Checkbox abstraction
    def check(self):
        self.select()

    def uncheck(self):
        self.deselect()

    def toggle_checkbox(self):
        self.click()

    def is_checked(self):
        return self.is_selected()

    def get_property_value(self, attr):
        return self.__get_attr_value_from_remote(attr)

    def perform_action_chain(self, single_action_chain):
        from arjuna.interact.gui.auto.automator.actions import SingleActionChain
        action_chain = SingleActionChain(self.__automator, element=self)
        action_chain.perform(single_action_chain)
