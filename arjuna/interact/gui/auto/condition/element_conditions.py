import abc
import types

from arjuna.core.poller.caller import DynamicCaller
from arjuna.core.poller.conditions import BooleanCondition, CommandCondition

class Handler(metaclass=abc.ABCMeta):

    def __init__(self, element_obj):
        self.__element = element_obj
        self.__config = element_obj.config

    @property
    def element(self):
        return self.__element

    @property
    def config(self):
        return self.__config


class GuiElementConditions(Handler):

    def __init__(self, element):
        super().__init__(element)

    def IsSelected(self):
        caller = DynamicCaller(self.element.is_selected)
        return BooleanCondition(caller, True)

    def IsVisible(self):
        caller = DynamicCaller(self.element.is_visible)
        return BooleanCondition(caller, True)   

    def IsClickable(self):
        caller = DynamicCaller(self.element.is_clickable)
        return BooleanCondition(caller, True)     

class GuiElementLenientInteraction:

    def __init__(self, gui_element):
        self.__element = gui_element

    def Click(self):
        caller = DynamicCaller(
            self.__element._only_click
        )
        return CommandCondition(caller)  

    def SetText(self, text):
        caller = DynamicCaller(
            self.__element._only_set_text,
            text,
        )
        return CommandCondition(caller) 