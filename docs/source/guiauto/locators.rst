.. _locators:

**GuiWidget Locators**
======================

.. _basic_locators:

**Basic Locators**
------------------

Following are the basic locators supported and corresponding Selenium **By** locators.

The locator strategy in GNS files is expressed using locator type names supported by Arjuna. These are simple locators and hence are expressed as basic key value pairs, almost equivalent to the way you pass them as keyword arguments in **app.element** calls. Functionality is equivalent as well.

**id** Locator
^^^^^^^^^^^^^^

Locates a GuiWidget by the content of its **id** attribute.

**Coded**

.. code-block:: python

   app.element(id="user_login")

**GNS**

.. code-block:: yaml

    user_id:
        id: user_login

**name** Locator
^^^^^^^^^^^^^^^^

Locates a GuiWidget by the content of its **name** attribute.

**Coded**

.. code-block:: python

   app.element(name="log")

**GNS**

.. code-block:: yaml

    user_name:
        name: log

**tags** Locator
^^^^^^^^^^^^^^^^

Locates a GuiWidget by the content of its tag name. For more advanced usage, see :ref:`locator_exts`.

**Coded**


.. code-block:: python

   app.element(tags="input")

**GNS**

.. code-block:: yaml

    user_tag:
        tags: input


**classes** Locator
^^^^^^^^^^^^^^^^^^^

Locates a GuiWidget by a class name contained in its class attribute. For more advanced usage, see :ref:`locator_exts`.

**Coded**


.. code-block:: python

   app.element(classes="cls")

**GNS**

.. code-block:: yaml

    user_class:
        classes: input

**link** Locator
^^^^^^^^^^^^^^^^^^^

Locates a GuiWidget by its PARTIAL link text.

.. code-block:: python

   app.element(link="password")

**GNS**

.. code-block:: yaml

    lost_pass_link:
        link: password

**flink** Locator
^^^^^^^^^^^^^^^^^

Locates a GuiWidget by its FULL link text.

**Coded**

.. code-block:: python

   app.element(flink="Lost your password?")

**GNS**

.. code-block:: yaml

    lost_pass_flink:
        flink: "Lost your password?"


**xpath** Locator
^^^^^^^^^^^^^^^^^

Locates a GuiWidget by the specifield XML Path (xpath).

**Coded**

.. code-block:: python

   app.element(xpath="//*[contains(text(), 'Lost')]")

**GNS**

.. code-block:: yaml

    lost_pass_text_content:
        xpath: "//*[contains(text(), 'Lost')]"


**selector** Locator
^^^^^^^^^^^^^^^^^^^^

Locates a GuiWidget by the specifield CSS Selector.

**Coded**

.. code-block:: python

   app.element(selector=".button.button-large")
   
**GNS**

.. code-block:: yaml

    button_compound_class:
        selector: ".button.button-large"

.. _locator_exts:

**Arjuna's Locator Extensions**
-------------------------------

Arjuna provides various higher level locator strategies in addition to wrapping Selenium's By-style strategies. 

All of Arjuna's locator extensions can be externalizd in GNS as well.

Following sections discuss these extensions:

**title** Locator
^^^^^^^^^^^^^^^^^
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
^^^^^^^^^^^^^^^^^
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
^^^^^^^^^^^^^^^^

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
^^^^^^^^^^^^^^^^^^^
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
^^^^^^^^^^^^^^^^^
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
^^^^^^^^^^^^^^
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
^^^^^^^^^^^^^^^^^^^^^^^

Arjuna provides the following locators for locating based on text: (For more options on text matching see **node** locator.)

These are externalized as a single key-value pair with key as the locator name and value as the full or partial content based on the locator.

**text** Locator
""""""""""""""""

It is used to locate a GuiWidget based on its PARTIAL text.

**Coded**


.. code-block:: python

    app.element(text="your")

**GNS**

.. code-block:: yaml

    lost_pass_text:
        text: Lost

**ftext** Locator
"""""""""""""""""
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
"""""""""""""""""
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
^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Arjuna provides the following locators for locating based on a single attribute: (For more options on attribute matching see **node** locator.)

These are externalized as a single key-value pair with key as the attribute name and value as the full or partial content attribute based on the locator.

.. note::

    For usage in Code, if the attribut name is a Python keyword, prefix it with '__' (two underscores). Arjuna removes this prefix and processes the attribute name as expected.

    In GNS format, this can be done but is not needed as this conflict of name does not arise.

**attr** Locator 
""""""""""""""""

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
"""""""""""""""""

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
"""""""""""""""""

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
"""""""""""""""""
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


**Node Definition Based Locators**
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Arjuna has a provision to define advanced combinational locator type. This provision replaces the need to hand-craft simple to medium complexity Xpaths and CSS Selectors.

Node Definition based locators are used to locate a GuiWidget based on an AND condition among the following when provided:
    - Full tag name(s) if specified as a single tag string, space separated string with multiple tags or a list of tags.
    - Full class name(s() if specified as a single class string, space separated string with multiple classes or a list of classes.
    - Attributes as key-value pairs of attribute name and Full or partial values depending on type of node locator.
    - Full or partial text content depending on type of node locator using **text**, **star_text** or **dot_text** key.
    - **use_xpath** key to enforce XPath generation instead of CSS Selector.

Following sections cover various node locators: **node**, **fnode** and **bnode** along with additional information. 

The difference is the way attribute content and text content is matched. Tags and classes are handled in the same manner for all.

**node** Locator
""""""""""""""""

Matches attributes and text partially. Tags and Classes are expected to be provided exactly as in HTML.

**Coded**

.. code-block:: python

    # Here a HTML element with tag input is targeted which has id=user_login and size=20. Partial content can be passed.
    app.element(node=node(tags="input", id="_login", size=20))

    # Sometimes names of attributes conflict with Python keywords. 
    # In such a case attribute name can be preceded with '__' (two underscores.)
    app.element(node=node(__for="_login", tags="label", size=20))

    # You can also pass a dictionary of attributes
    app.element(node=node(tags="label", size=20, attrs={'for': '_login'}))
    app.element(node=node(tags="label", size=20, attrs={'__for': '_login'}))

.. note::

    In situations where the same attribute name is present in multiple places in the call, following sequence determines what value is finally retained for such an attribute:
        * First the **attrs** dictionary is processed
        * Then, the attributes passed as direct keyword arguments are processed.

**GNS**

.. code-block:: yaml

    n1:
        node:
            tags: label
            size: 20
            for: _login


**Text Specification**: Understanding **text**, **star_text** and **dot_text** Keys
"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""

You can specify the partial text of a node using the **text** key:

**Coded**

.. code-block:: python

    # You can also use partial text content for matching
    app.element(node=node(tags="a", text="your password", title="Found"))


**GNS**

.. code-block:: yaml

    n1:
        node:
            tags: a
            text: your password
            title: Found

Sometimes the HTML/DOM structure contains elements within the text node and hence interferes with the text match. Instead of using **text** key, you can also use the following:
    * **star_text**: It translates to '*//text()' instead of 'text()' in generated XPath. It can also be represented as '*text' in **attrs** dict argument or in gns.
    * **dot_text**: It translates to '.' instead of 'text()' in generated XPath. It can also be represented as '.text' in **attrs** dict argument or in gns.

**Coded**

.. code-block:: python

    # Using node with star_text
    app.element(node=node(star_text="Me"))

    app.element(node=node(attrs={'*text' : "Me"}))

    # Using node with dot_text
    e = app.element(node=node(tags="form", dot_text="Me"))
    print(e.source.content.root)

    e = app.element(node=node(tags="form", attrs={'.text' : "Me"}))
    print(e.source.content.root)

**GNS**

.. code-block:: yaml

    n1:
        node:
            star_text: Me

    n2:
        node:
            '*text': Me

    n3:
        node:
            tags: form
            dot_text: Me

    n4:
        node:
            tags: form
            '.text': Me

.. note::

    You can specify only one out of **text**, **star_text** and **dot_text** keys. They can not be used together in a single node specification.

Specifying **Multiple Tags** and **Multiple Classes** using **tags** and **classes** Keys
"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""

You can specify multiple tags as well as classes. The behavior is just like their usage as individual locators except the fact that here they are used in combination with other conditions.

**Coded**


.. code-block::

    # As space separated strings
    app.element(node=node(tags="html body", classes="locale-en-us wp-core-ui")))

    # As tuples. Can also use lists.
    app.element(node=node(tags=("html", "body"), classes=("locale-en-us", "wp-core-ui"))))

**GNS**

.. code-block:: yaml

    n1:
        node:
            tags: html body
            classes: 
                - locale-en-us 
                - wp-core-ui

    n2:
        node:
            tags: html body
            classes: 
                - locale-en-us 
                - wp-core-ui


**Enforcing XPath Generation**
""""""""""""""""""""""""""""""

The Node Definition Locators like **node** are translated to a CSS Selector or an XPath by Arjuna.

If no text is specified using **text**, **star_text** or **dot_text** keys, Arjuna generates a CSS Selector rather than an XPath.

For example, consider the following situation in Coded and GNS format:

**Coded**

.. code-block:: python

    app.element(node=node(tags="html *", classes=("locale-en-us", "wp-core-ui")))

**GNS**

.. code-block:: yaml

    n1:
        node:
            tags: html *
            classes: 
                - locale-en-us 
                - wp-core-ui

As in the above situation, no text related keys are specified, following CSS Selector is generated:

.. code-block:: text

    html *.locale-en-us.wp-core-ui

To enforce XPath generation instead of a CSS Selector, you can pass **use_xpath** key as True.

**Coded**

.. code-block:: python

    app.element(node=node(use_xpath=True, tags="html *", classes=("locale-en-us", "wp-core-ui")))

**GNS**

.. code-block:: yaml

    n1:
        node:
            tags: html *
            classes: 
                - locale-en-us 
                - wp-core-ui
            use_xpath: True

As **use_xpath** is set to True, Arjuna generates the following XPath:

.. code-block:: text

    //html//*[contains(@class,'locale-en-us') and contains(@class,'wp-core-ui')]

**fnode** Locator
"""""""""""""""""

Matches FULL content of attributes and text. Tags and Classes are also expected to be provided exactly as in HTML.

Code usage is same as that of **node** locator. Following is a sample:

**Coded**

.. code-block:: python

    app.element(fnode=node(tags="a", text="Lost your password?", title="Password Lost and Found"))

**GNS**

.. code-block:: yaml

    n1:
        fnode:
            tags: a
            text: "Lost your password?"
            title: Password Lost and Found

**bnode** Locator
"""""""""""""""""

Matches partial content at BEGINNING of attributes and text. Tags and Classes are expected to be provided exactly as in HTML.

Code usage is same as that of **node** locator. Following is a sample:

**Coded**

.. code-block:: python

    # You can also partial text content at beginning for matching
    app.element(bnode=node(tags="a", text="Lost", title="Password Lost"))

**GNS**

.. code-block:: yaml

    n1:
        fnode:
            tags: a
            text: Lost
            title: Password Lost
