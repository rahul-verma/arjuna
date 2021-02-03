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

from arjuna.tpi.tracker import track

@track("trace")
class GuiSourceContent:
    '''
        Source content of a Gui or GuiWidget.

        Not meant to be directly constructed by a test author. Retrieve as:
        
            .. code-block:: python
                
                gui_entity.source.content

        Arguments:
            all: Complete XML source
            root: Source of XML root.
            inner: All source minus the root source.
            text: Text content.
    '''

    def __init__(self, all, root, inner, text):
        self.__all = all
        self.__root = root
        self.__inner = inner
        self.__text = text

    @property
    def all(self) -> str:
        '''
            Complete source of associated Gui entity.
        '''
        return self.__all

    @property
    def root(self) -> str:
        '''
            Source of root node of associated Gui entity.
        '''
        return self.__root

    @property
    def inner(self) -> str:
        '''
            Complete source of associated Gui entity minus the root node source.
        '''
        return self.__inner

    @property
    def text(self) -> str:
        '''
            All text content of associated Gui entity.
        '''
        return self.__text