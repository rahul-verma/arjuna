.. _gui_radiogroup:

Advanced GuiWidgets: **RadioGroup** - Handling Default HTML Radio Group
========================================================================

RadioGroup object in Arjuna represents the Radio Buttons in the UI that belong to a single selection group (have the same name). Here, we cover handling of a default-HTML RadioGroup control which represents multiple **<input type='radio'>` elements which have the same **name** attribute value.

Defining and Using a RadioGroup In Code
---------------------------------------

You can create a **RadioGroup** using the **radio_group** factory call of a **GuiApp** (assume **app** to be **GuiApp** object):

.. code-block:: python

   app.radio_group(<locator_type>=<locator_value>)

Defining RadioGroup in GNS and Using it in Code
-----------------------------------------------

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
---------------------------

It provides various properties and methods for a higher level interaction with a radio group.

- You can select a a by its visible text by calling **select_text** method of DropDown.
- RadioGroup provides various enquiry methods - **has_value_selected**, **has_index_selected**.
- RadioGroup also has **value** enquirable property.
- You can use two ways of selecting a radio button - **select_value** to select by value attribute of an option, **select_index** to select a radio button present at provided index.
