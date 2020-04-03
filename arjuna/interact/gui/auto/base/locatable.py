# This file is a part of Arjuna
# Copyright 2015-2020 Rahul Verma

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

    def __init__(self, gui, emd):
        # super().__init__(automator.config) #, obj_name)
        self.__gui = gui
        self.__automator = gui.automator
        self.__emd = emd
        self.__located = False
        self.__located_by = None 

        # self.__parent = parent

    @property
    def gui(self):
        return self.__gui
        
    @property
    def automator(self):
        return self.__automator

    @property
    def emd(self):
        return self.__emd

    @property
    def is_located(self):
        return self.__located

    @property
    def located_with(self):
        return self.__located_by

    @located_with.setter
    def located_with(self, locator_tuple):
        self.__located = True
        self.__located_by = locator_tuple