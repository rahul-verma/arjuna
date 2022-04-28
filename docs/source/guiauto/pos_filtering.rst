.. _pos_filtering:

**Selection-Time Positional Filtering**
=======================================

Although you can filter elements by finding multiple elements as **GuiMultiElement** and then using its method calls, you might want to do the filtering at selection time itself.

For this purpose, Arjuna provides you with a special **pos** meta data key which can be provided in locator calls as well as GNS label specification.

The **pos** filter acts based on the **Extractor** object it is assigned.

.. note::
    Position filters are not supported for Radio Group widget.

.. note::
    Position filters use human counting. First position is 1.

Following sections discuss various position based extractor strategies which are made available by the factory methods of **pos** class.

**at** Extractor
----------------

You can use **at** strategy to define one or more positions to choose GuiWidgets.

**Coded**
"""""""""

.. code-block:: python

    # Out of matched GuiWidgets, select the one at position 2.
    app.element(tags="input", pos=pos.at(2))

    # Simpler special construct
    app.element(tags="input", pos=2)

    # With multi_element call, multi-element will contain a single element.
    app.multi_element(tags="input", pos=2)

You can define more than one position as well:

.. code-block:: python

    # With multi_element call, multi-element will contain all elements at defined positions
    app.multi_element(tags="input", pos=pos.at(2,4))

    # Simpler special construct
    app.multi_element(tags="input", pos=(2,4))

**GNS**
"""""""

In GNS, **pos.at** can be represented using an int for a single position and YAML list for multiple positions.

.. code-block:: yaml

    elem1:
        tags: input
        pos: 2

    multi_elem1:
        type: multi_element
        tags: input
        pos:
            - 2
            - 4 

**first** Extractor
-------------------

You can use **first** strategy to choose first GuiWidget.

**Coded**
"""""""""

.. code-block:: python

    # Out of matched GuiWidgets, select the one at first position
    app.element(tags="input", pos=pos.first())

    # Simpler special construct
    app.element(tags="input", pos="first")

    # With multi_element call, multi-element will contain a single element
    app.multi_element(tags="input", pos="first")

**GNS**
"""""""

.. code-block:: yaml

    elem1:
        tags: input
        pos: first

**last** Extractor
------------------

You can use **last** strategy to choose last GuiWidget.

**Coded**
"""""""""

.. code-block:: python

    # Out of matched GuiWidgets, select the one at last position
    app.element(tags="input", pos=pos.last())

    # Simpler special construct
    app.element(tags="input", pos="last")

    # With multi_element call, multi-element will contain a single element
    app.multi_element(tags="input", pos="last")

**GNS**
"""""""

.. code-block:: yaml

    elem1:
        tags: input
        pos: last

**odd** Extractor
-----------------

You can use **odd** strategy to choose all GuiWidgets at odd positions.

**Coded**
"""""""""

.. code-block:: python

    # Out of matched GuiWidgets, select the ones at odd positions
    app.multi_element(tags="input", pos=pos.odd())

    # Simpler special construct
    app.multi_element(tags="input", pos="odd")

    # With element call, first element at odd position is returned (same as first element)
    app.element(tags="input", pos="odd")


**GNS**
"""""""

.. code-block:: yaml

    elem1:
        tags: input
        pos: odd

    melem1:
        tags: input
        pos: odd

**even** Extractor
------------------

You can use **even** strategy to choose all GuiWidgets at even positions.

**Coded**
"""""""""

.. code-block:: python

    # Out of matched GuiWidgets, select the ones at even positions
    app.multi_element(tags="input", pos=pos.even())

    # Simpler special construct
    app.multi_element(tags="input", pos="even")

    # With element call, first element at even position is returned (second element)
    app.element(tags="input", pos="even")


**GNS**
"""""""

.. code-block:: yaml

    elem1:
        tags: input
        pos: even

    melem1:
        tags: input
        pos: even

**random** Extractor
--------------------

You can use **random** strategy to choose GuiWidgets at one or more random positions.

**Coded**
"""""""""

.. code-block:: python

    # Out of matched GuiWidgets, select the one at position 2.
    app.element(tags="input", pos=pos.random())

    # Simpler special construct
    app.element(tags="input", pos="random")

    # With multi_element call, multi-element will contain a single element.
    app.multi_element(tags="input", pos="random")

You can also specify number of random selections using **count** attribute or a positional arg to that effect:

.. code-block:: python

    # With multi_element call, multi-element will contain all elements at defined positions
    app.multi_element(tags="input", pos=pos.random(count=4))

    # Simpler special construct
    app.multi_element(tags="input", pos=pos.random(4))

**GNS**
"""""""

In GNS, **pos.random** can be represented using a string literal or the count can be provided as count arg or a positional int.

.. code-block:: yaml

    elem1:
        tags: input
        pos: random

    multi_elem1:
        type: multi_element
        tags: input
        pos:
            random: 3

**slice** Extractor
-------------------

This extractor is inspired by Python's built-in slice implementation, but uses positions instead of indices.

You can provide a start position, a stop position and define step which tells the logic how much to move from one position to another when creating the slice.

It is an advanced extractor which behaves differently depending on the argument combinations.

**Coded**
"""""""""

.. code-block:: python

    # Out of matched GuiWidgets, select the ones as per slice: First 5.
    app.multi_element(tags="input", pos=pos.slice(5))
    app.multi_element(tags="input", pos=pos.slice(stop=5))

    # Out of matched GuiWidgets, select the ones as per slice: From 3 to 5.
    app.multi_element(tags="input", pos=pos.slice(3,5))
    app.multi_element(tags="input", pos=pos.slice(start=3, stop=5))

    # Out of matched GuiWidgets, select the ones as per slice: From 3 to 10 with step of 2 i.e 3,5,7,9.
    app.multi_element(tags="input", pos=pos.slice(3,10,2))
    app.multi_element(tags="input", pos=pos.slice(start=3, stop=10, step=2))

    # With element call, first object in the slice match is returned. Here object at 3rd position is got.
    app.element(tags="input", pos=pos.slice(start=3, stop=10, step=2))


**GNS**
"""""""

In GNS, **pos.slice** can be represented using a YAML mapping.

.. code-block:: yaml

    multi_elem1:
        type: multi_element
        tags: input
        pos:
            slice:
                stop: 5

    multi_elem2:
        type: multi_element
        tags: input
        pos:
            slice:
                start: 3
                stop: 5

    multi_elem3:
        type: multi_element
        tags: input
        pos:
            slice:
                start: 3
                stop: 10
                step: 2

