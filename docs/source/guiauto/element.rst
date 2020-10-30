.. _element:

**Element Identification and Interaction**
==========================================

**GuiElement and Widgets**
--------------------------

Arjuna's Gui automation implementation has different types of Gui Widgets which are associated with corresponding Widget types.

A single node in the DOM of a web UI is represented by a **GuiElement** object in Arjuna, irrespective of its type. This is unless you need specialized methods which we will see later.

The Widget type for **GuiElement** is **element**. This information is not important here, but will become relevant when we deal with more complex node types.

All locators discussed here can be used for any type of Gui Widgets.

Locators - Using ID, Name, Tag, Class, Link Text, Partial Link Text, XPath and CSS Selectors
--------------------------------------------------------------------------------------------

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

Locators - **Arjuna's Locator Extensions**
------------------------------------------

Arjuna provides various higher level locator strategies in addition to wrapping Selenium's By-style strategies. 

Following sections discuss these extensions:

**text** Locator
^^^^^^^^^^^^^^^^

Generates Partial Text based XPath

.. code-block:: python

    # Using text locator. Can specify part of the text.
    wordpress.element(text="Lost")


**ftext** Locator
^^^^^^^^^^^^^^^^^
Generates Full Text based XPath

.. code-block:: python

    # Using ftext locator. Full text is to be specified.
    wordpress.element(ftext="Lost your password?")

**title** Locator
^^^^^^^^^^^^^^^^^
Generates Title Match CSS Selector

.. code-block:: python

    # Using title locator. Full content of title attribute should be specified.   
    wordpress.element(title="Password Lost and Found")

**value** Locator
^^^^^^^^^^^^^^^^^
Generates Value Match CSS Selector

.. code-block:: python

    # Using value locator. Full content of value attribute should be specified.      
    wordpress.element(value="Log In")

**attr** Locator 
^^^^^^^^^^^^^^^^
Generates Partial Attribute Value Match CSS Selector

.. code-block:: python

    # Using attr locator. Value should be supplied as attr call with name and partial content as arguments.
    wordpress.element(attr=attr("for", "_login"))


**fattr** Locator 
^^^^^^^^^^^^^^^^^
Generates Full Attribute Match CSS Selector

.. code-block:: python

    # Using fattr locator. Value should be supplied as attr call with name and full content as arguments.
    wordpress.element(fattr=attr("for", "user_login"))


**node** Locator
^^^^^^^^^^^^^^^^
Generates Partial Multi Attribute Value Match XPath. Tag name can be optionally specified as well.

.. code-block:: python

    # Using node locator. Value should be supplied as node call with attributes as key value pairs and optionally a tag argument. 
    # Attribute values can be partial contents.
    wordpress.element(node=node(tag="input", id="_login", size=20))


**fnode** Locator
^^^^^^^^^^^^^^^^^
Generates Full Multi Attribute Value Match XPath. Tag name can be optionally specified as well.

.. code-block:: python

    # Using fnode locator. Value should be supplied as node call with attributes as key value pairs and optionally a tag argument. 
    # Attribute values should be full contents.
    wordpress.element(fnode=node(tag="input", id="user_login", size=20))


**bnode** Locator
^^^^^^^^^^^^^^^^^
Generates Partial Multi Attribute Value Match XPath. The match is done at beginning of attribute values. Tag name can be optionally specified as well.

.. code-block:: python

    # Using bnode locator. Value should be supplied as node call with attributes as key value pairs and optionally a tag argument. 
    # Attribute values can be partial contents at the beginning of the attribute contents.
    wordpress.element(fnode=node(tag="input", id="user_", size=20))


**classes** Locator
^^^^^^^^^^^^^^^^^^^
Supports compound classes (supplied as a single string or as multiple separate strings)

.. code-block:: python

    # Using classes locator. Value can be a string containing space separated CSS classes.
    wordpress.element(classes="button button-large")

    # Using classes locator. Value can also be supplied as a list/tuple of CSS classes.
    wordpress.element(classes=("button", "button-large"))


**point** Locator
^^^^^^^^^^^^^^^^^
Runs a JavaScript to find the GuiElement under an XY coordinate

.. code-block:: python

    # Using point locator. Value should be a Point object with x and y coordinates specified.
    wordpress.element(point=Point(1043, 458))


**js** Locator 
^^^^^^^^^^^^^^
Runs the supplied JavaScript and returns GuiElement representing the element it returns.

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