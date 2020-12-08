.. _element:

**Element Identification and Interaction**
==========================================

**GuiElement and Widgets**
--------------------------

Arjuna's Gui automation implementation has different types of Gui Widgets which are associated with corresponding Widget types.

A single node in the DOM of a web UI is represented by a **GuiElement** object in Arjuna, irrespective of its type. This is unless you need specialized methods which we will see later.

The Widget type for **GuiElement** is **element**. This information is not important here, but will become relevant when we deal with more complex node types.

All locators discussed here can be used for any type of Gui Widgets.

**Identification**
------------------

Arjuna supports various basic locators (:ref:`basic_locators`) and its own locator extensions (:ref:`locator_exts`).

For locating **GuiElement**, you can use the **.element** factory method (assume **app** is the **GuiApp** object):

.. code-block:: python

   app.element(<locator_type>=<locator_value>)

The locator strategy is expressed using locator type names supported by Arjuna. You can pass it as a keyword argument **k=v** format to the the **element** call. 

For example, following code locates a GuiElement by its **id** attribute:

.. code-block:: python

   app.element(id="user_login")

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

Check :py:class:`GuiElement <arjuna.tpi.guiauto.widget.element.GuiElement>` and its base classes to know about various methods and properties.
