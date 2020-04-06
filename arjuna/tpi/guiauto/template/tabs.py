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

# from .base_element import ElementConfig

# class Tab:

#     def __init__(self, automator, label_elem, content_relation_attr, content_relation_type):
#         super().__init__(automator, parent)
#         self.__label_elem = label_elem
#         self.__tab_group = tab_group
#         self.__label = label_elem.text

#         # Find an element based on content of attribute that ties a tab label to content that it controls.
#         attr_value = label_elem.get_attr_value(content_relation_attr)
#         with_obj = getattr(With, content_relation_type.name.lower())(attr_value)

#         self.__tab_content_emd = self.__automator.create_emd(with_obj)
#         self.__tab_content = None

#     @property
#     def label(self):
#         return self.__name

#     def click(self):
#         self.__label_elem.click()
#         self.__tab_content = self.__tab_grouptab_group.root.element(self.__tab_content_emd)

#     def element(self, *with_locators):
#         self.__content.element(*with_locators)


# class TabGroup(ElementConfig):

#     def __init__(self, automator, emd, *, tab_header_emd, content_relation_attr, content_relation_type, parent=None):
#         super().__init__(automator)
#         self.__root = automator.define_element(emd)
#         tabs = self.root.define_element(tab_header_emd).identify()
#         self.__tabs = []
#         for i in range(tabs.length):
#             self.__tabs.append(Tab(self, tabs.at_index(i), content_relation_attr, content_relation_type))

#     @property
#     def root(self):
#         return self.__root

#     @property
#     def labels(self):
#         return [t.label for t in self.__tabs]
