.. _element_state_wait:

**Element State Checking and Dynamic Waiting**
==============================================

**State Checking** for an Element
---------------------------------

Following are all the state checking methods available in **GuiElement** interface:

.. code-block:: python
    
    # Visibility
    element.is_visible()

    # Clickability
    element.is_clickable()

    # Selected
    element.is_selected()

    # Checked
    element.is_checked()

**Dynamic Waiting**
-------------------

As mentioned earlier, Arjuna does a granular automatic waiting of three types:
    - Waiting for the presence of an element when it is attempting to identify a GuiElement
    - Waiting for the right state (for example, clickability of an GuiElement when you enter text or want to click it)
    - Waiting for interaction to succeed (Arjuna, for example, retries click if interaction exception is raised).

However, for many other contexts, you'll need to make appropriate wait calls based on need.

Following are all the wait methods available in **GuiElement** interface:

.. code-block:: python
    
    # Visibility
    element.wait_until_visible()

    # Clickability
    element.wait_until_clickable()

    # Selected
    element.wait_until_selected()

    # Absence of an element inside this element
    element.wait_until_absent(name="child") # Any Arjuna identifiers can be used here to define child element.

    # Wait for child element content
    element.contains(name="child") # Any Arjuna identifiers can be used here to define child element.  
