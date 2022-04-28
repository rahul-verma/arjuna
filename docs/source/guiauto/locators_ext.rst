.. _locators_ext:

**Arjuna's Locator Extensions**
===============================

Arjuna provides various higher level locator strategies in addition to wrapping Selenium's By-style strategies. 

All of Arjuna's locator extensions can be externalizd in GNS as well.

Following sections discuss these extensions:

**title** Locator
-----------------
It is used to locate a GuiWidget based on content of its **title** attribute.

**Coded**

.. code-block:: python

    # Using title locator. Full content of title attribute should be specified.   
    app.element(title="Password Lost and Found")

**GNS**

Externalization uses a simple format with **title** as key and value as the title content.

.. code-block:: yaml

    lost_pass_title:
        title: Password Lost and Found

**value** Locator
-----------------
It is used to locate a GuiWidget based on content of its **value** attribute.

**Coded**

.. code-block:: python

    # Using value locator. Full content of value attribute should be specified.      
    app.element(value="Log In")

**GNS**

Externalization uses a simple format with **value** as key and value as content of **value** attribute.

.. code-block:: yaml

    user_value:
        value: Log In


**tags** Locator
----------------

This is used to locate a GuiWidget based on a sequence of tags representing a sequence of descendants.

**Coded**

.. code-block:: python

    # Value can be a string containing space separated tags.
    app.element(tags="html body form")

    # Value can also be supplied as a list/tuple of tags.
    app.element(tags=("html", "body", "form"))

**GNS**

This locator can externalized in multiple formats based on whether you specify single or multiple tags:
    - a single string with a single tag name
    - multiple space separated tag names
    - a list of tag names

.. code-block:: yaml
   
    tags_1:
        tags: form

    tags_2:
        tags: body form

    tags_3:
        tags: 
            - body 
            - form

When you use wildcard '*', you should use quotes around it for valid YAML:

.. code-block:: yaml

    tags_4:
        tags: 
            - body 
            - '*'

You can use **ANY** instead of specifying it as '*'.

.. code-block:: yaml

    tags_5:
        tags: 
            - body
            - ANY

**classes** Locator
-------------------

This is used to locate GuiWidget based on class(es) associated with it.

It supports compound classes (supplied as a single string or as multiple separate strings).

Order of provided classes does not matter.

**Coded**

.. code-block:: python

    # Value can be a string containing space separated CSS classes.
    app.element(classes="button button-large")

    # Value can also be supplied as a list/tuple of CSS classes.
    app.element(classes=("button", "button-large"))

**GNS**


This locator is externalized in multiple formats based on whether you specify single or multiple classes:
    - a single string with a single class name
    - multiple space separated class names
    - a list of class names

.. code-block:: yaml
   
    cls_1:
        classes: button-large

    cls_2:
        classes: button button-large

    cls_3:
        classes: 
            - button 
            - button-large


**point** Locator
-----------------
This is used to run a JavaScript to find the GuiWidget under an XY coordinate.

**Coded**

.. code-block:: python

    # Using point locator. Value should be a Point object with x and y coordinates specified.
    app.element(point=Point(1043, 458))

**GNS**

This locator is externalized as a YAML mapping with **x** and **y** keys.


.. code-block:: yaml

   labels:
   
    elem_xy:
        point:
            x: 1043
            y: 458


**js** Locator 
--------------
This is used to run the provided JavaScript and returns GuiWidget representing the element it returns.

**Coded**

.. code-block:: python

    # Using js locator. Value should be a string containing the JavaScript.
    app.element(js="return document.getElementById('wp-submit')")

**GNS**

Externalization uses a simple format with **js** as key and value as the JavaScript string.

.. code-block:: yaml

    elem_js:
        js: "return document.getElementById('wp-submit')"


**Text Based Locators**
-----------------------

Arjuna provides the following locators for locating based on text: (For more options on text matching see **node** locator.)

These are externalized as a single key-value pair with key as the locator name and value as the full or partial content based on the locator.

**text** Locator
----------------

It is used to locate a GuiWidget based on its PARTIAL text.

**Coded**


.. code-block:: python

    app.element(text="your")

**GNS**

.. code-block:: yaml

    lost_pass_text:
        text: Lost

**ftext** Locator
-----------------

It is used to locate a GuiWidget based on its FULL text.

**Coded**


.. code-block:: python

    # Using ftext locator. Full text is to be specified.
    app.element(ftext="Lost your password?")

**GNS**

.. code-block:: yaml

    lost_pass_ftext:
        ftext: "Lost your password?"

**btext** Locator
-----------------

It is used to locate a GuiWidget based on partial text match at BEGINNING of text.

**Coded**

.. code-block:: python

    # Using ftext locator. Full text is to be specified.
    app.element(btext="Lost")

**GNS**

.. code-block:: yaml

    lost_pass_ftext:
        btext: Lost your


**Attribute Based Locators**
----------------------------

Arjuna provides the following locators for locating based on a single attribute: (For more options on attribute matching see **node** locator.)

These are externalized as a single key-value pair with key as the attribute name and value as the full or partial content attribute based on the locator.

.. note::

    For usage in Code, if the attribut name is a Python keyword, prefix it with '__' (two underscores). Arjuna removes this prefix and processes the attribute name as expected.

    In GNS format, this can be done but is not needed as this conflict of name does not arise.

**attr** Locator 
----------------

It is used to locate a GuiWidget based on PARTIAL content of a specific attribute.

**Coded**

.. code-block:: python

    # Here the size attribute is 230
    app.element(attr=attr(size=3))

    # Here the 'for' attribute contains the value 'user_login'. Partial content can be passed.
    app.element(attr=attr(__for='er_l'))

**GNS**

.. code-block:: yaml

    user_attr_1:
        attr:
            size: 3

    # No need for underscores if the attribute name conflicts with a Python keyword
    user_attr_2:
        attr:
            for: _login


**fattr** Locator 
-----------------

It is used to locate a GuiWidget based on FULL content of a specific attribute.

**Coded**


.. code-block:: python

    # Here the size attribute is 230
    app.element(fattr=attr(size=230))

    # Here the 'for' attribute contains the value 'user_login'. Full content should be passed.
    app.element(fattr=attr(__for="user_login"))

**GNS**

.. code-block:: yaml

    user_attr_1:
        fattr:
            size: 230

    # No need for underscores if the attribute name conflicts with a Python keyword
    user_attr_2:
        fattr:
            for: user_login


**battr** Locator 
-----------------

It is used to locate a GuiWidget based on partial content at BEGINNING of a specific attribute.

**Coded**

.. code-block:: python

    # Here the size attribute is 230
    app.element(battr=attr(size=2))

    # Here the 'for' attribute contains the value 'user_login'.
    app.element(battr=attr(__for="user_"))

**GNS**

.. code-block:: yaml

    user_attr_1:
        battr:
            size: 2

    # No need for underscores if the attribute name conflicts with a Python keyword
    user_attr_2:
        battr:
            for: user_


**eattr** Locator 
-----------------

It is used to locate a GuiWidget based on partial content at END of a specific attribute.

**Coded**

.. code-block:: python

    # Here the size attribute is 230
    app.element(eattr=attr(size=0))

    # Here the 'for' attribute contains the value 'user_login'.
    app.element(eattr=attr(__for="user_"))

**GNS**

.. code-block:: yaml

    user_attr_1:
        eattr:
            size: 0

    # No need for underscores if the attribute name conflicts with a Python keyword
    user_attr_2:
        eattr:
            for: _login

