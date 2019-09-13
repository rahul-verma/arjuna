import re
import os
from lxml import etree, html
from io import StringIO

def process_child_html(in_str):
    processed = os.linesep.join([l for l in in_str.splitlines() if l.strip()])
    return "\t" + processed

class ElementXMLSourceParser:

    def __init__(self, source):
        self.__source = source
        parser = etree.HTMLParser()
        tree = etree.parse(StringIO(source), parser)
        body = tree.getroot().find('body')
        elem_node = list(body)[0]
        non_normalized_text_content = ' '.join(
            [
                ' '.join(c.text.splitlines()) 
                for c in elem_node.iter() 
                if c.text is not None
            ]).strip()

        non_normalized_inner_html = os.linesep.join([
            process_child_html(etree.tostring(c, encoding='unicode'))
            for c in list(elem_node.iterchildren())
            ])

        self.__tag = elem_node.tag
        self.__text_content = re.sub(r"\s+" , " ", non_normalized_text_content)
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

    def get_source(self):
        return self.__self_source

    def get_inner_source(self):
        return self.__inner_html

    def get_full_source(self):
        return self.__full_source

    def get_text_content(self):
        return self.__text_content

    
