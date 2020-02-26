
def xfinder(tag=None, rxpath=True, **attrs):
    from arjuna.interact.gui.auto.source.parser import SourceNode

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

    def wrapper(xml_node):
        return [SourceNode(n) for n in xml_node.xpath(xpath)]

    return wrapper