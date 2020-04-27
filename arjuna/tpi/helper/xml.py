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
Classes to assist in XML Parsing. 
'''

from lxml import etree, html
from typing import List, Dict, Tuple

from arjuna.tpi.tracker import track

@track("debug")
class NodeLocator:
    '''
        Locator for finding an XML Node in an **XmlNode**.

        Keyword Arguments:
            tag: (Optional) Tag of the node
            **attrs: Arbitrary number of key value pairs representing attribute name and value.

        Raises:
            Exception: If neither tag nor an attribute is provided.

        Note:
            You can use tag and attributes in combination.

            Supports nested node finding.
    '''
    
    def __init__(self, *, tag: str=None, **attrs):

        if tag is None and not attrs:
            raise Exception("You must provided tag and/or attributes for finding nodes.")

        attr_conditions = []
        if attrs:
            for attr, value in attrs.items():
                if value is None:
                    attr_conditions.append("@{}".format(attr))
                else:
                    attr_conditions.append("contains(@{}, '{}')".format(attr, value))

        attr_str = ""
        if attr_conditions:
            attr_str = "[{}]".format("and ".join(attr_conditions))
        tag = tag and tag or "*"
        prefix = ".//"

        self.__xpath = "{}{}{}".format(prefix, tag, attr_str)

    def search_node(self, xml_node):
        return [XmlNode(n) for n in xml_node.xpath(self.__xpath)]

@track("debug")
class XmlNode:
    '''
        Represents a single node in a parsed XML.

        Arguments:
            node: **lxml** Element object.
    '''

    def __init__(self, node):
        self.__node = node

    @property
    def xml_node(self):
        '''
            Wrapped **lxml** Element

            Not supposed to be used directly.
        '''
        return self.__node

    @property
    def text(self) -> str:
        '''
            Text of the node.

            Note:
                Multiple texts are joined together.
        '''
        return self.xml_node.text

    @property
    def texts(self) -> list:
        '''
            List of Texts of the node.

            Note:
                Multiple texts are stored separately.
        '''
        return self.xml_node.xpath("//text()")

    @property
    def tag(self) -> str:
        '''
            Tag of the node.
        '''     
        return self.xml_node.tag

    @property
    def children(self) -> List['XmlNode']:
        '''
            All Children of this node as a List of XmlNodes
        '''
        return [XmlNode(c) for c in list(self.xml_node)]

    @property
    def parent(self) -> 'XmlNode':
        '''
            Parent XmlNode
        '''
        return XmlNode(self.xml_node.getparent())

    @property
    def preceding_sibling(self) -> 'XmlNode':
        '''
            The XmlNode before this node at same hierarchial level.
        '''
        return XmlNode(self.xml_node.getprevious())

    @property
    def following_sibling(self) -> 'XmlNode':
        '''
            The XmlNode after this node at same hierarchial level.
        '''
        return XmlNode(self.xml_node.getnext())

    @property
    def attrs(self) -> Dict[str,str]:
        '''
            All Attributes of this node as a dictionary.
        '''
        return dict(self.xml_node.attrib)

    def attr(self, name) -> str:
        '''
            Value of an attribute of this node.
        '''
        return self.xml_node.get(name)

    def has_attr(self, name):
        '''
            Check if an attribute is present.
        '''
        return name in self.xml_node.attrib

    def __xpath(self, xpath):
        if not xpath.startswith("."):
            return "." + xpath
        else:
            return xpath

    def findall_with_xpath(self, xpath) -> List['XmlNode']:
        '''
            Find all XmlNodes that match an XPath.
        '''
        return [XmlNode(n) for n in self.xml_node.xpath(self.__xpath(xpath))]

    def find_with_xpath(self, xpath, position=1):
        '''
            Find nth XmlNode that matches an XPath.

            Args:
                xpath: XPath string
                position: XPath index. Default is 1.
        '''
        return self.findall_with_xpath(xpath)[position]

    def as_str(self) -> str:
        '''
            String representation of this node.
        '''
        return etree.tostring(self.xml_node, encoding=str)

    def __str__(self):
        return self.as_str()

    def findall(self, *node_locators, stop_when_matched: bool=False) -> List['XmlNode']:
        '''
            Find all XmlNodes that match one of more `NodeLocator` s.

            Args:
                *node_locators: One or more `NodeLocator` s

            Keyword Arguments:
                stop_when_matched: If True, the call returns nodes found by the first `NodeLocator` that locates one or more nodes. Default is False.

            Returns:
                List of `XmlNode` s. In case of no match, empty list is returned.
        '''

        out = []
        for locator in node_locators:
            nodes = locator.search_node(self.xml_node)
            out.extend(nodes)
            if stop_when_matched:
                if nodes:
                    break
        return out

    def find(self, *node_locators, stop_when_matched: bool=False) -> 'XmlNode':
        '''
            Find first `XmlNode` that match one of more `NodeLocator` s.

            Args:
                *node_locators: One or more `NodeLocator` s

            Keyword Arguments:
                stop_when_matched: If True, the call returns nodes found by the first `NodeLocator` that locates one or more nodes.

            Note:
                In case of no node match, returns None
        '''
        matches = self.findall(*node_locators, stop_when_matched=stop_when_matched)
        if matches:
            return matches[0]
        else:
            return None

    def find_keyvalue_texts(self, key_locator, value_locator) -> Tuple[str, str]:
        '''
            Returns texts of first XmlNodes for a pair of `NodeLocator` s

            Args:
                key_locator: First `NodeLocator` (key)
                value_locator: First `NodeLocator` (value)

            Returns:
                2-element tuple containing the text strings.
        '''
        key = self.find(key_locator).text
        value = self.find(value_locator).text
        return key,value