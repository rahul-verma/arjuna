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

import re
import os
import copy
import abc
from collections import namedtuple
from lxml import etree
from arjuna.tpi.parser.html import Html, HtmlNode
from arjuna.tpi.tracker import track
from .content import GuiSourceContent

@track("trace")
class GuiSource:
    '''
        GUI Source of a GUI entity.

        Not meant to be directly constructed by a test author. Retrieve as:
        
            .. code-block:: python
                
                gui_entity.source
    '''
    def __init__(self):
        self.__content = None

    @property
    def content(self) -> GuiSourceContent:
        '''
            Source content of associated GUI entity returned as :class:`~arjuna.tpi.guiauto.source.content.GuiSourceContent`.
        '''
        return self.__content

    @content.setter
    def _content(self, content):
        self.__content = content

@track("trace")
class SingleGuiEntitySource(GuiSource, metaclass=abc.ABCMeta):
    '''
        Abstract Base class for GUI Source of a Singular GUI entity (**GuiPage** or **GuiElement**).

        Not meant to be directly constructed by a test author. Retrieve as:
        
            .. code-block:: python
                
                gui_entity.source

        Args:
            raw_source: Raw XML source.
            root_tag: 'html' for Gui and 'body' for GuiElement.
    '''

    def __init__(self, raw_source, partial=False):
        super().__init__()
        self.__raw_source = raw_source
        self.__partial = partial
        self.__fpaths = []
        self.__node = None 
        self.__elem_node = None

    @property
    def node(self) -> HtmlNode:
        '''
            Source code as an Arjuna :class:`~arjuna.tpi.parser.xml.XmlNode` for advanced inquiry and parsing.
        '''
        return self.__node

    @property
    def _elem_node(self):
        return self.__elem_node

    def _process_elem_node(self, elem_node):
        pass

    def _load(self):
        raw_source = self.__raw_source
        self.__elem_node = Html.from_str(raw_source, partial=self.__partial)
        self.__node = self.__elem_node.clone()
        self.__text_content = self.__elem_node.normalized_text
        self.__inner_html = self.__elem_node.normalized_inner_html
        self.__full_source = raw_source
        self.__elem_node.remove_all_children()
        self.__self_source = self.__elem_node.normalized_source
        self._content = GuiSourceContent(all=self.__full_source, root=self.__self_source, inner=self.__inner_html, text=self.__text_content)
        self._process_elem_node(self.__elem_node)
