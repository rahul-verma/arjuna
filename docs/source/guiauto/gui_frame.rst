.. _gui_frame:

**Handling Frames**
===================

Arjuna currently has basic support for frame handling in the web browser.

From Selenium perspective, a context switching is involved. To find and interact with elements one has to switch the WebDriver to context of frame.

This is wrapped inside Arjuna logic.

**GuiFrame** Object
-------------------

GuiFrame is the obejct in Arjuna that represents a frame.

You can locate a GuiFrame with any of the identification strategies that are used for GuiWidgets.

**Coded** GuiFrame
------------------

.. code-block:: python

   frame = app.frame(id="someframe")

Frame in **GNS**
----------------

To define a frame in GNS specify **type** as **frame**.

.. code-block:: yaml

    myframe:
        type: frame
        id: someframe

.. code-block:: python

   frame = app.gns.myframe

**Dynamic Waiting** for Presence of a Frame
-------------------------------------------

A frame is automatically waited for in Arjuna.

**Context Switching**
---------------------

As soon as a frame is located, Arjuna automatically switches context to it.

**Exiting** a Frame
-------------------

.. code-block:: python

   frame.exit()

**Finding Elements** inside a Frame
-----------------------------------

Once a frame object is created, you can find any types of GuiWidget inside it using the frame object itself.

Coded Element Finding inside Frame
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. code-block:: python

   frame.element(name="somelelement")

GNS Element Finding inside Frame
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

A frame element has access to the GNS file for the GuiApp/GuiPage/GuiSection it is defined for.

.. code-block:: yaml

    myframe:
        type: frame
        id: someframe

    myelement:
        name: somelement

.. code-block:: python

    frame = app.gns.myframe
    elem = frame.gns.myelement

Important Information on **Frames in GuiSection**
-------------------------------------------------

A GuiSection object in Arjuna can define a **root** element which is used for nested element finding for the elements inside this section.

As a frame switching loads a fresh DOM,such nested element finding is not possible.

So, for elements that are present inside a frame, provide the identifiers in a way that they are not planned as nested.


