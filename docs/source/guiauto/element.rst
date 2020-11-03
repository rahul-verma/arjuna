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

**ID**, **Name**, **Tag**, **Class**, **Link Text**, **Partial Link Text**, **XPath** and **CSS Selector**
----------------------------------------------------------------------------------------------------------

Arjuna supports the locators which are supported by Selenium's By object. Apart from these, there are various abstracted locators which Arjuna provides for easier coding.

For locating **GuiElement**, you can use the **.element** factory method (assume **app** is the **GuiApp** object):

.. code-block:: python

   app.element(<locator_type>=<locator_value>)

The locator strategy is expressed using locator type names supported by Arjuna. You can pass it as a keyword argument **k=v** format to the the **element** call. Following are the basic locators supported and corresponding Selenium **By** locators:
    - **id** : Wraps **By.id**
    - **name** : Wraps **By.name**
    - **tag** : Wraps **By.tag_name**
    - **classes** : Wraps **By.class_name**, however it supports compound classes. See Arjuna Locator Extensions page for more information.
    - **link** : Wraps **By.partial_link_text**. Note that all content/text matches in Arjuna are partial matches (opposite of Selenium).
    - **flink** : Wraps **By.link_text** (short for Full Link)
    - **xpath** : Wraps **By.xpath**
    - **selector** : Wraps **By.css_selector**

Following are some examples:

.. code-block:: python

   wordpress.element(id="user_login")
   wordpress.element(name="log")
   wordpress.element(tag="input")
   wordpress.element(classes="input")
   wordpress.element(link="password")
   wordpress.element(flink="Lost your password?")
   wordpress.element(xpath="//*[contains(text(), 'Lost')]")
   wordpress.element(selector=".button.button-large")

**Alternative Locators** - Specifying Multiple Locators with **OR Relationship**
--------------------------------------------------------------------------------

You can also pass multiple locators as arugment in **element** calls. 

Arjuna will try all of these one by one in a dynamic wait mechanism. The total maximum wait time does not add up, it remains same as that for using a single identifier.

.. code-block:: python

   wordpress.element(tag="input", classes="someclass")

.. _coded_locator_exts:

**Arjuna's Locator Extensions**
-------------------------------

Arjuna provides various higher level locator strategies in addition to wrapping Selenium's By-style strategies. 

Following sections discuss these extensions:

**text** Locator
^^^^^^^^^^^^^^^^

It is used to locate a GuiWidget based on its partial text.

.. code-block:: python

    wordpress.element(text="your")


**ftext** Locator
^^^^^^^^^^^^^^^^^
It is used to locate a GuiWidget based on its full text.

.. code-block:: python

    # Using ftext locator. Full text is to be specified.
    wordpress.element(ftext="Lost your password?")


**btext** Locator
^^^^^^^^^^^^^^^^^
It is used to locate a GuiWidget based on partial text match at beginning of text.

.. code-block:: python

    # Using ftext locator. Full text is to be specified.
    wordpress.element(btext="Lost")


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

**attr** Locator 
^^^^^^^^^^^^^^^^
It is used to locate a GuiWidget based on partial content of a specific attribute.

.. code-block:: python

    # Here the 'for' attribute contains the value 'user_login'. Partial content can be passed.
    wordpress.element(attr=attr("for", "_login"))


**fattr** Locator 
^^^^^^^^^^^^^^^^^
It is used to locate a GuiWidget based on full content of a specific attribute.

.. code-block:: python

    # Here the 'for' attribute contains the value 'user_login'. Full content should be passed.
    wordpress.element(fattr=attr("for", "user_login"))


**battr** Locator 
^^^^^^^^^^^^^^^^^
It is used to locate a GuiWidget based on partial content at beginning of a specific attribute.

.. code-block:: python

    # Here the 'for' attribute contains the value 'user_login'.
    wordpress.element(battr=attr("for", "user_"))


**eattr** Locator 
^^^^^^^^^^^^^^^^^
It is used to locate a GuiWidget based on partial content at end of a specific attribute.

.. code-block:: python

    # Here the 'for' attribute contains the value 'user_login'.
    wordpress.element(eattr=attr("for", "user_"))


**node** Locator
^^^^^^^^^^^^^^^^
It is used to locate a GuiWidget based on:
    - Partial content of one or more attributes 
    - (Optional) the tag name
    - (Optional) Partial text content

.. code-block:: python

    # Here a HTML element with tag input is targeted which has id=user_login and size=20. Partial content can be passed.
    wordpress.element(node=node(tag="input", id="_login", size=20))

    # Sometimes names of attributes conflict with Python keywords. 
    # In such a case 'attr' can be passed as a psitional argument
    wordpress.element(node=node(attr('for','_login'), tag="label", size=20))

    # You can also pass a dictionary of attributes
    wordpress.element(node=node(tag="label", size=20, attrs={'for': '_login'}))

    # You can also use partial text content for matching
    wordpress.element(node=node(tag="a", text="your password?", title="Found"))

.. note::

    In situations where the same attribute name is present in multiple places in the call, following sequence determines what value is finally retained for such an attribute:
        * First the **attrs** dictionary is processed
        * Second, the attributes passed as positional arguments are processed.
        * Third, the attributes passed as direct keyword arguments are processed.

**fnode** Locator
^^^^^^^^^^^^^^^^^
It is used to locate a GuiWidget based on:
    - Full content of one or more attributes 
    - (Optional) the tag name
    - (Optional) Full text content

.. code-block:: python

    # Here a HTML element with tag input is targeted which has id=user_login and size=20. Full content must be passed.
    wordpress.element(fnode=node(tag="input", id="user_login", size=20))

    # Sometimes names of attributes conflict with Python keywords. 
    # In such a case 'attr' can be passed as a psitional argument
    wordpress.element(fnode=node(attr('for','user_login'), tag="label", size=20))

    # You can also pass a dictionary of attributes
    wordpress.element(fnode=node(tag="label", size=20, attrs={'for': 'user_login'}))

    # You can also full text content for matching
    wordpress.element(fnode=node(tag="a", text="Lost your password?", title="Password Lost and Found"))


.. note::

    In situations where the same attribute name is present in multiple places in the call, following sequence determines what value is finally retained for such an attribute:
        * First the **attrs** dictionary is processed
        * Second, the attributes passed as positional arguments are processed.
        * Third, the attributes passed as direct keyword arguments are processed.


**bnode** Locator
^^^^^^^^^^^^^^^^^
It is used to locate a GuiWidget based on:
    - Partial match at beginning of one or more attributes 
    - (Optional) the tag name
    - (Optional) Partial text content at beginning

.. code-block:: python

    # Here a HTML element with tag input is targeted which has id=user_login and size=20. Partial content at beginning of attribute(s) can be passed.
    wordpress.element(bnode=node(tag="input", id="user_", size=20))

    # Sometimes names of attributes conflict with Python keywords. 
    # In such a case 'attr' can be passed as a psitional argument
    wordpress.element(bnode=node(attr('for','user_'), tag="label", size=20))

    # You can also pass a dictionary of attributes
    wordpress.element(bnode=node(tag="label", size=20, attrs={'for': 'user_'}))

    # You can also partial text content at beginning for matching
    wordpress.element(bnode=node(tag="a", text="Lost", title="Password Lost"))


.. note::

    In situations where the same attribute name is present in multiple places in the call, following sequence determines what value is finally retained for such an attribute:
        * First the **attrs** dictionary is processed
        * Second, the attributes passed as positional arguments are processed.
        * Third, the attributes passed as direct keyword arguments are processed.


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


Interaction with GuiElement
---------------------------

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
    
    wordpress.formatter(tg="input", idx="er_l", sz=20).element(node=node(tag="$tg$", id="$idx$", size="$sz$"))
    wordpress.formatter(tg="input", attr1='id', idx="er_l", attr2='size', sz=20).element(node=node(attrs={'tag':"$tg$", '$attr1$': "$idx$", '$attr2$': "$sz$"}))







