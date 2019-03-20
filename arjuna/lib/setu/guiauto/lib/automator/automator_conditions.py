from .handler import Handler
from arjuna.lib.setu.guiauto.lib.base.conditions import *

class GuiAutomatorConditions(Handler):

    def __init__(self, automator):
        super().__init__(automator)

    def AlertIsPresent(self):
        caller = DynamicCaller(self.automator.alert_handler.is_alert_present)
        return BooleanCondition(caller, True)