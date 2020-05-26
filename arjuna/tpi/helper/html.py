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

    def clone(self):
        return Html.from_str(str(self))

class Html:

    @classmethod
    def from_str(self, html_str):
        return HtmlNode(soupparser.parse(StringIO(html_str)))

    @classmethod
    def from_lxml_node(self, node, clone=False):
        return HtmlNode(node)

