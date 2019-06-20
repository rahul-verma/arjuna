from arjuna.unitee.types.containers import *

def get_children_tags(xml_node):
    return [child.tag.lower() for child in list(xml_node)]

def has_child(xml_node, child_tag):
    return child_tag.lower() in get_children_tags(xml_node)

def convert_to_cidict(xml_node):
    return CIStringDict({child.tag:child for child in list(xml_node)})

def convert_attribs_to_cidict(xml_node):
    return CIStringDict({attr: value for attr, value in xml_node.attrib.items()})