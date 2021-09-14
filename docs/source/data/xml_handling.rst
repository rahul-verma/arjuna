.. _xml_handling:

**XML**
=======

XML is another popular format used for data exchange.

.. _xml_node:

**XmlNode**
-----------

A loaded full Xml or a part of it is represented using an :py:class:`XmlNode <arjuna.tpi.parser.xml.XmlNode>` object.

Creating an **XmlNode** Object
------------------------------

Arjuna's :py:class:`Xml <arjuna.tpi.parser.xml.Xml>` class provides various helper methods to easily create an XmlNode object from various sources:

    * **from_file**: Load XmlNode from a file.
    * **from_str**: Load XmlNode from a string.
    * **from_lxml_element**: From an `lxml` element.

The loaded object is returned as an `XmlNode`.


**Inquiring** an XmlNode Object
-------------------------------

**XmlNode** object provides the following properties for inquiry:

    * **node**: The underlying `lxml` element.
    * **text**: Unaltered text content. Text of all children is clubbed.
    * **normalized_text**: Text of this node with empty lines removed and individual lines trimmed.
    * **texts**: Texts returned as a sequence.
    * **inner_xml**: Xml of children.
    * **normalized_inner_xml**: Normalized inner XML of this node, with empty lines removed between children nodes.
    * **source**: String representation of this node's XML.
    * **normalized_source**: String representation of this node with all new lines removed and more than one conseuctive space converted to a single space.
    * **tag**: Tag name
    * **chidlren**: All Children of this node as a Tuple of XmlNodes
    * **parent**: Parent XmlNode
    * **preceding_sibling**: The XmlNode before this node at same hierarchial level.
    * **following_sibling**: The XmlNode after this node at same hierarchial level.
    * **attrs**: All attributes as a mapping.
    * **value**: Content of `value` attribute.


Following inquiry methods are available:
    * **attr**: Get value of an attribute by name.
    * **has_attr**: Check presence of an attribute.

**Cloning** an XmlNode Object
-----------------------------

You can clone an XmlNode by calling its **clone** method.


**Finding XmlNodes** in an XmlNode Object using **XPath**
---------------------------------------------------------

You can find XmlNodes in a given XmlNode object using XPath:

    * **find_with_xpath**: Find first match using XPath
    * **findall_with_xpath** Find all matches using XPath

**Finding XmlNodes** in an XmlNode Object using **XML.node_locator**
--------------------------------------------------------------------

Arjuna's **NodeLocator** object helps you in easily defining locating criteria.

    .. code-block:: python

        # XmlNode with tag input
        locator = Xml.node_locator(tags='input')

        # XmlNode with attr 'a' with value 1
        locator = Xml.node_locator(a=1)

        # XmlNode with tag input and attr 'a' with value 1
        locator = Xml.node_locator(tags='input', a=1)

.. note::
    'tags' can be provided as:

        * A string containing a single tag
        * A string containing multiple tags
        * A list/tuple containing multiple tags.

    When multiple tags are provided, they are treated as a sequential descendant tags.

    .. code-block:: python

        # XmlNode with tag input and attr 'a' with value 1
        locator = Xml.node_locator(tags='form input', a=1)
        locator = Xml.node_locator(tags=('form', 'input'), a=1)

You can search for all XMlNodes using this locator in an `XmlNode`:

    .. code-block:: python

        locator.search_node(node=some_xml_node)


For finer control, you can use finder methods in `XmlNode` object itself and provide the locator:

    * **find**: Find first match using XPath
    * **findall** Find all matches using XPath


    .. code-block:: python

        node.findall(locator)
        
        # Returns None if not found
        node.find(locator)

        # Raise Exception if not found
        node.find(locator, strict=True)


Providing **Alternative NodeLocators (OR Relationship)**
--------------------------------------------------------

In some situations, you might want to find **XmlNode(s)** which match any of the provided locators.

You can provide any number of locators in `XmlNode` finder methods.

    .. code-block:: python
        
        node.find(locator1, locator2, locator3)
        node.findall(locator1, locator2, locator3)


Exiting XmlNode.findall on **First Matched Locator**
----------------------------------------------------

You can stop `findall` logic at first matched locator by setting `stop_when_matched` to True:

    .. code-block:: python
        
        node.findall(locator1, locator2, locator3, stop_when_matched=True)
