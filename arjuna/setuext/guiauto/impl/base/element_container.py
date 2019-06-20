import abc

from arjuna.setu.types import SetuConfiguredObject

from .container_conditions import GuiElementContainerConditions


class ElementContainer(SetuConfiguredObject, metaclass=abc.ABCMeta):
    def __init__(self, config):
        super().__init__(config)
        self.element_map = {}
        self.melement_map = {}
        self.__container_conditions = GuiElementContainerConditions(self)

    def _add_element(self, setu_id, element):
        self.element_map[setu_id] = element

    def _add_multielement(self, setu_id, melement):
        self.melement_map[setu_id] = melement

    def get_element_for_setu_id(self,id):
        return self.element_map[id]

    def get_multielement_for_setu_id(self,id):
        return self.melement_map[id]

    @abc.abstractmethod
    def _create_element_flat_or_nested(self, locator_meta_data):
        pass

    @abc.abstractmethod
    def _create_multielement_flat_or_nested(self, locator_meta_data):
        pass

    def create_element(self, locator_meta_data):
        elem = self._create_element_flat_or_nested(locator_meta_data)
        elem.dispatcher_creator = self.dispatcher_creator
        self._add_element(elem.get_setu_id(), elem)
        return elem

    def create_multielement(self, locator_meta_data):
        element = self._create_multielement_flat_or_nested(locator_meta_data)
        element.dispatcher_creator = self.dispatcher_creator
        self._add_multielement(element.get_setu_id(), element)
        return element

    def create_dropdown(self, locator_meta_data):
        from arjuna.setuext.guiauto.impl.element.dropdown import GuiWebSelect
        select = GuiWebSelect(self, locator_meta_data)
        self._add_element(select.get_setu_id(), select)
        return select

    def create_radiogroup(self, locator_meta_data):
        from arjuna.setuext.guiauto.impl.element.radio_group import GuiWebRadioGroup
        rg = GuiWebRadioGroup(self, locator_meta_data)
        rg.dispatcher_creator = self.dispatcher_creator
        self._add_element(rg.get_setu_id(), rg)
        return rg

    def _find(self, dispatcher_call, gui_element):
        found = False
        for locator in gui_element.get_locator_meta_data().locators: 
            try:
                instance_count = dispatcher_call(gui_element.get_setu_id(), locator.ltype.name, locator.lvalue)
                return locator.ltype.name, locator.lvalue, instance_count
            except Exception as e:
                print(e)
                continue
        if not found:
            raise Exception("Could not locate elements with locator(s): {}".format(gui_element.get_locator_meta_data().locators))

    def wait_until_element_found(self, gui_element):
        return self.__container_conditions.PresenceOfElement(gui_element).wait()

    def wait_until_multielement_found(self, gui_element):
        return self.__container_conditions.PresenceOfMultiElement(gui_element).wait()

    def find_multielement(self, gui_element):
        locator_type, locator_value, instance_count = self.wait_until_multielement_found(gui_element)
        gui_element.set_found_with(locator_type, locator_value)
        gui_element.set_instance_count(instance_count)

    def find_element(self, gui_element):
        locator_type, locator_value, __ = self.wait_until_element_found(gui_element)
        gui_element.set_found_with(locator_type, locator_value)
