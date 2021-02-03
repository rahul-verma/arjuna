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