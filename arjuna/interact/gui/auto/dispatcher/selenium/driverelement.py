from arjuna.interact.gui.auto.dispatcher.driver.element_commands import DriverElementCommands
from arjuna.interact.gui.auto.dispatcher.driver.element_finder import ElementFinder
from arjuna.interact.gui.auto.dispatcher.driver.melement import MultiElement
from arjuna.interact.gui.auto.dispatcher.commons.exceptions import *

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

    def find_element(self, with_type, with_value):
        element = ElementFinder.find_element(self.__driver, with_type, with_value)
        return 1, self.create_dispatcher(self.__driver_dispatcher, element)

    def find_multielement(self, with_type, with_value):
        web_elements = ElementFinder.find_elements(self.__driver, with_type, with_value)
        melement = MultiElement([self.create_dispatcher(self.__driver_dispatcher, web_element) for web_element in web_elements])
        return melement.get_instance_count(), melement

    @property
    def driver(self):
        return self.__driver_dispatcher.driver

    def click(self):
        try:
            DriverElementCommands.click(self.driver_element)
        except Exception as e:
            raise GuiElementNotReady(str(e))

    def hover(self):
        self.__driver_dispatcher.hover_on_element(self)

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