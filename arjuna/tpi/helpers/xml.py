from lxml import etree, html

class NodeLocator:
    
    def __init__(self, tag=None, **attrs):

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


class XmlNode:

    def __init__(self, node):
        self.__node = node

    @property
    def xml_node(self):
        return self.__node

    @property
    def text(self):
        return self.xml_node.text

    @property
    def texts(self):
        return self.xml_node.xpath("//text()")

    @property
    def tag(self):
        return self.xml_node.tag

    @property
    def children(self):
        return [XmlNode(c) for c in list(self.xml_node)]

    @property
    def parent(self):
        return XmlNode(self.xml_node.getparent())

    @property
    def preceding_sibling(self):
        return XmlNode(self.xml_node.getprevious())

    @property
    def following_sibling(self):
        return XmlNode(self.xml_node.getnext())

    @property
    def attrs(self):
        return dict(self.xml_node.attrib)

    def attr(self, name):
        return self.xml_node.get(name)

    def has_attr(self, name):
        return name in self.xml_node.attrib

    def __xpath(self, xpath):
        if not xpath.startswith("."):
            return "." + xpath
        else:
            return xpath

    def findall_with_xpath(self, xpath):
        return [XmlNode(n) for n in self.xml_node.xpath(self.__xpath(xpath))]

    def find_with_xpath(self, xpath, position=1):
        return self.findall_with_xpath(xpath)[position]

    def as_str(self):
        return etree.tostring(self.xml_node, encoding=str)

    def __str__(self):
        return self.as_str()

    def findall(self, *finders, stop_when_matched=False):
        out = []
        for finder in finders:
            nodes = finder.search_node(self.xml_node)
            out.extend(nodes)
            if stop_when_matched:
                if nodes:
                    break
        return out

    def find(self, *finders, stop_when_matched=False):
        matches = self.findall(*finders, stop_when_matched=stop_when_matched)
        if matches:
            return matches[0]
        else:
            return None

    def find_keyvalue_texts(self, key_finder, value_finder):
        key = self.find(key_finder).text
        value = self.find(value_finder).text
        return key,value