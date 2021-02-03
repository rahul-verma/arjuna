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

class Locatable:
    '''
        Represents an object that is locatable using **GuiWidgetMetaData** in a **Gui**.
    '''

    def __init__(self, gui, wmd):
        # super().__init__(automator.config) #, obj_name)
        self.__gui = gui
        self.__automator = gui._automator
        self.__wmd = wmd
        self.__located = False
        self.__located_with = None 

        # self.__parent = parent

    @property
    def gui(self):
        '''
            **Gui** object containing this **Locatable** object.
        '''
        return self.__gui
        
    @property
    def _automator(self):
        return self.__automator

    @property
    def _wmd(self):
        return self.__wmd

    @property
    def _is_located(self):
        return self.__located

    @property
    def located_with(self):
        '''
            Identifier which located this Locatable. Useful to know if multiple identifiers are present in GuiWidgetDefinition.
        '''
        return self.__located_with

    @located_with.setter
    def _located_with(self, locator_tuple):
        self.__located = True
        self.__located_with = locator_tuple