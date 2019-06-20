from arjuna.setuext.guiauto.dispatcher.driver.impl.element_commands import DriverElementCommands
from arjuna.setuext.guiauto.dispatcher.driver.impl.element_finder import ElementFinder

class SeleniumDriverElement:

    def __init__(self, driver_wrapper, element_setu_id):
        self.__driver_wrapper = driver_wrapper
        self.__driver = driver_wrapper.driver
        self.__automator_setu_id = driver_wrapper.setu_id
        self.__element_set_id = element_setu_id
        self.__partial = False
        self.__instance_index = 0

    def set_partial(self, index):
        self.__partial = True
        self.__instance_index = index

    @property
    def automator_setu_id(self):
        return self.__automator_setu_id

    @property
    def element_setu_id(self):
        return self.__element_set_id


    def find_element(self, child_gui_element_setu_id, with_type, with_value):
        wrapped_element = self.__driver_wrapper.get_driver_element(self.element_setu_id)
        child_element = ElementFinder.find_element(wrapped_element, with_type, with_value)
        self.__driver_wrapper.add_driver_element(child_gui_element_setu_id, child_element)

    def find_multielement(self, child_gui_element_setu_id, with_type, with_value):
        wrapped_element = self.__driver_wrapper.get_driver_element(self.element_setu_id)
        child_melement = ElementFinder.find_elements(wrapped_element, with_type, with_value)
        self.__driver_wrapper.add_driver_melement(child_gui_element_setu_id, child_melement)
        return child_melement.get_instance_count()

    @property
    def driver(self):
        return self.__driver_wrapper.driver

    @property
    def driver_element(self):
        if not self.__partial:
            return self.__driver_wrapper.get_driver_element(self.element_setu_id)
        else:
            return self.__driver_wrapper.get_driver_melement(self.element_setu_id).get_element_at_index(self.__instance_index)

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