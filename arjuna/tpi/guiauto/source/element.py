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

from arjuna.tpi.tracker import track

from .base import SingleGuiEntitySource

@track("debug")
class GuiElementSource(SingleGuiEntitySource):
    '''
        Abstract Base class for GUI Source of a Singular GUI entity (**GuiPage** or **GuiElement**).

        Not meant to be directly constructed by a test author. Retrieve as:
        
            .. code-block:: python
                
                gui_element.source

        Args:
            raw_source: Raw XML source.
    '''

    def __init__(self, raw_source):
        super().__init__(raw_source, root_tag="body")
        self.__tag = None
        self.__raw_attrs = None
        self.__attributes = None

    @property
    def tag(self) -> str:
        '''
            Tag name.
        '''
        return self.__tag

    def _process_elem_node(self, elem_node):
        self.__tag = elem_node.tag
        self.__raw_attrs = elem_node.keys()
        self.__attributes = {k.lower():v for k,v in elem_node.items()}

    @property
    def attrs(self) -> dict:
        '''
            All attributes as a dictionary.
        '''
        return self.__raw_attrs

    def is_attr_present(self, attr) -> bool:
        '''
            Check if an attribute is present.

            Args:
                attr: Attribute name
        '''
        return attr in self.__attributes.keys()

    def get_attr_value(self, attr, optional=False) -> str:
        '''
            Get value of an attribute.

            Args:
                attr: Attribute name

            Keyword Args:
                optional: Set to True if this attribute is optional. Default is False.

            Raises:
                Exception if optional is False and attribute is not found.
        '''
        try:
            return self.__attributes[attr.lower()]
        except Exception as e:
            if optional:
                return None
            else:
                raise Exception("Attribute {} not found for element".format(attr))

    def get_value(self, optional=False):
        '''
            Get content of value attribute.

            Keyword Args:
                optional: Set to True if value attribute is optional. Default is False.

            Raises:
                Exception if optional is False and value attribute is not found.
        '''
        return self.get_attr_value("value")

