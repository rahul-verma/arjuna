from arjuna.interact.gui.auto.dispatcher.driver.element_commands import DriverElementCommands
from arjuna.interact.gui.auto.dispatcher.driver.element_finder import ElementFinder

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
 
    def set_partial(self, index):
        self.__partial = True
        self.__instance_index = index

    def find_element(self, child_gui_element_setu_id, with_type, with_value):
        return ElementFinder.find_element(self.element, with_type, with_value)

    def find_multielement(self, child_gui_element_setu_id, with_type, with_value):
        return ElementFinder.find_elements(self.element, with_type, with_value)

    @property
    def driver(self):
        return self.__driver_dispatcher.driver

    def click(self):
        DriverElementCommands.click(self.driver_element)

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