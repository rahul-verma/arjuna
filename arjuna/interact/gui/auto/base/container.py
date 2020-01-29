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

    def wait_until_element_found(self, gui_element, max_wait_time=None):
        max_wait_time = max_wait_time and max_wait_time or self.max_wait_time
        return self.__container_conditions.PresenceOfElement(gui_element).wait(max_wait_time=max_wait_time)

    def wait_until_multielement_found(self, multi_guielement, max_wait_time=None):
        max_wait_time = max_wait_time and max_wait_time or self.max_wait_time
        return self.__container_conditions.PresenceOfMultiElement(multi_guielement).wait(max_wait_time=max_wait_time)

    def load_multielement(self, multi_guielement, max_wait_time=None):
        locator_type, locator_value, instance_count, dispatcher = self.wait_until_multielement_found(multi_guielement, max_wait_time=max_wait_time)
        if instance_count == 0:
            raise Exception("MultiElement could not be found with any of the provided locators.")
        multi_guielement.located_with = locator_type, locator_value
        multi_guielement.dispatcher = dispatcher
        multi_guielement.instance_count = instance_count
        multi_guielement.load_source_parser()

    def load_element(self, gui_element, max_wait_time=None):
        locator_type, locator_value, instance_count, dispatcher = self.wait_until_element_found(gui_element, max_wait_time=max_wait_time)
        gui_element.located_with = locator_type, locator_value
        gui_element.dispatcher = dispatcher
        gui_element.load_source_parser()