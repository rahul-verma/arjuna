.. _locators_ext_node:

**Arjuna Advanced Locators: Node Definition Based Locators**
============================================================

Arjuna has a provision to define advanced combinational locator type. This provision replaces the need to hand-craft simple to medium complexity Xpaths and CSS Selectors.

Node Definition based locators are used to locate a GuiWidget based on an AND condition among the following when provided:
    - Full tag name(s) if specified as a single tag string, space separated string with multiple tags or a list of tags.
    - Full class name(s() if specified as a single class string, space separated string with multiple classes or a list of classes.
    - Attributes as key-value pairs of attribute name and Full or partial values depending on type of node locator.
    - Full or partial text content depending on type of node locator using **text**, **star_text** or **dot_text** key.
    - **use_xpath** key to enforce XPath generation instead of CSS Selector.

Following sections cover various node locators: **node**, **fnode** and **bnode** along with additional information. 

The difference is the way attribute content and text content is matched. Tags and classes are handled in the same manner for all.

.. _node_locator:

**node** Locator
----------------

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
-----------------------------------------------------------------------------------

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
-----------------------------------------------------------------------------------------

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
------------------------------

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
-----------------

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
-----------------

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
