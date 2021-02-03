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

'''
Classes to assist in HTML Parsing. 
'''

from io import StringIO
from lxml.html import soupparser

from .xml import XmlNode

class HtmlNode(XmlNode):
    '''
        Represents a single node in a parsed HTML.

        Arguments:
            node: **lxml** Element object.
    '''

    def __init__(self, node):
        super().__init__(node)

    def clone(self) -> 'HtmlNode':
        '''
            Create a clone of this HtmlNode object.
        '''
        return Html.from_str(str(self))

    @property
    def inner_html(self) -> str:
        '''
            Unaltered inner HTML of this node.
        '''
        return self.inner_xml

    @property
    def normalized_inner_html(self) -> str:
        '''
            Normalized inner XML of this node, with empty lines removed between children nodes.
        '''
        return self.normalized_inner_xml

class Html:
    '''
        Helper class to create HtmlNode objects.
    '''

    @classmethod
    def from_str(self, html_str, partial=False) -> HtmlNode:
        '''
            Create an `HtmlNode` from a string.

            Keyword Arguments:
                partial: If True, the provided string is considered as a part of HTML for parsing.
        '''
        if partial:
            html_str = f"<html><body>{html_str}</body></html>"
            lxml_tree = soupparser.parse(StringIO(html_str))
            body = lxml_tree.getroot().find('body')
            return HtmlNode(list(body)[0])
        else:
            lxml_tree = soupparser.parse(StringIO(html_str))
            body = lxml_tree.getroot()
            return HtmlNode(body)

    @classmethod
    def from_file(cls, file_path: str, partial=False) -> HtmlNode:
        '''
            Creates an `HtmlNode` from file.

            Arguments:
                file_path: Absolute path of the json file.

            Keyword Arguments:
                partial: If True, the provided string is considered as a part of HTML for parsing.

            Returns:
                Arjuna's `HtmlNode` object
        '''

        with open(file_path, 'r') as f:
            return cls.from_str(f.read(), partial=partial)

    @classmethod
    def from_lxml_element(self, element, clone=False) -> HtmlNode:
        '''
            Create an `HtmlNode` from an `lxml` element.

            Arguments:
                element: `lxml` element
        '''
        if clone:
            return HtmlNode(element)
        else:
            return HtmlNode(element).clone()

