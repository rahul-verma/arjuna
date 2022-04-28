.. _element:

**Element Identification**
==========================

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