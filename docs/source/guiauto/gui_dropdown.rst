.. _gui_dropdown:

Advanced GuiWidgets: **DropDown** - Handling Default HTML Select
=================================================================

DropDown object in Arjuna represents the Select-style control in the UI. Here, we cover handling of a default-HTML select control which has **<select>` as the root tag and **option** as the tag for an option.

Defining and Using a DropDown In Code
-------------------------------------

You can create a **DropDown** using the **dropdown** factory call of a **GuiApp** (assume **app** to be **GuiApp** object):

.. code-block:: python

   app.dropdown(<locator_type>=<locator_value>)

Defining DropDown in GNS and Using it in Code
---------------------------------------------

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
-------------------------

It provides various properties and methods for a higher level interaction with a drop down list.

- You can select an option by its visible text by calling **select_text** method of DropDown.
- DropDown provides various enquiry methods - **has_visible_text_selected**, **has_value_selected**, has_index_selected**.
- DropDown also has enquirable properties - **value** and **text**.
- There are other ways of selection as well - **select_value** to select by value attribute of an option, **select_index** to select an option present at provided index.
- DropDown also has a way of selecting an option by setting its **text** property. This is similar to **.text** property setting of a text-box. It is different from **select_text** method in terms of implementation. **select_text** uses DOM inquiry to match the text of an option and then clicks it to select it. Setting the **.text** property similuates the user action where the user types a string in a focused/highlighted select control to select an option (in technical terms it is equivalent of sendkeys).