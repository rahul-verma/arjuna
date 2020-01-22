from .handler import Handler
from arjuna.interact.gui.auto.impl.base.conditions import *

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