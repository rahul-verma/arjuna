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

from arjuna.interact.gui.auto.element.guielement import GuiElement
from arjuna.interact.gui.auto.finder.emd import SimpleGuiElementMetaData
from arjuna.interact.gui.auto.base.configurable import Configurable

# UUID is for client reference. Agent does not know about this.
class GuiWebSelect(Configurable):

    def __init__(self, gui, emd, parent=None, option_container_lmd=None, option_lmd=None, iconfig=None):
        super().__init__(gui, iconfig)
        self.__gui = gui
        self.__automator = gui.automator
        self.__finder = parent and parent or gui.automator
        self._wrapped_main_element = self.automator.element(self.gui, emd)
        self.__found = False
        self.__options = None
        self.__option_lmd = option_lmd is not None and option_lmd or SimpleGuiElementMetaData("tag_name", "option")

        # It is seen in some websites like Bootstrap based that both select and options are children of a main div element.
        self.__option_container_same_as_select = option_container_lmd is None and True or False
        if not self.__option_container_same_as_select:
            self.__option_container = self.__finder.element_with_lmd(self.gui, option_container_lmd, iconfig=self.settings)
            # # Needs to be loaded so that options can be discovered.
            # self.__option_container.find_if_not_found()

        self.__source_parser = None

        self.__find()

    @property
    def gui(self):
        return self.__gui

    @property
    def automator(self):
        return self.__automator

    def __validate_select_control(self, tag):
        if tag.lower() != "select":
            raise Exception("The element should have a 'select' tag for WebSelect element. Found: " + tag)
        self._multi = self.__is_multi_select()

    def is_found(self):
        return self.__found

    def __find(self):

        def check_type_if_configured(tag):
            if self._should_check_type(): self.__validate_select_control(tag)

        def get_root_element():
            return self.__option_container_same_as_select and self._wrapped_main_element or self.__option_container

        def load_options():
            container = get_root_element()
            self.__options = container.multi_element_with_lmd(self.gui, self.__option_lmd, iconfig=self.settings)
            # self.__options.find_if_not_found()

        # self._wrapped_main_element.find()
        tag = self._wrapped_main_element.source.tag
        check_type_if_configured(tag)
        load_options()

    def __is_multi_select(self):
        source = self._wrapped_main_element.source
        return source.get_attr_value("multiple", optional=True) is True or source.get_attr_value("multi", optional=True) is True

    def is_multi_select(self):
        return self._multi

    def __set_option_locators(self, emd):
        self.__option_lmd = emd

    def has_index_selected(self, index):
        return self.__options[index].is_selected()

    def has_value_selected(self, value):
        return self.__options.get_instance_by_value(value).is_selected()

    def has_visible_text_selected(self, text):
        return self.__options.get_instance_by_visible_text(text).is_selected()

    def __select_option(self, option):
        self._wrapped_main_element.click()
        option.select()
        if self._should_check_post_state() and not option.is_selected():
            raise Exception("The attempt to select the dropdown option was not successful.")

    def select_index(self, index):
        option = self.__options[index]
        self.__select_option(option)

    def select_ordinal(self, ordinal):
        return self.select_by_index(ordinal-1)

    def select_text(self, text):
        option = self.__options.get_instance_by_visible_text(text)
        self.__select_option(option)

    @property
    def text(self):
        option = self.__options.get_first_selected_instance()
        return option.text

    @text.setter
    def text(self, text):
        # Dropdown element does not support clear text.
        self._wrapped_main_element.enter_text(text)

    def select_value(self, value):
        option = self.__options.get_instance_by_value(value)
        self.__select_option(option)

    @property
    def value(self):
        option = self.__options.get_first_selected_instance()
        return option.source.get_attr_value("value")

    # The following methods deal with multi-select and would be implemented later.

    def __validate_multi_select(self):
        if not self.is_multi_select():
            raise Exception("Deselect actions are allowed only for a multi-select dropdown.")

    def deselect_by_value(self, value):
        self.__validate_multi_select()
        return self.__options.get_instance_by_value(value).deselect()

    def deselect_by_index(self, index):
        pass

    def deselect_by_visible_text(self, text):
        pass

    def get_selected_options(self):
        pass

    def are_visible_texts_selected(self, text_list):
        pass

    def are_values_selected(self, text_list):
        pass

    def all_options(self):
        pass

    def select_by_values(self, value_list):
        pass

    def deselect_by_values(self, value_list):
        pass

    def select_by_indices(self, indices):
        pass

    def deselect_by_indices(self, indices):
        pass

    def select_by_visible_texts(self, text_list):
        pass

    def deselect_by_visible_texts(self, text_list):
        pass

    def get_source(self):
        self.__find_if_not_found()
        return self.__get_root_element().get_source()