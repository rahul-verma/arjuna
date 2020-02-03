'''
This file is a part of Arjuna
Copyright 2015-2020 Rahul Verma

Website: www.RahulVerma.net

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

  http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
'''

import re
import os
from lxml import etree, html
from io import StringIO
from collections import namedtuple

def process_child_html(in_str):
    processed = os.linesep.join([l for l in in_str.splitlines() if l.strip()])
    return "\t" + processed

def remove_empty_lines_from_string(in_str):
    return ' '.join([l.strip() for l in in_str.splitlines() if l.strip()])

def empty_or_none(in_str):
    if type(in_str) is str and not in_str.strip():
        return True
    else:
        return in_str is None

SourceContent = namedtuple('SourceContet', "all root inner text")

class ElementXMLSourceParser:

    def __init__(self, raw_source, root_element="body"):
        super().__init__()
        self.__raw_source = raw_source
        self.__root_element = root_element
        self.__fpaths = []
        self.__content = None

    @property
    def content(self):
        return self.__content

    def load(self):
        raw_source = self.__raw_source
        parser = etree.HTMLParser(remove_comments=True)
        tree = etree.parse(StringIO(raw_source), parser)
        if self.__root_element == "body":
            body = tree.getroot().find('body')
            elem_node = list(body)[0]
        else:
            body = tree.getroot()
            elem_node = body

        # print(etree.tostring(elem_node, encoding='unicode'))
        non_normalized_text_content = os.linesep.join(
            [
                remove_empty_lines_from_string(c.text)
                for c in elem_node.iter() 
                if not empty_or_none(c.text)
            ]).strip()

        non_normalized_inner_html = os.linesep.join([
            process_child_html(etree.tostring(c, encoding='unicode'))
            for c in list(elem_node.iterchildren())
            ])

        self.__tag = elem_node.tag
        self.__text_content = non_normalized_text_content
        self.__inner_html = non_normalized_inner_html
        self.__raw_attrs = elem_node.keys()
        self.__attributes = {k.lower():v for k,v in elem_node.items()}
        self.__full_source = raw_source

        for child in list(elem_node): elem_node.remove(child)
        self.__self_source = ' '.join(etree.tostring(elem_node, encoding=str).splitlines())
        self.__self_source = re.sub(r"\s+", " ", self.__self_source)

        self.__content = SourceContent(all=self.__full_source, root=self.__self_source, inner=self.__inner_html, text=self.__text_content)

    @property
    def tag(self):
        return self.__tag

    def get_attr_names(self):
        return self.__raw_attrs

    def is_attr_present(self, attr):
        return attr in self.__attributes.keys()

    def get_attr_value(self, attr_name, optional=False):
        try:
            return self.__attributes[attr_name.lower()]
        except Exception as e:
            if optional:
                return None
            else:
                raise Exception("Attribute {} not found for element".format(attr_name))

    def get_value(self, optional=False):
        return self.get_attr_value("value")

    def get_root_content(self):
        return self.__self_source

    def get_inner_content(self):
        return self.__inner_html

    def get_full_content(self):
        return self.__full_source

    def get_text_content(self):
        return self.__text_content

class MultiElementSource:

    def __init__(self):
        super().__init__()
        self.__instances = None

    def load(self, instances):
        self.__instances = instances

    def get_full_content(self):
        return os.linesep.join([e.source.content.all for e in self.__instances])

    def get_inner_content(self):
        return os.linesep.join([e.source.content.inner for e in self.__instances])

    def get_text_content(self):
        return os.linesep.join([e.source.content.root for e in self.__instances])

    def get_root_content(self):
        return os.linesep.join([e.source.content.root for e in self.__instances])

    def _get_root_content_as_list(self):
        return [e.source.content.root for e in self.__instances]

    def get_tag_names(self):
        return [e.source.tag for e in self.__instances]

    def get_text_contents(self):
        return [e.source.get_text_content() for e in self.__instances]

    def get_values(self):
        return [e.source.get_attr_value("value") for e in self.__instances]

    def get_attr_values(self, attr):
        return [e.source.get_attr_value(attr) for e in self.__instances]

class FrameSource:

    def __init__(self, frame):
        super().__init__()
        self.__frame = frame
        self.__root_source = None
        self.__html_source = None

    def set_root_source(self, src):
        '''
        Once frame switch takes place, this source can not be got. Hence needs to happen
        explicitly at the time of wrapped element finding.
        '''
        self.__root_source = src

    def load(self):
        self.__frame.focus()
        self.__html_source = self.__frame._get_html_content_from_remote()

    def get_full_content(self):
        return self.get_root_content() + self.get_inner_content()

    def get_inner_content(self):
        return self.__html_source.get_full_content()

    def get_text_content(self):
        return self.__html_source.get_text_content()

    def get_root_content(self):
        return self.__root_source

