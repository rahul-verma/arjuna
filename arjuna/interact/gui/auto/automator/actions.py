# This file is a part of Arjuna
# Copyright 2015-2021 Rahul Verma

# Website: www.RahulVerma.net

# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at

#   http://www.apache.org/licenses/LICENSE-2.0

# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

# from arjuna.tpi.constant import ArjunaOption
# from arjuna.client.core.action import *
# from arjuna.interact.gui.auto.finder.wmd import SimpleGuiWidgetMetaData

# from .guiautomator import GuiAutomator
# from .handler import Handler

# class SingleActionChain(Handler):

#     def __init__(self, automator, element=None):
#         super().__init__(automator)
#         from arjuna.interact.gui.auto.widget.frame import DomRoot
#         self.__automator = automator
#         self.__element = element
#         self.__attached_to_element = element is not None

#     def is_click_action(self, action):
#         return PartialActionType[action["actionType"]] == PartialActionType.CLICK

#     def are_args_defined(self, action):
#         return "args" in action

#     def get_args(self, action):
#         return action["args"]

#     def contains_target_element(self, action):
#         return "targetElement" in self.get_args(action)

#     def get_target_element(self, action):
#         return action["args"]["targetElement"]

#     def contains_target_point(self, action):
#         return "targetPoint" in self.get_args(action)

#     def get_target_point(self, action):
#         return action["args"]["targetPoint"]

#     def perform(self, single_action_chain):
#         processed_list = []
#         current_action_list = []
#         for action in single_action_chain:
#             if self.is_click_action(action):
#                 if not self.are_args_defined():
#                     current_action_list.append(("click", dict()))
#                     continue

#                 target_element = None
#                 if self.contains_target_element(action):
#                     target_element_id = self.get_target_element(action)
#                     target_element = self.__automator.get_element_for_setu_id(target_element_id)
#                 elif self.contains_target_point(action):
#                     wmd = SimpleGuiWidgetMetaData("point", self.get_target_point(action))
#                     element = self.__automator.create_element(wmd)
                
#                 if target_element:
#                     target_element.find_if_not_found()
#                     current_action_list.append(("click", {"on_element" : (target_element.setu_id, True)}))
                    
#         processed_list.append(current_action_list)
#         for single_chain in processed_list:
#             self.__automator.dispatcher.perform_action_chain(single_chain)


        



