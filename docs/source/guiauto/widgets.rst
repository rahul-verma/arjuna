.. _widgets:

Gui Widgets
===========

**GuiElement**
--------------

So far this was the GuiWidget type that was dicussed in documentation.

Arjuna has more types of widgets covered in the following sections.

**GuiMultiElement** - Handling Multiple GuiElements Together
------------------------------------------------------------

Arjuna provides a special abstraction for representing mutliple **GuiElements** together rather than a raw Python list. This provides an opportunity to include higher level methods for test code authors.

Defining and Using a GuiMultiElement In Code
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

You can create a **GuiElement** using the **multi_element** factory call of a **GuiApp** (assume **app** to be **GuiApp** object):

.. code-block:: python

  app.multi_element(<locator_type>=<locator_value>)

Defining GuiMultiElement in GNS and Using it in Code
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

You can also define a **GuiMultiElement** in a GNS File.

In the GNS file for a label corresponding to a GuiMultiElement, add the **type** entry and set it to **multi_element**, for example:

.. code-block:: yaml

  cat_checkboxes:
    type: multi_element
    name: "delete_tags[]"

In your code, you can create an element of this as usual, however this time you'll get a **GuiMultiElement** object instead of **GuiElement**.

.. code-block:: python

   check_boxes = wordpress.gns.cat_checkboxes

Interacting with GuiMultiElement
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

It provides various properties and methods for a higher level interaction with a sequence of **GuiElements**.

- It supports index based retrieval just like a regular list. Indexes start from computer counting (0).
- In addition to this, it provides propeties like **first_element**, **last_element** and **random_element**.

**DropDown** - Handling Default HTML Select
-------------------------------------------

DropDown object in Arjuna represents the Select-style control in the UI. Here, we cover handling of a default-HTML select control which has **<select>` as the root tag and **option** as the tag for an option.

Defining and Using a DropDown In Code
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

You can create a **DropDown** using the **dropdown** factory call of a **GuiApp** (assume **app** to be **GuiApp** object):

.. code-block:: python

   app.dropdown(<locator_type>=<locator_value>)

Defining DropDown in GNS and Using it in Code
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

You can also define a **DropDown** in a GNS File.

In the GNS file for a label corresponding to a GuiMultiElement, add the **type** entry and set it to **dropdown**, for example:

.. code-block:: python

  role:
    type: dropdown
    id: default_role

In your code, you can create an element of this as usual, however this time you'll get a **DropDown** object instead of **GuiElement**.

.. code-block:: python

   element = app.gns.role

Interacting with DropDown
^^^^^^^^^^^^^^^^^^^^^^^^^

It provides various properties and methods for a higher level interaction with a drop down list.

- You can select an option by its visible text by calling **select_text** method of DropDown.
- DropDown provides various enquiry methods - **has_visible_text_selected**, **has_value_selected**, has_index_selected**.
- DropDown also has enquirable properties - **value** and **text**.
- There are other ways of selection as well - **select_value** to select by value attribute of an option, **select_index** to select an option present at provided index.
- DropDown also has a way of selecting an option by setting its **text** property. This is similar to **.text** property setting of a text-box. It is different from **select_text** method in terms of implementation. **select_text** uses DOM inquiry to match the text of an option and then clicks it to select it. Setting the **.text** property similuates the user action where the user types a string in a focused/highlighted select control to select an option (in technical terms it is equivalent of sendkeys).

**RadioGroup** - Handling Default HTML Radio Group
--------------------------------------------------

RadioGroup object in Arjuna represents the Radio Buttons in the UI that belong to a single selection group (have the same name). Here, we cover handling of a default-HTML RadioGroup control which represents multiple **<input type='radio'>` elements which have the same **name** attribute value.

Defining and Using a RadioGroup In Code
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

You can create a **RadioGroup** using the **radio_group** factory call of a **GuiApp** (assume **app** to be **GuiApp** object):

.. code-block:: python

   app.radio_group(<locator_type>=<locator_value>)

Defining RadioGroup in GNS and Using it in Code
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

You can also define a **RadioGroup** in a GNS File.

In the GNS file for a label corresponding to a GuiMultiElement, add the **type** entry and set it to **radio_group**, for example:

.. code-block:: python

  date_format:
    type: radio_group
    name: date_format

In your code, you can create an element of this as usual, however this time you'll get a **RadioGroup** object instead of **GuiElement**.

.. code-block:: python

   element = app.gns.date_format

Interacting with RadioGroup
^^^^^^^^^^^^^^^^^^^^^^^^^^^

It provides various properties and methods for a higher level interaction with a radio group.

- You can select a a by its visible text by calling **select_text** method of DropDown.
- RadioGroup provides various enquiry methods - **has_value_selected**, **has_index_selected**.
- RadioGroup also has **value** enquirable property.
- You can use two ways of selecting a radio button - **select_value** to select by value attribute of an option, **select_index** to select a radio button present at provided index.
