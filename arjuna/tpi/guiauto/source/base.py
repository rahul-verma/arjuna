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

import re
import os
import copy
import abc
from collections import namedtuple
from lxml import etree
from arjuna.tpi.helper.html import Html, HtmlNode
from arjuna.tpi.tracker import track
from .content import GuiSourceContent


def _process_child_html(in_str):
    processed = os.linesep.join([l for l in in_str.splitlines() if l.strip()])
    return "\t" + processed

def _remove_empty_lines_from_string(in_str):
    return ' '.join([l.strip() for l in in_str.splitlines() if l.strip()])

def _empty_or_none(in_str):
    if type(in_str) is str and not in_str.strip():
        return True
    else:
        return in_str is None

@track("debug")
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

@track("debug")
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

    def __init__(self, raw_source, root_tag):
        super().__init__()
        self.__raw_source = raw_source
        self.__root_tag = root_tag
        self.__fpaths = []
        self.__node = None 
        self.__elem_node = None

    @property
    def node(self) -> HtmlNode:
        '''
            Source code as an Arjuna :class:`~arjuna.tpi.helper.xml.XmlNode` for advanced inquiry and parsing.
        '''
        return self.__node

    @property
    def _elem_node(self):
        return self.__elem_node

    def _process_elem_node(self, elem_node):
        pass

    def _load(self):
        raw_source = self.__raw_source
        # parser = etree.HTMLParser(remove_comments=True)
        if self.__root_tag == "body":
            tree = Html.from_str(f"<html><body>{raw_source}</body></html>").node
        else:
            tree = Html.from_str(raw_source).node

        if self.__root_tag == "body":
            body = tree.getroot().find('body')
            elem_node = list(body)[0]
        else:
            body = tree.getroot()
            elem_node = body

        self.__elem_node = Html.from_lxml_node(elem_node)
        self.__node = self.__elem_node.clone()

        normalized_text_content = os.linesep.join(
            [
                _remove_empty_lines_from_string(c.text)
                for c in elem_node.iter() 
                if not _empty_or_none(c.text)
            ]).strip()

        normalized_inner_html = os.linesep.join([
            _process_child_html(etree.tostring(c, encoding='unicode'))
            for c in list(elem_node.iterchildren())
            ])

        self.__text_content = normalized_text_content
        self.__inner_html = normalized_inner_html
        self.__full_source = raw_source
        for child in list(elem_node): elem_node.remove(child)
        self.__self_source = ' '.join(etree.tostring(elem_node, encoding=str).splitlines())
        self.__self_source = re.sub(r"\s+", " ", self.__self_source)

        self._content = GuiSourceContent(all=self.__full_source, root=self.__self_source, inner=self.__inner_html, text=self.__text_content)

        self._process_elem_node(elem_node)
