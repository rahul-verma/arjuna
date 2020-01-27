from arjuna.core.poller.conditions import *
from arjuna.core.poller.caller import *

class GuiAutomatorConditions:

    def __init__(self, automator):
        self.__automator = automator

    @property
    def automator(self):
        return self.__automator

    def AlertIsPresent(self):
        caller = DynamicCaller(self.automator.alert_handler.is_alert_present)
        return BooleanCondition(caller, True)