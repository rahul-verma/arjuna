.. _html_handling:

**HTML**
========

In Web UI automation and HTTP Automation, extracting data from and matching data are common needs.


Creating an **HtmlNode** Object
-------------------------------

A loaded full HTML or a part of it is represented using an :py:class:`HtmlNode <arjuna.tpi.parser.html.HtmlNode>` object.

Arjuna's :py:class:`Html <arjuna.tpi.parser.xml.Html>` class provides various helper methods to easily create an HtmlNode object from various sources:

    * **from_file**: Load HtmlNode from a file.
    * **from_str**: Load HtmlNode from a string.
    * **from_lxml_element**: Load HtmlNode from an `lxml` element.


Arjuna uses BeautifulSoup based lxml parser to fix broken HTML while loading.

Loading Partial HTML
--------------------

While using **from_file** or **from_file** methods of `Html` object, you can load pass partial HTML content to be loaded as an `HtmlNode`

For this provide **partial=True** as the keyword argument.

    .. code-block:: python

        node = Html.from_str(partial_html_str, partial=True)

**An HtmlNode IS an XmlNode**
-----------------------------

As the `HtmlNode` inherits from :ref:`xml_node`, it supports all properties, methods and flexbilities that are discussed for :ref:`xml_node` object in :ref:`xml_handling` documentation.

Additionally, it has the following properties:

    * **inner_html**: HTML of children.
    * **normalized_inner_html**: Normalized inner HTML of this node, with empty lines removed between children nodes.






