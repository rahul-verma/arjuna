from arjuna.core.poller.caller import DynamicCaller
from arjuna.core.poller.conditions import CommandCondition

class GuiElementContainerConditions:

    def __init__(self, container):
        self.__container = container

    @property
    def container(self):
        return self.__container

    def PresenceOfElement(self, gui_element):
        caller = DynamicCaller(
            self.container.element_finder.find,  
            self.__container.dispatcher.find_element,
            gui_element,
            context = "ELEMENT"
        )
        return CommandCondition(caller)   

    def PresenceOfMultiElement(self, gui_element):
        caller = DynamicCaller(
            self.container.element_finder.find, 
            self.container.dispatcher.find_multielement,
            gui_element,
            context = "MULTI_ELEMENT"
        )
        return CommandCondition(caller)  