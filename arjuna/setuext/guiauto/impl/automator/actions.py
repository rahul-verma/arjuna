from arjuna.tpi.enums import ArjunaOption
from arjuna.client.core.action import *

from .guiautomator import GuiAutomator
from .handler import Handler

class SingleActionChain(Handler):

    def __init__(self, automator, element=None):
        super().__init__(automator)
        from arjuna.setuext.guiauto.impl.element.frame import DomRoot
        self.__automator = automator
        self.__element = element
        self.__attached_to_element = element is not None

    def perform(self, single_action_chain):
        processed_list = []
        current_action_list = []
        for action in single_action_chain:
            if PartialActionType[action["actionType"]] == PartialActionType.CLICK:
                if "args" in action:
                    if "targetElement" in action["args"]:
                        element = self.__automator.get_element_for_setu_id(action["args"]["targetElement"])
                        element.find_if_not_found()
                        current_action_list.append(("click", {"on_element" : (action["args"]["targetElement"], True)}))
                else:
                    current_action_list.append(("click", dict()))
        processed_list.append(current_action_list)
        for single_chain in processed_list:
            self.__automator.dispatcher.perform_action_chain(single_chain)


        



