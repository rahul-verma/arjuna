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
Classes to assist in XML Parsing. 
'''
import os
import re
from lxml import etree, html
from typing import List, Dict, Tuple

from arjuna.tpi.tracker import track
from arjuna.tpi.helper.arjtype import CIStringDict

def _process_tags(tagsvalue):
    tag_list = None
    if type(tagsvalue) is str:
        tag_list = tagsvalue.strip().split()
    else:
        tag_list = tagsvalue
    return [t.lower()=='any' and '*' or t for t in tag_list]

@track("trace")
class NodeLocator:
    '''
        Locator for finding an XML Node in an **XmlNode**.

        Keyword Arguments:
            tags: (Optional) Descendant tags for the node. Can be a string of single or multiple tags or a list/tuple of tags.
            **attrs: Arbitrary number of key value pairs representing attribute name and value.

        Raises:
            Exception: If neither tag nor an attribute is provided.

        Note:
            You can use tag and attributes in combination.

            Supports nested node finding.
    '''
    
    def __init__(self, *, tags: 'strOrSequence'=None, **attrs):

        if tags is None and not attrs:
            raise Exception("You must provided tags and/or attributes for finding nodes.")

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
        tags = tags and "//".join(_process_tags(tags)) or "*"
        prefix = ".//"

        self.__xpath = "{}{}{}".format(prefix, tags, attr_str)

    def search_node(self, node: 'XmlNode') -> tuple:
        '''
        Search `XmlNode` objects that match this locator in the provided `XmlNode` object.
        '''
        return (XmlNode(n) for n in node.xpath(self.__xpath))


def _process_child_html(in_str):
    processed = "\n".join([l for l in in_str.splitlines() if l.strip()])
    return "\t" + processed

def _remove_empty_lines_from_string(in_str):
    return '\n'.join(
        [l.strip() for l in in_str.splitlines() if l.strip()]
    )

def _empty_or_none(in_str):
    if type(in_str) is str and not in_str.strip():
        return True
    else:
        return in_str is None


@track("trace")
class XmlNode:
    '''
        Represents a single node in a parsed XML.

        Arguments:
            node: **lxml** Element object.
    '''

    def __init__(self, node):
        self.__node = node
        self.__attrs = CIStringDict(self.node.attrib)

    @property
    def node(self):
        '''
            Wrapped **lxml** Element

            Not supposed to be used directly.
        '''
        return self.__node

    def get_text(self, normalize: bool=False) -> str:
        '''
            Text of this node.

            Keyword Arguments:
                normalize: If True, empty lines are removed and individual lines are trimmed.
        '''
        texts = self.texts

        if normalize:
            return "".join([l for l in texts if l !="\n"]).strip()
        else:
            return "".join(texts).strip()

    @property
    def normalized_text(self) -> str:
        '''
            Text of this node with empty lines removed and individual lines trimmed.
        '''
        return self.get_text(normalize=True)

    @property
    def text(self) -> str:
        '''
            Unaltered text of the node.
        '''
        text = self.get_text()
        if text is None:
            return ""
        else:
            return text

    @property
    def texts(self) -> list:
        '''
            List of Texts of the node.

            Note:
                Multiple texts are stored separately.
        '''
        return self.node.xpath(".//text()")

    def get_inner_xml(self, normalize=False) -> str:
        '''
            Inner XML of this node.

            Keyword Arguments:
                normalize: If True, empty lines are removed between children nodes.
        '''

        def same(i):
            return i

        processor = normalize and _process_child_html or same
        out = [
                processor(etree.tostring(c, encoding='unicode'))
                for c in list(self.__node.iterchildren())
            ]
        return "\n".join(out).strip()

    @property
    def inner_xml(self) -> str:
        '''
            Unaltered inner XML of this node
        '''
        return self.get_inner_xml()

    @property
    def normalized_inner_xml(self) -> str:
        '''
            Normalized inner XML of this node, with empty lines removed between children nodes.
        '''
        return self.get_inner_xml(normalize=True)

    def remove_all_children(self) -> None:
        '''
            Remove all children nodes from this node.
        '''
        for child in list(self.__node): self.__node.remove(child)

    def as_str(self, normalize=False) -> str:
        '''
            String representation of this node.

            normalize: If True all new lines are removed and more than one conseuctive space is converted to a single space.
        '''
        true_source = etree.tostring(self.node, encoding='unicode')
        if not normalize:
            return true_source
        else:
            ret_source = ' '.join(true_source.splitlines())
            return re.sub(r"\s+", " ", ret_source)

    @property
    def source(self) -> str:
        '''
            Unalereted string representation of this node.
        '''
        return self.as_str()

    @property
    def normalized_source(self) -> str:
        '''
            String representation of this node with all new lines removed and more than one conseuctive space converted to a single space.
        '''
        return self.as_str(normalize=True)

    @property
    def tag(self) -> str:
        '''
            Tag of the node.
        '''     
        return self.node.tag

    @property
    def children(self) -> Tuple['XmlNode']:
        '''
            All Children of this node as a Tuple of XmlNodes
        '''
        return (XmlNode(c) for c in list(self.node))

    @property
    def parent(self) -> 'XmlNode':
        '''
            Parent XmlNode
        '''
        return XmlNode(self.node.getparent())

    @property
    def preceding_sibling(self) -> 'XmlNode':
        '''
            The XmlNode before this node at same hierarchial level.
        '''
        return XmlNode(self.node.getprevious())

    @property
    def following_sibling(self) -> 'XmlNode':
        '''
            The XmlNode after this node at same hierarchial level.
        '''
        return XmlNode(self.node.getnext())

    @property
    def attrs(self) -> CIStringDict:
        '''
            All Attributes of this node as a dictionary.
        '''
        return self.__attrs

    def attr(self, name) -> str:
        '''
            Value of an attribute of this node.
        '''
        return self.__attrs[name]

    @property
    def value(self) -> str:
        '''
            Value of an 'value' attribute of this node.
        '''
        return self.attr("value")

    def has_attr(self, name):
        '''
            Check if an attribute is present.
        '''
        return name in self.__attrs

    def __xpath(self, xpath):
        if not xpath.startswith("."):
            return "." + xpath
        else:
            return xpath

    def findall_with_xpath(self, xpath) -> List['XmlNode']:
        '''
            Find all XmlNodes that match an XPath.
        '''
        return [XmlNode(n) for n in self.node.xpath(self.__xpath(xpath))]

    def find_with_xpath(self, xpath, position=1):
        '''
            Find nth XmlNode that matches an XPath.

            Args:
                xpath: XPath string
                position: XPath index. Default is 1.
        '''
        try:
            all = self.findall_with_xpath(xpath)
            return all[position-1]
        except IndexError as e:
            raise Exception(f"No node match at position >>{position}<< for xpath >>{xpath}<< in xml >>{self}<<")

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
            try:
                nodes = list(locator.search_node(self.node))
            except:
                continue
            else:
                out.extend(nodes)
                if stop_when_matched:
                    if nodes:
                        break
        return out

    def find(self, *node_locators, strict: bool=False) -> 'XmlNode':
        '''
            Find first `XmlNode` that match one of more `NodeLocator` s.

            Args:
                *node_locators: One or more `NodeLocator` s

            Keyword Arguments:
                strict: If True, the call raises an exception if element is not found, else returns None
        '''
        matches = self.findall(*node_locators, stop_when_matched=True)
        if matches:
            return matches[0]
        else:
            if strict:
                raise Exception("Element could not be found with Node Locators: >><<".format([str(n) for n in node_locators]))
            else:
                return None

    def find_keyvalue_texts(self, key_locator, value_locator) -> Tuple[str, str]:
        '''
            Returns texts of first XmlNodes for a pair of `NodeLocator` s

            Args:
                key_locator: `NodeLocator` (for key)
                value_locator: First `NodeLocator` (for value)

            Returns:
                2-element tuple containing the text strings.
        '''
        key = self.find(key_locator).text
        value = self.find(value_locator).text
        return key,value

    def __str__(self):
        return self.as_str()

    def clone(self) -> 'XmlNode':
        '''
            Create a clone of this XmlNode object.
        '''
        return Xml.from_str(str(self))
        
class Xml:
    '''
        Helper class to create XmlNode objects.
    '''

    @classmethod
    def from_str(cls, xml_str):
        '''
            Create an `XmlNode` from a string.
        '''
        lenient_parser = etree.XMLParser(encoding='utf-8', recover=True)
        return XmlNode(etree.parse(StringIO(xml_str), lenient_parser))


    @classmethod
    def from_file(cls, file_path: str) -> XmlNode:
        '''
            Creates an `XmlNode` from file.

            Arguments:
                file_path: Absolute path of the json file.

            Returns:
                Arjuna's `XmlNode` object
        '''

        with open(file_path, 'r') as f:
            return cls.from_str(f.read())

    @classmethod
    def from_lxml_element(cls, element, clone=False) -> XmlNode:
        '''
            Create an `XmlNode` from an `lxml` element.

            Arguments:
                element: `lxml` element
        '''
        if clone:
            return XmlNode(element)
        else:
            return XmlNode(element).clone()

    @classmethod
    def node_locator(cls, *, tags: 'strOrSequence'=None, **attrs):
        '''
            Create a locator for finding an XML Node in an **XmlNode**.

            Keyword Arguments:
                tags: (Optional) Descendant tags for the node. Can be a string of single or multiple tags or a list/tuple of tags.
                **attrs: Arbitrary number of key value pairs representing attribute name and value.

            Raises:
                Exception: If neither tag nor an attribute is provided.

            Note:
                You can use tag and attributes in combination.

                Supports nested node finding.
        '''
        return NodeLocator(tags=tags, **attrs)