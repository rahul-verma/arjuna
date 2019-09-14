import re
import os
from lxml import etree, html
from io import StringIO

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

class ElementXMLSourceParser:

    def __init__(self, source, root_element="body"):
        print(source)
        self.__source = source
        parser = etree.HTMLParser(remove_comments=True)
        tree = etree.parse(StringIO(source), parser)
        if root_element == "body":
            body = tree.getroot().find('body')
            elem_node = list(body)[0]
        else:
            body = tree.getroot()
            elem_node = body
        print(etree.tostring(elem_node, encoding='unicode'))
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
        self.__full_source = source

        for child in list(elem_node): elem_node.remove(child)
        self.__self_source = ' '.join(etree.tostring(elem_node, encoding=str).splitlines())
        self.__self_source = re.sub(r"\s+", " ", self.__self_source)

    def get_tag_name(self):
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

    def get_root_source(self):
        return self.__self_source

    def get_inner_source(self):
        return self.__inner_html

    def get_full_source(self):
        return self.__full_source

    def get_text_content(self):
        return self.__text_content

    
