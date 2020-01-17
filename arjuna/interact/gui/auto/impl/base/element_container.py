import abc

from .container_conditions import GuiElementContainerConditions
from .conditions import *


class ElementContainer(metaclass=abc.ABCMeta):
    def __init__(self, config, obj_name=""):
        self.__config = config
        self.__obj_name = obj_name
        self.element_map = {}
        self.melement_map = {}
        self.__container_conditions = GuiElementContainerConditions(self)

    @property
    def max_wait_time(self):
        return self.config.get_arjuna_option_value("guiauto.max.wait").as_int()

    @property
    def config(self):
        return self.__config

    def _add_element(self, setu_id, element):
        self.element_map[setu_id] = element

    def _add_multielement(self, setu_id, melement):
        self.melement_map[setu_id] = melement

    def get_element_for_setu_id(self,id):
        return self.element_map[id]

    def get_multielement_for_setu_id(self,id):
        return self.melement_map[id]

    @abc.abstractmethod
    def _create_element_flat_or_nested(self, lmd):
        pass

    @abc.abstractmethod
    def _create_multielement_flat_or_nested(self, lmd):
        pass

    def define_element(self, lmd):
        return self._create_element_flat_or_nested(lmd)

    def define_multielement(self, lmd):
        return self._create_multielement_flat_or_nested(lmd)

    def define_dropdown(self, lmd, option_container_lmd=None, option_lmd=None):
        from arjuna.interact.gui.auto.impl.element.dropdown import GuiWebSelect
        return GuiWebSelect(self, lmd, option_container_lmd=option_container_lmd, option_lmd=option_lmd)

    def define_radiogroup(self, lmd):
        from arjuna.interact.gui.auto.impl.element.radio_group import GuiWebRadioGroup
        return GuiWebRadioGroup(self, lmd)

    def _find(self, dispatcher_call, gui_element, context="ELEMENT"):
        found = False
        js_call_name = context == "ELEMENT" and "find_element_with_js" or "find_multielement_with_js"
        js_call = getattr(self, js_call_name)
        locators = gui_element.get_lmd().locators
        if context != "ELEMENT":
            if "POINT" in {l.ltype.name for l in locators}:
                raise ConditionException("With.POINT can be used only with GuiElement.")

        for locator in locators: 
            try:
                if locator.ltype.name == "POINT":
                    # Assumption here is that this container is automator.
                    instance_count, dispatcher = js_call("return document.elementFromPoint({}, {})".format(*locator.lvalue))
                elif locator.ltype.name == "JAVASCRIPT":
                    instance_count, dispatcher = js_call(locator.lvalue)
                else:
                    instance_count, dispatcher = dispatcher_call(locator.ltype.name, locator.lvalue)
                return locator.ltype.name, locator.lvalue, instance_count, dispatcher
            except Exception as e:
                print(e)
                import traceback
                traceback.print_exc()
                continue
        if not found:
            raise Exception("Could not locate elements with locator(s): {}".format(gui_element.get_lmd()))

    def wait_until_element_found(self, gui_element):
        return self.__container_conditions.PresenceOfElement(gui_element).wait(max_wait_time=self.max_wait_time)

    def wait_until_multielement_found(self, gui_element):
        return self.__container_conditions.PresenceOfMultiElement(gui_element).wait(max_wait_time=self.max_wait_time)

    def find_multielement(self, gui_element):
        locator_type, locator_value, instance_count, dispatcher = self.wait_until_multielement_found(gui_element)
        if instance_count == 0:
            raise Exception("MultiElement could not be found with any of the provided locators.")
        gui_element.set_found_with(locator_type, locator_value)
        gui_element.dispatcher = dispatcher
        gui_element.set_instance_count(instance_count)

    def find_element(self, gui_element):
        locator_type, locator_value, instance_count, dispatcher = self.wait_until_element_found(gui_element)
        gui_element.set_found_with(locator_type, locator_value)
        gui_element.dispatcher = dispatcher
