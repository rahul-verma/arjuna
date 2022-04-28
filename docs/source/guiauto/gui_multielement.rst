.. _gui_multielement:

Advanced GuiWidgets: **GuiMultiElement** - Handling Multiple GuiElements Together
=================================================================================

Arjuna provides a special abstraction for representing mutliple **GuiElements** together rather than a raw Python list. This provides an opportunity to include higher level methods for test code authors.

Defining and Using a GuiMultiElement In Code
--------------------------------------------

You can create a **GuiElement** using the **multi_element** factory call of a **GuiApp** (assume **app** to be **GuiApp** object):

.. code-block:: python

  app.multi_element(<locator_type>=<locator_value>)

Defining GuiMultiElement in GNS and Using it in Code
----------------------------------------------------

You can also define a **GuiMultiElement** in a GNS File.

In the GNS file for a label corresponding to a GuiMultiElement, add the **type** entry and set it to **multi_element**, for example:

.. code-block:: yaml

  cat_checkboxes:
    type: multi_element
    name: "delete_tags[]"

In your code, you can create an element of this as usual, however this time you'll get a **GuiMultiElement** object instead of **GuiElement**.

.. code-block:: python

   check_boxes = app.gns.cat_checkboxes

Interacting with GuiMultiElement
--------------------------------

It provides various properties and methods for a higher level interaction with a sequence of **GuiElements**.

- It supports index based retrieval just like a regular list. Indexes start from computer counting (0).
- In addition to this, it provides propeties like **first_element**, **last_element** and **random_element**.
