from lxml import etree, html

class XmlUtils:

    @classmethod
    def str(cls, nodes):
        if type(nodes) not in {list, tuple}:
            nodes = [nodes]
        return [etree.tostring(node, encoding=str) for node in nodes]

    @classmethod
    def findall(cls, node, *, tag=None, rxpath=True, **attrs):
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
        prefix = rxpath and ".//" or ""

        xpath = "{}{}{}".format(prefix, tag, attr_str)
        return node.xpath(xpath)

    @classmethod
    def find(cls, node, *, tag=None, rxpath=True, **attrs):
        matches = cls.findall(node, tag=tag, rxpath=rxpath, **attrs)
        if matches:
            return matches[0]
        else:
            return None
    

