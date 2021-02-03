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

from arjuna.core.poller.caller import DynamicCaller
from arjuna.core.poller.conditions import CommandCondition

class GuiGuiWidgetContainerConditions:

    def __init__(self, container):
        self.__container = container

    @property
    def container(self):
        return self.__container

    def PresenceOfElement(self, gui_element):
        caller = DynamicCaller(
            self.container._element_finder.find,  
            self.__container.dispatcher.find_element,
            gui_element._wmd,
            context = "ELEMENT"
        )
        return CommandCondition(caller)   

    def PresenceOfMultiElement(self, gui_element):
        caller = DynamicCaller(
            self.container._element_finder.find, 
            self.container.dispatcher.find_multielement,
            gui_element._wmd,
            context = "MULTI_ELEMENT"
        )
        return CommandCondition(caller)  

    def AbsenceOfElement(self, wmd):
        caller = DynamicCaller(
            self.container._element_finder.check_for_absence, 
            self.container.dispatcher.find_element,
            wmd,
            context = "ELEMENT"
        )
        return CommandCondition(caller) 