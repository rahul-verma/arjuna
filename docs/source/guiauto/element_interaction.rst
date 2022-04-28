.. _element_interaction:

**Element Interactions**
========================

To interact with a GuiElement, from automation angle it must be in an interactable state. In the usual automation code, a test author writes a lot of waiting related code (and let's not even touch the **time.sleep**.).

**Automatic Contextual Dynamic Waiting**
----------------------------------------

Arjuna does a granular automatic waiting of three types:
    - Waiting for the presence of an element when it is attempting to identify a GuiElement
    - Waiting for the right state (for example, clickability of an GuiElement when you enter text or want to click it)
    - Waiting for interaction to succeed (Arjuna, for example, retries click if interaction exception is raised).

**Entering/Setting Text**
-------------------------

You can enter text in a text box using **enter_text** call. It clicks on the element before entering text.

.. code-block:: python

   element.enter_text("user")

You can set text for an element using the **text** property. It clicks the element, clears text and then enters the text provided.

.. code-block:: python

   element.text = "user"

**text** is a property of **GuiElement**. **element.text = "some_string"** is equivalent of setting text of the text box.

To clear text without entering new text, you can use the **clear_text** call:

.. code-block:: python

   element.clear_text()

**(Single/Double) Clicking** an Element 
---------------------------------------

.. code-block:: python

   element.click()
   element.double_click()

**Hovering Actions** on an Element
----------------------------------

.. code-block:: python

   element.hover()
   element.hover_and_click()

**Dragging/Dropping** an Element
--------------------------------

You can drag an element using **drag** method by providing an Offset specifying X and Y coordinate offsets as follows:

.. code-block:: python

   element.drag(offset=Screen.offset(10,20))

You can drop an element on another element using **drop** method by providing the target element and optionally an Offset specifying X and Y coordinate offsets as follows:

.. code-block:: python

   element.drop(target_element)
   element.drop(target_element, offset=Screen.offset(10,20))

**Checking/Unchecking/Toggling** a Checkbox
-------------------------------------------

The calls do not change the state if the checkbox is already in target state.

.. code-block:: python

   element.check()
   element.uncheck()

If you want to switch the current state of checbox, use **toggle**:

.. code-block:: python

   element.toggle()

**Selecting/Deselecting/Toggling** an Element
---------------------------------------------

The calls do not change the state if the element is already in target state.

.. code-block:: python

   element.select()
   element.deselect()

If you want to switch the current state of an element, use **toggle**:

.. code-block:: python

   element.toggle()