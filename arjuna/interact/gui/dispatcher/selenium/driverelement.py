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


from arjuna.interact.gui.dispatcher.driver.element_commands import DriverElementCommands
from arjuna.interact.gui.dispatcher.driver.element_finder import SeleniumElementFinder
from arjuna.interact.gui.dispatcher.driver.melement import MultiElement
from arjuna.tpi.error import *
from arjuna.core.error import *

class SeleniumDriverElementDispatcher:

    def __init__(self, driver_dispatcher, element):
        self.__driver_dispatcher = driver_dispatcher
        self.__driver = driver_dispatcher.driver
        self.__element = element
        self.__partial = False
        self.__instance_index = 0

    @property
    def driver_element(self):
        return self.__element

    @classmethod
    def create_dispatcher(cls, automator_dispatcher, web_element):
        return SeleniumDriverElementDispatcher(automator_dispatcher, web_element)
 
    def set_partial(self, index):
        self.__partial = True
        self.__instance_index = index

    def find_element(self, with_type, with_value, *, relations=None, filters=None):
        element = SeleniumElementFinder.find_element(self.driver_element, with_type, with_value, relations=relations, filters=filters)
        return 1, self.create_dispatcher(self.__driver_dispatcher, element)

    def find_multielement(self, with_type, with_value, *, relations=None, filters=None):
        web_elements = SeleniumElementFinder.find_elements(self.driver_element, with_type, with_value, relations=relations, filters=filters)
        melement = MultiElement([self.create_dispatcher(self.__driver_dispatcher, web_element) for web_element in web_elements])
        return melement.get_size(), melement

    @property
    def driver(self):
        return self.__driver_dispatcher.driver

    def click(self):
        try:
            DriverElementCommands.click(self.driver_element)
        except Exception as e:
            raise GuiWidgetNotReadyError(str(e))

    def hover(self):
        self.__driver_dispatcher.hover_on_element(self)

    def mouse_click(self):
        self.__driver_dispatcher.mouse_click_on_element(self)

    def double_click(self):
        self.__driver_dispatcher.double_click_on_element(self)

    def scroll_to_view(self):
        self.__driver_dispatcher.scroll_to_element(self)

    def clear_text(self):
        DriverElementCommands.clear_text(self.driver_element)

    def send_text(self, text):
        DriverElementCommands.send_text(self.driver_element, text)

    def is_selected(self):
        return DriverElementCommands.is_selected(self.driver_element)

    def is_visible(self):
        return DriverElementCommands.is_visible(self.driver_element)

    def is_clickable(self):
        return DriverElementCommands.is_clickable(self.driver_element)

    def get_tag_name(self):
        return DriverElementCommands.get_tag_name(self.driver_element)

    def get_attr_value(self, attr_name, optional=False):
        try:
            return DriverElementCommands.get_attr_value(self.driver_element, attr_name)
        except Exception as e:
            if optional:
                return None
            else:
                raise e

    def get_text_content(self):
        return DriverElementCommands.get_text_content(self.driver_element)

    def scroll_full_height(self):
        self.__driver_dispatcher.execute_javascript("arguments[0].scrollBy(0, arguments[1].scrollHeight)", self.driver_element, self.driver_element)