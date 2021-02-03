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

import os

from arjuna.tpi.tracker import track
from .base import GuiSource
from .content import GuiSourceContent
from arjuna.tpi.parser.xml import XmlNode

@track("trace")
class GuiMultiElementSource(GuiSource):
    '''
        A combined source of all GuiElements in a GuiMultiElement.

        Not meant to be directly constructed by a test author. Use **.source** property of **GuiMultiElement**.
    '''

    def __init__(self, instances):
        super().__init__()
        self.__instances = instances
        self._content = GuiSourceContent(all=self.__get_full_content(), root=self.__get_root_content(), inner=self.__get_inner_content(), text=self.__get_text_content())
    
    def __get_full_content(self):
        return os.linesep.join([e.source.content.all for e in self.__instances])

    def __get_inner_content(self):
        return os.linesep.join([e.source.content.inner for e in self.__instances])

    def __get_text_content(self):
        return os.linesep.join([e.source.content.text for e in self.__instances])

    def __get_root_content(self):
        return os.linesep.join([e.source.content.root for e in self.__instances])

    def _get_root_content_as_list(self):
        return [e.source.content.root for e in self.__instances]

    @property
    def tag_names(self) -> list:
        '''
            Tag names of all GuiElements in this **GuiMultiElement**.
        '''
        return [e.source.tag for e in self.__instances]

    @property
    def texts(self) -> list:
        '''
            Text of all GuiElements in this **GuiMultiElement**.
        '''
        return [e.source.content.text for e in self.__instances]

    @property
    def values(self) -> list:
        '''
            Content of value attribute of all GuiElements in this **GuiMultiElement**.
        '''
        return [e.source.get_attr_value("value") for e in self.__instances]

    def get_attr_values(self, attr) -> list:
        '''
            Content of value of given attribute of all GuiElements in this **GuiMultiElement**.

            Args:
                attr: Attribute name
        '''
        return [e.source.get_attr_value(attr) for e in self.__instances]
