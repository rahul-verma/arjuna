import abc
from arjuna.core.exceptions import WaitableError, GuiElementNotFoundError

class ElementFinder:
    def __init__(self, container): #, obj_name=""):
        self.__container = container
        self.__config = container.config
        # self.__obj_name = obj_name

    @property
    def config(self):
        return self.__config

    @property
    def container(self):
        return self.__container

    @abc.abstractmethod
    def _create_element_flat_or_nested(self, lmd):
        pass

    @abc.abstractmethod
    def _create_multielement_flat_or_nested(self, lmd):
        pass

    def find(self, dispatcher_call, gui_element, context="ELEMENT"):
        found = False
        js_call_name = context == "ELEMENT" and "find_element_with_js" or "find_multielement_with_js"
        js_call = getattr(self.container, js_call_name)
        locators = gui_element.lmd.locators
        if context != "ELEMENT":
            if "POINT" in {l.ltype.name for l in locators}:
                raise ConditionException("With.POINT can be used only with GuiElement.")

        we = None
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
            except WaitableError as e:
                we = e
            except Exception as f:
                raise f
            else:
                we = None
        if not found:
            raise GuiElementNotFoundError("None of the locators worked.", *gui_element.lmd.locators)