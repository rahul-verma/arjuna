.. _text_parsing:


Parsing JSON, XML, HTML Files and Strings
=========================================

JSON, XML and HTML parsing is a very common need in test automation.

Arjuna provides its own objects to easy handle these content types in its helper classes in Tester Programming Interface. The corresponding objects are also returned by its other objects.


**JSON** (Javascript Object Notation)
-------------------------------------

Json is a popular format used in RESTful services and configurations.

Creating JSON Objects
^^^^^^^^^^^^^^^^^^^^^

Arjuna's :py:class:`Json <arjuna.tpi.helper.json.Json>` class provides with various helper methods to easily create a Json object from various sources:

    * **from_file**: Load Json from a file.
    * **from_str**: Load Json from a string.
    * **from_map**: Load Json from a mapping type object.
    * **from_iter**: Load Json from an iterable.
    * **from_object**: Load Json from a Python built-in data type object.

The loaded object is returned as one of the following:
    * :py:class:`JsonDict <arjuna.tpi.helper.json.JsonDict>`
    * :py:class:`JsonList <arjuna.tpi.helper.json.JsonList>`
    * If `allow_any` is set to True, then **from_file**, **from_str** and **from_object** calls return the same object as passed, if it is not a mapping or iterable.

Json Class Assertions
^^^^^^^^^^^^^^^^^^^^^

Json class provides the following assertions:

    * **assert_list_type**: Validate that the object is a JsonList or Python list
    * **assert_dict_type**: Validate that the object is a JsonDict or Python dict

Automatic Json Schema Extraction
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Given a Json object, you can extract its schema automatically:

    .. code-block:: python

        Json.extract_schema(jsonobject_or_str)

This schema can be used for schema validation for another Json object.

**JsonDict** Object
^^^^^^^^^^^^^^^^^^^

:py:class:`JsonDict <arjuna.tpi.helper.json.JsonDict>` encapsulates the Json dictionary and provides higher level methods for interaction.

It has the following properties:
    * **raw_object**: The underlying dictionary
    * **size**: Number of keys in the JsonDict
    * **schema**: The Json schema of this JsonDict (as a JsonSchema object)


Finding Json elements in a **JsonDict** Object
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

You can find Json elements in JsonDict by using a key name or by creating a more involved **JsonPath** query.

    * **find**: Find first match using a key or JsonPath
    * **findall** Find all matches using a JsonPath

Matching Schema of a **JsonDict** object
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

You can use a custom Json schema dictionary or a :py:class:`JsonSchema <arjuna.tpi.helper.json.JsonSchema>` object to validate schema of a **JsonDict** object.

    .. code-block:: python

        json_dict.matches_schema(schema)

It returns True/False depending on the match success.

Asserting **JsonDict** Object
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

**JsonDict** object provides various assertions to validate its contents:

    * **assert_contents**: Validate arbitary key-value pairs in its root.
    * **assert_keys_present**: Validate arbitrary keys
    * **assert_match**: Assert if it matches another Python dict or JsonDict.
    * **assert_schema** Assert if it matches provided schema dict or JsonSchema.
    * **assert_match_schema** Assert if it has the same schema as that of the provided dict or JsonDict.


**JsonList** Object
^^^^^^^^^^^^^^^^^^^

:py:class:`JsonList <arjuna.tpi.helper.json.JsonList>` encapsulates the Json list and provides higher level methods for interaction.

It has the following properties:
    * **raw_object**: The underlying dictionary
    * **size**: Number of keys in the JsonDict


**==** Operator with **JsonDict** and **JsonList** Objects
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

**==** operator is overridden for  **JsonDict** and **JsonList** objects.

JsonDict supports comparison with a JsonDoct or Python dict.

JsonList supports comparision with a JsonList or Python list.

    .. code-block:: python

        json_dict_1 == json_dict_2
        json_dict_1 == py_dict

        json_list_1 == json_list_2
        json_list_1 == py_list

Size Related Assertions in **JsonDict** and **JsonList** Objects
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

**JsonDict** and **JsonList** both extend the **IterableAsserterMixin** and hence provide the following size related assertions.

Note that size for JsonList means number of objects/elements in it and for JsonDict means number of keys in its root.

    * **assert_empty**: Validate that it is empty (size=0)
    * **assert_not_empty**: Validate size >= 1
    * **assert_size**: Validate size = provided size.
    * **assert_min_size**: Validate size >= provided size.
    * **assert_max_size**: Validate size <= provided size.
    * **assert_size_range**: Validate provided min size <= actual size <= provided max size

Modifying a **JsonSchema** object
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

**JsonSchema** object is primarily targeted to be created using auto-extraction using **Json.extract_schema**.

You can currently make two modifications to the **JsonSchema** once created:

    * **mark_optional**: Mark arbitrary keys as optional in the root of the schema.
    * **allow_null**: Allow `null` value for the arbitrary keys.

**XML**
-------

XML is another popular format used for data exchange.

Creating an **XmlNode** Object
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

A loaded full Xml or a part of it is represented using an :py:class:`XmlNode <arjuna.tpi.helper.xml.XmlNode>` object.

Arjuna's :py:class:`Xml <arjuna.tpi.helper.xml.Xml>` class provides various helper methods to easily create an XmlNode object from various sources:

    * **from_file**: Load XmlNode from a file.
    * **from_str**: Load XmlNode from a string.
    * **from_lxml_element**: From an `lxml` element.

The loaded object is returned as an `XmlNode`.


Inquiring an **XmlNode** Object
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

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

Cloning an **XmlNode** object
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

You can clone an XmlNode by calling its **clone** method.


Finding XmlNodes in an **XmlNode** Object using **XPath**
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

You can find XmlNodes in a given XmlNode object using XPath:

    * **find_with_xpath**: Find first match using XPath
    * **findall_with_xpath** Find all matches using XPath

Finding XmlNodes in an **XmlNode** Object using **NodeLocator**
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Arjuna's **NodeLocator** object helps you in easily defining locating criteria.

    .. code-block:: python

        # XmlNode with tag input
        locator = NodeLocator(tag='input')

        # XmlNode with attr 'a' with value 1
        locator = NodeLocator(a=1)

        # XmlNode with tag input and attr 'a' with value 1
        locator = NodeLocator(tag='input, a=1)


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


Providing Alternative **NodeLocators** (OR Relationship)
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

In some situations, you might want to find **XmlNode(s)** which match any of the provided locators.

You can provide any number of locators in `XmlNode` finder methods.

    .. code-block:: python
        
        node.find(locator1, locator2, locator3)
        node.findall(locator1, locator2, locator3)


Exiting **XmlNode.findall** on First Matched Locator
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

You can stop `findall` logic at first matched locator by setting `stop_when_matched` to True:

    .. code-block:: python
        
        node.findall(locator1, locator2, locator3, stop_when_matched=True)

**HTML**
--------

In Web UI automation and HTTP Automation, extracting data from and matching data are common needs.


Creating an **HtmlNode** Object
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

A loaded full HTML or a part of it is represented using an :py:class:`HtmlNode <arjuna.tpi.helper.html.HtmlNode>` object.

Arjuna's :py:class:`Html <arjuna.tpi.helper.xml.Html>` class provides various helper methods to easily create an HtmlNode object from various sources:

    * **from_file**: Load HtmlNode from a file.
    * **from_str**: Load HtmlNode from a string.
    * **from_lxml_element**: Load HtmlNode from an `lxml` element.


Arjuna uses BeautifulSoup based lxml parser to fix broken HTML while loading.

Loading Partial HTML
^^^^^^^^^^^^^^^^^^^^

While using **from_file** or **from_file** methods of `Html` object, you can load pass partial HTML content to be loaded as an `HtmlNode`

For this provide **partial=True** as the keyword argument.

    .. code-block:: python

        node = Html.from_str(partial_html_str, partial=True)

An `HtmlNode` is an `XmlNode`
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

As the `HtmlNode` inherits from `XmlNode`, it supports all properties, methods and flexbilities that are discussed above for `XmlNode` object.

Additionally, it has the following properties:

    * **inner_html**: HTML of children.
    * **normalized_inner_html**: Normalized inner HTML of this node, with empty lines removed between children nodes.






