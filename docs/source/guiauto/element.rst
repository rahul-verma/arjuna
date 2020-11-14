.. _element:

**Element Identification and Interaction**
==========================================

**GuiElement and Widgets**
--------------------------

Arjuna's Gui automation implementation has different types of Gui Widgets which are associated with corresponding Widget types.

A single node in the DOM of a web UI is represented by a **GuiElement** object in Arjuna, irrespective of its type. This is unless you need specialized methods which we will see later.

The Widget type for **GuiElement** is **element**. This information is not important here, but will become relevant when we deal with more complex node types.

All locators discussed here can be used for any type of Gui Widgets.

.. _locators:

Basic Locators
--------------

Arjuna supports the locators which are supported by Selenium's By object. Apart from these, there are various abstracted locators which Arjuna provides for easier coding.

For locating **GuiElement**, you can use the **.element** factory method (assume **app** is the **GuiApp** object):

.. code-block:: python

   app.element(<locator_type>=<locator_value>)

The locator strategy is expressed using locator type names supported by Arjuna. You can pass it as a keyword argument **k=v** format to the the **element** call. 

Following are the basic locators supported and corresponding Selenium **By** locators:

**id** Locator
^^^^^^^^^^^^^^

Locates a GuiWidget by the content of its **id** attribute.

.. code-block:: python

   wordpress.element(id="user_login")

**name** Locator
^^^^^^^^^^^^^^^^

Locates a GuiWidget by the content of its **name** attribute.

.. code-block:: python

   wordpress.element(name="log")

**tags** Locator
^^^^^^^^^^^^^^^^

Locates a GuiWidget by the content of its tag name. For more advanced usage, see :ref:`coded_locator_exts`.

.. code-block:: python

   wordpress.element(tags="input")


**classes** Locator
^^^^^^^^^^^^^^^^^^^

Locates a GuiWidget by a class name contained in its class attribute. For more advanced usage, see :ref:`coded_locator_exts`.

.. code-block:: python

   wordpress.element(classes="cls")


**link** Locator
^^^^^^^^^^^^^^^^^^^

Locates a GuiWidget by its partial link text.

.. code-block:: python

   wordpress.element(link="password")


**flink** Locator
^^^^^^^^^^^^^^^^^

Locates a GuiWidget by its full link text.

.. code-block:: python

   wordpress.element(flink="Lost your password?")


**xpath** Locator
^^^^^^^^^^^^^^^^^

Locates a GuiWidget by the specifield XML Path (xpath).

.. code-block:: python

   wordpress.element(xpath="//*[contains(text(), 'Lost')]")


**selector** Locator
^^^^^^^^^^^^^^^^^^^^

Locates a GuiWidget by the specifield CSS Selector.

.. code-block:: python

   wordpress.element(selector=".button.button-large")
   

**Alternative Locators** - Specifying Multiple Locators with **OR Relationship**
--------------------------------------------------------------------------------

You can also pass multiple locators as arugment in **element** calls. 

Arjuna will try all of these one by one in a dynamic wait mechanism. The total maximum wait time does not add up, it remains same as that for using a single identifier.

.. code-block:: python

   wordpress.element(tags="input", classes="someclass")

.. _coded_locator_exts:

**Arjuna's Locator Extensions**
-------------------------------

Arjuna provides various higher level locator strategies in addition to wrapping Selenium's By-style strategies. 

Following sections discuss these extensions:

**title** Locator
^^^^^^^^^^^^^^^^^
It is used to locate a GuiWidget based on content of its **title** attribute.

.. code-block:: python

    # Using title locator. Full content of title attribute should be specified.   
    wordpress.element(title="Password Lost and Found")

**value** Locator
^^^^^^^^^^^^^^^^^
It is used to locate a GuiWidget based on content of its **value** attribute.

.. code-block:: python

    # Using value locator. Full content of value attribute should be specified.      
    wordpress.element(value="Log In")

**tags** Locator
^^^^^^^^^^^^^^^^

This is used to locate a GuiWidget based on a sequence of tags representing a sequence of descendants.

.. code-block:: python

    # Value can be a string containing space separated tags.
    wordpress.element(tags="html body form")

    # Value can also be supplied as a list/tuple of tags.
    wordpress.element(tags=("html", "body", "form"))


**classes** Locator
^^^^^^^^^^^^^^^^^^^
This is used to locate GuiWidget based on class(es) associated with it.

Supports compound classes (supplied as a single string or as multiple separate strings)

.. code-block:: python

    # Value can be a string containing space separated CSS classes.
    wordpress.element(classes="button button-large")

    # Value can also be supplied as a list/tuple of CSS classes.
    wordpress.element(classes=("button", "button-large"))


**point** Locator
^^^^^^^^^^^^^^^^^
This is used to run a JavaScript to find the GuiWidget under an XY coordinate.

.. code-block:: python

    # Using point locator. Value should be a Point object with x and y coordinates specified.
    wordpress.element(point=Point(1043, 458))


**js** Locator 
^^^^^^^^^^^^^^
This is used to run the provided JavaScript and returns GuiWidget representing the element it returns.

.. code-block:: python

    # Using js locator. Value should be a string containing the JavaScript.
    wordpress.element(js="return document.getElementById('wp-submit')")

**Text Based Locators**
^^^^^^^^^^^^^^^^^^^^^^^

Arjuna provides the following locators for locating based on text: (For more options on text matching see **node** locator.)

**text** Locator
""""""""""""""""

It is used to locate a GuiWidget based on its partial text.

.. code-block:: python

    wordpress.element(text="your")

**ftext** Locator
"""""""""""""""""
It is used to locate a GuiWidget based on its full text.

.. code-block:: python

    # Using ftext locator. Full text is to be specified.
    wordpress.element(ftext="Lost your password?")

**btext** Locator
"""""""""""""""""
It is used to locate a GuiWidget based on partial text match at beginning of text.

.. code-block:: python

    # Using ftext locator. Full text is to be specified.
    wordpress.element(btext="Lost")

**Attribute Based Locators**
^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Arjuna provides the following locators for locating based on a single attribute: (For more options on attribute matching see **node** locator.)

.. note::

    If the attribut name is a Python keyword, prefix it with '__' (two underscores). Arjuna removes this prefix and processes the attribute name as expected.

**attr** Locator 
""""""""""""""""

It is used to locate a GuiWidget based on partial content of a specific attribute.

.. code-block:: python

    # Here the size attribute is 230
    wordpress.element(attr=attr(size=3))

    # Here the 'for' attribute contains the value 'user_login'. Partial content can be passed.
    wordpress.element(attr=attr(__for='er_l'))

**fattr** Locator 
"""""""""""""""""

It is used to locate a GuiWidget based on full content of a specific attribute.

.. code-block:: python

    # Here the size attribute is 230
    wordpress.element(fattr=attr(size=20))

    # Here the 'for' attribute contains the value 'user_login'. Full content should be passed.
    wordpress.element(fattr=attr(__for="user_login"))


**battr** Locator 
"""""""""""""""""

It is used to locate a GuiWidget based on partial content at beginning of a specific attribute.

.. code-block:: python

    # Here the size attribute is 230
    wordpress.element(fattr=attr(size=2))

    # Here the 'for' attribute contains the value 'user_login'.
    wordpress.element(battr=attr(__for="user_"))


**eattr** Locator 
"""""""""""""""""
It is used to locate a GuiWidget based on partial content at end of a specific attribute.

.. code-block:: python

    # Here the size attribute is 230
    wordpress.element(eattr=attr(size=0))

    # Here the 'for' attribute contains the value 'user_login'.
    wordpress.element(eattr=attr(__for="user_"))


**Node Definition Based Locators**
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Arjuna has a provision to define advanced combinational locator type. This provision replaces the need to hand-craft simple to medium complexity Xpaths and CSS Selectors.

Node Definition based locators are used to locate a GuiWidget based on an AND condition among the following when provided:
    - Content of one or more attributes 
    - Text Content
    - Descendant Tag Sequence
    - One or more associated class names

Following sections cover various node locators: **node**, **fnode** and **bnode** along with additional information. The difference is the way attribute content and text content is matched. Tags and classes are handled in the same manner for all.

**node** Locator
""""""""""""""""

Matches attributes and text partially. Tags and Classes are expected to be provided exactly as in HTML.

.. code-block:: python

    # Here a HTML element with tag input is targeted which has id=user_login and size=20. Partial content can be passed.
    wordpress.element(node=node(tags="input", id="_login", size=20))

    # Sometimes names of attributes conflict with Python keywords. 
    # In such a case attribute name can be preceded with '__' (two underscores.)
    wordpress.element(node=node(__for="_login", tags="label", size=20))

    # You can also pass a dictionary of attributes
    wordpress.element(node=node(tags="label", size=20, attrs={'for': '_login'}))
    wordpress.element(node=node(tags="label", size=20, attrs={'__for': '_login'}))

.. note::

    In situations where the same attribute name is present in multiple places in the call, following sequence determines what value is finally retained for such an attribute:
        * First the **attrs** dictionary is processed
        * Then, the attributes passed as direct keyword arguments are processed.

**Text Specification**: Understanding **text**, **star_text** and **dot_text** Keys
"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""

You can specify the partial text of a node using the **text** key:

.. code-block:: python

    # You can also use partial text content for matching
    wordpress.element(node=node(tags="a", text="your password?", title="Found"))

Sometimes the HTML/DOM structure contains elements within the text node and hence interferes with the text match. Instead of using **text** key, you can also use the following:
    * **star_text**: It translates to '*//text()' instead of 'text()' in generated XPath. It can also be represented as '*text' in **attrs** dict argument or in gns.
    * **dot_text**: It translates to '.' instead of 'text()' in generated XPath. It can also be represented as '.text' in **attrs** dict argument or in gns.

.. code-block:: python

    # Using node with star_text
    wordpress.element(node=node(star_text="Me"))

    wordpress.element(node=node(attrs={'*text' : "Me"}))

    # Using node with dot_text
    e = wordpress.element(node=node(tags="form", dot_text="Me"))
    print(e.source.content.root)

    e = wordpress.element(node=node(tags="form", attrs={'.text' : "Me"}))
    print(e.source.content.root)


.. note::

    You can specify only one out of **text**, **star_text** and **dot_text** keys. They can not be used together in a single node specification.

Specifying **Multiple Tags** and **Multiple Classes** using **tags** and **classes** Keys
"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""

You can specify multiple tags as well as classes. The behavior is just like their usage as individual locators except the fact that here they are used in combination with other conditions.

.. code-block::

    # As space separated strings
    wordpress.element(node=node(tags="html body", classes="locale-en-us wp-core-ui")))

    # As tuples. Can also use lists.
    wordpress.element(node=node(tags=("html", "body"), classes=("locale-en-us", "wp-core-ui"))))

**Enforcing XPath Generation**
""""""""""""""""""""""""""""""

The Node Definition Locators like **node** are translated to a CSS Selector or an XPath by Arjuna.

If no text is specified using **text**, **star_text** or **dot_text** keys, Arjuna generates a CSS Selector rather than an XPath.

For example, consider the following situation:

.. code-block:: python

    wordpress.element(node=node(tags="html *", classes=("locale-en-us", "wp-core-ui")))

As in the above situation, no text related keys are specified, following CSS Selector is generated:

.. code-block:: text

    html *.locale-en-us.wp-core-ui

To enforce XPath generation instead of a CSS Selector, you can pass **use_xpath** key as True.

.. code-block:: python

    wordpress.element(node=node(use_xpath=True, tags="html *", classes=("locale-en-us", "wp-core-ui")))

As **use_xpath** is set to True, Arjuna generates the following XPath:

.. code-block:: text

    //html//*[contains(@class,'locale-en-us') and contains(@class,'wp-core-ui')]


**fnode** Locator
"""""""""""""""""

Matches full content of attributes and text. Tags and Classes are also expected to be provided exactly as in HTML.

Code usage is same as that of **node** locator. Following is a sample:

.. code-block:: python

    # You can also full text content for matching
    wordpress.element(fnode=node(tags="a", text="Lost your password?", title="Password Lost and Found"))


**bnode** Locator
"""""""""""""""""

Matches partial content at beginning of attributes and text. Tags and Classes are expected to be provided exactly as in HTML.

Code usage is same as that of **node** locator. Following is a sample:

.. code-block:: python

    # You can also partial text content at beginning for matching
    wordpress.element(bnode=node(tags="a", text="Lost", title="Password Lost"))


**Interaction with GuiElement**
-------------------------------

To interact with a GuiElement, from automation angle it must be in an interactable state. In the usual automation code, a test author writes a lot of waiting related code (and let's not even touch the **time.sleep**.).

**Automatic Dynamic Waiting**
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Arjuna does a granular automatic waiting of three types:
    - Waiting for the presence of an element when it is attempting to identify a GuiElement
    - Waiting for the right state (for example, clickability of an GuiElement when you enter text or want to click it)
    - Waiting for interaction to succeed (Arjuna, for example, retries click if interaction exception is raised).

Interaction Methods
^^^^^^^^^^^^^^^^^^^

Once locted **GuiElement** provides various interaction methods. Some are shown below:

.. code-block:: python

   element.text = user
   element.click()

**text** is a property of **GuiElement**. **element.text = "some_string"** is equivalent of setting text of the text box.

**click** method is used to click the element.

.. _dynamic_locators:

**Dynamic/Formatted Locators** 
------------------------------

There are many situations where you would like to use dyanamic or formattable locators.

.. _placeholder_dollars:

Arjuna's **$<name>$** Placeholder
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

You can use Arjuna's **$<name>$** placeholders in locators to define dynamic locators.

.. _locator_auto_format:

**Auto-Formatting** using **C,L,R** Magic Functions
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

The placeholder is more advanced than Python's **{}** placeholder:
    * Provides case-insensitive match for names in placeholders
    * Supports auto-parameterization of the placeholders with the following prefixes:
        * **C.<query>**: Reference configuation option value. For example C.abc
        * **L.<query>**: Localized value for the name. For example L.abc
        * **R.<query>**: Data Reference Value for the name. For example R.abc

    .. note::
        The **query** in each of the above formats corresponds to the query string format that you use for the magic **C()**, **L()** and **R()** calls.

In the following examples, the values are automatically formatted for dyanmic locators:

.. code-block:: python

    # From Reference Configuration
    wordpress.element(link="$C.link.name$")

    # From Data Reference
    wordpress.element(link="$R.links.test1.navlink$")

    # From Localizer
    wordpress.element(link="$L.links.posting$")


Using **Gui**'s **formatter()** Method for Formatting Plaeholders
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Arjuna provides an easy way to programmatically format dynamic identifiers.

Rather than using the **element** method of a **Gui**, you use **formatter** call and use the **element** method of formatter object.

.. code-block:: python

    wordpress.formatter(text="Media").element(link="$text$")

In the above example, **$text$** placeholder is defined for the **link** locator.

Using **formatter** you pass one or more keyword arguments to format the locator.

The above call is equivalent to the following non-dynamic locator call:

.. code-block:: python

    wordpress.element(link="Media")

Following is some more involved examples of the power of dyanmic identifiers:

.. code-block:: python
    
    wordpress.formatter(tg="input", idx="er_l", sz=20).element(node=node(tags="$tg$", id="$idx$", size="$sz$"))
    wordpress.formatter(tg="input", attr1='id', idx="er_l", attr2='size', sz=20).element(node=node(attrs={'tags':"$tg$", '$attr1$': "$idx$", '$attr2$': "$sz$"}))







