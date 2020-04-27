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

Locators - **Arjuna's Locator Extensions**
------------------------------------------

Arjuna provides various higher level locator strategies in addition to wrapping Selenium's By-style strategies. Following is the list of these extensions:
    - **text** : Generates Partial Text based XPath
    - **ftext** : Generates Full Text based XPath
    - **title** : Generates Title Match CSS Selector
    - **value** : Generates Value Match CSS Selector
    - **attr** : Generates Partial Attribute Value Match CSS Selector
    - **fattr** : Generates Full Attribute Match CSS Selector
    - **classes** : Supports compound classes (supplied as a single string or as multiple separate strings)
    - **point** : Runs a JavaScript to find the GuiElement under an XY coordinate
    - **js** : Runs the supplied JavaScript and returns GuiElement representing the element it returns.

Following are some examples:

.. code-block:: python

   wordpress.element(text="Lost")
   wordpress.element(ftext="Lost your password?")
   wordpress.element(title="Password Lost and Found")
   wordpress.element(value="Log In")
   wordpress.element(attr=Attr("for", "_login"))
   wordpress.element(fattr=Attr("for", "user_login"))
   wordpress.element(classes="button button-large")
   wordpress.element(classes=("button", "button-large"))
   wordpress.element(point=Point(1043, 458))
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