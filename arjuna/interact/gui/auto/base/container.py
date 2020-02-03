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

import abc

from arjuna.interact.gui.auto.finder.element_finder import ElementFinder

class ElementContainer(metaclass=abc.ABCMeta):

    def __init__(self, config):
        self.__config = config
        from arjuna.interact.gui.auto.condition.container_conditions import GuiElementContainerConditions
        self.__element_finder = ElementFinder(self)
        self.__container_conditions = GuiElementContainerConditions(self)

    @property
    def config(self):
        return self.__config

    @property
    def element_finder(self):
        return self.__element_finder

    @property
    def max_wait_time(self):
        return self.config.get_arjuna_option_value("guiauto.max.wait").as_int()

    def wait_until_element_absent(self, lmd, max_wait_time=None):
        max_wait_time = max_wait_time and max_wait_time or self.max_wait_time
        return self.__container_conditions.AbsenceOfElement(lmd).wait(max_wait_time=max_wait_time)

    def wait_until_element_found(self, gui_element, max_wait_time=None):
        max_wait_time = max_wait_time and max_wait_time or self.max_wait_time
        return self.__container_conditions.PresenceOfElement(gui_element).wait(max_wait_time=max_wait_time)

    def wait_until_multielement_found(self, multi_guielement, max_wait_time=None):
        max_wait_time = max_wait_time and max_wait_time or self.max_wait_time
        return self.__container_conditions.PresenceOfMultiElement(multi_guielement).wait(max_wait_time=max_wait_time)

    def load_multielement(self, multi_guielement, max_wait_time=None):
        locator_type, locator_value, size, dispatcher = self.wait_until_multielement_found(multi_guielement, max_wait_time=max_wait_time)
        if size == 0:
            raise Exception("MultiElement could not be found with any of the provided locators.")
        multi_guielement.located_with = locator_type, locator_value
        multi_guielement.dispatcher = dispatcher
        multi_guielement.size = size
        multi_guielement.load_source_parser()

    def load_element(self, gui_element, max_wait_time=None):
        locator_type, locator_value, size, dispatcher = self.wait_until_element_found(gui_element, max_wait_time=max_wait_time)
        gui_element.located_with = locator_type, locator_value
        gui_element.dispatcher = dispatcher
        gui_element.load_source_parser()