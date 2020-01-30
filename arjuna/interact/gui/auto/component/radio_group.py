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

from arjuna.interact.gui.auto.base.configurable import Configurable

class GuiWebRadioGroup(Configurable):

    def __init__(self, gui, lmd, parent=None):
        super().__init__(gui)
        self.__gui = gui
        self.__automator = gui.automator
        self.__finder = parent and parent or self.automator
        self.__radios = None
        self.__find(self.__finder, lmd)

    @property
    def gui(self):
        return self.__gui

    @property
    def automator(self):
        return self.__automator

    def __validate_radio_buttons(self, source):
        if [t for t in source.get_tag_names() if t.strip().lower() != 'input']:
            raise Exception("Not a valid radio group. Contains non-input elements.")
        if [t for t in source.get_attr_values("type") if t.strip().lower() != 'radio']:
            raise Exception("Not a valid radio group. Contains non-radio elements.")
        names = source.get_attr_values("name")
        if len(set(names)) != 1:
            raise Exception("Not a valid radio group. Contains radio elements belonging to different radio groups.")

    def __check_type_if_configured(self, tags):
        if self._should_check_type(): self.__validate_radio_buttons(tags)

    def __find(self, finder, lmd):
        # This would force the identification of partial elements in the wrapped multi-element.
        self.__radios = finder.multi_element(self.gui, lmd)
        self.__check_type_if_configured(self.source)
        self.__radios.configure_partial_elements(self.settings)

    def has_index_selected(self, index):
        return self.__radios[index].is_selected()

    def has_value_selected(self, value):
        return self.__radios.get_instance_by_value(value).is_selected()

    @property
    def value(self):
        instance = self.__radios.get_first_selected_instance()
        return instance.source.get_attr_value("value")

    def __select_option(self, option):
        option.select()
        if self._should_check_post_state() and not option.is_selected():
            raise Exception("The attempt to select the radio button was not successful.")

    def select_index(self, index):
        option = self.__radios[index]
        self.__select_option(option)

    def select_ordinal(self, ordinal):
        return self.select_by_index(ordinal-1)

    def select_value(self, value):
        option = self.__radios.get_instance_by_value(value)
        self.__select_option(option)

    @property
    def source(self):
        return self.__radios.source