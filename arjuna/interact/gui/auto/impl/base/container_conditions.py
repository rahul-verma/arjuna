from arjuna.interact.gui.auto.impl.base.conditions import DynamicCaller, CommandCondition

class GuiElementContainerConditions:

    def __init__(self, container):
        self.__container = container

    def PresenceOfElement(self, gui_element):
        caller = DynamicCaller(
            self.__container._find,  
            self.__container.dispatcher.find_element,
            gui_element,
            context = "ELEMENT"
        )
        return CommandCondition(caller)   

    def PresenceOfMultiElement(self, gui_element):
        caller = DynamicCaller(
            self.__container._find, 
            self.__container.dispatcher.find_multielement,
            gui_element,
            context = "MULTI_ELEMENT"
        )
        return CommandCondition(caller)  