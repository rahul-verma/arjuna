.. _widget_meta:


**Gui Widget Meta Data - Controlling Selection and Interaction Behavior**
=========================================================================

For any of the Gui Widget location method calls which are made for a Gui (GuiApp, GuiPage, GuiSection, GuiDialog), GuiElement/GuiPartialElement (for nested element finding) or for GNS of a Gui:
    * **element**
    * **multi_element**
    * **dropdown**
    * **radio_group**

along with locators, you can also specify meta data which provides you with specific keys for controlling selection and interaction time behavior.

This meta data can be defined in GNS files as well for GNS labels.

Following sections discuss various types of meta data:

Specifying **Visual Relationships** with Other GuiElements 
----------------------------------------------------------

Arjuna supports specifying visual relationships with other **GuiElements**.

This feature is built on top of Selenium's relative locators but is extended to provide much more powerful way of using it as compared to directly using Selenium.

Visual relationships act as selection-time filters. Depending on usage (coded vs GNS, direct vs nested locating) the relationship is specified with respect to a:
    * GuiElement
    * GuiPartialElement
    * GuiWidgetDefinition
    * GNS Label

**Types** of Visual Relationships
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

The visual relationships supported by Arjuna are:

**below**
"""""""""
Specifies that GuiWidget to be found is below a given GuiWidget.

**above**
"""""""""

Specifies that GuiWidget to be found is above a given GuiWidget.

**right_of**
""""""""""""

Specifies that GuiWidget to be found is to the right of a given GuiWidget.

**left_of**
"""""""""""

Specifies that GuiWidget to be found is to the left of a given GuiWidget.

**near**
""""""""

Specifies that GuiWidget to be found is near (atmost 50px) a given GuiWidget.

**Basic Usage** of Visual Relationships
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

**Coded**
"""""""""

All relationships in code are provided as a keyword argument in the locator calls of a Gui.

The object can be a GuiElement or GuiWidgetDefinition.

Following is an example of locating a submit button to the right of remember me checkbox. Other relations can be used in the same manner:

.. code-block:: python

    # right_of with GuiElement as its value
    app.element(classes="button", right_of=wordpress.element(id="rememberme"))

    # right_of with widget (GuiWidgetDefinition) as its value
    app.element(classes="button", right_of=widget(id="rememberme"))

**GNS**
"""""""

You can also use visual relationships in GNS files. The relationship can be provided with another label in the same GNS file.

Following is an example of locating a submit button to the right of remember me checkbox. Other relations can be used in the same manner:

.. code-block:: yaml

    remember_cbox:
        id: rememberme

    submit_btn:
        classes: button
        right_of: remember_cbox

Now you can use this in code as usual:

.. code-block:: python

    app.gns.submit_btn

Specifying **Multiple Visual Relationships**
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

You can specify multiple visual relationships together.

Following coded and GNS examples locate Publish date link which is in Date Column (below Date heading) and for the row cell containing "Test1" (to right of this entry in the same row).

**Coded**
"""""""""

.. code-block:: python

    test1 = wordpress.element(link="Test1")
    date_col = wordpress.element(id="date")
    test1_date = wordpress.element(classes="column-date", right_of=test1, below=date_col)

**GNS**
"""""""

.. code-block:: yaml

    test1:
        link: Test1

    date_col:
        id: date

    test1_date:
        classes: column-date
        right_of: test1
        below: date_col

Now you can use this in code as usual:

.. code-block:: python

    app.gns.test1_date

Visual Relationships and **Alternative Locators (OR Relationship)**
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Arjuna supports :ref:`alt_loc`.

When multiple locators are specified and you also provide one or more visual relationships, then these relationships are used for **EACH** one of the alternative locators provided.

In the following coded and GNS example, Arjuna will attempt to locate the GuiElement in following sequence:
    * name = choice1, above = pass_label
    * id = choice2, above = pass_label
    * tags = input, above = pass_label

**Coded**
"""""""""

.. code-block:: python

    pass_label = app.element(attr=attr(name="plabel"))
    e = app.element(name="choice1", id="choice2", tags="input", above=pass_label)

**GNS**
"""""""

.. code-block:: yaml

    pass_label:
        name: plabel

    submit_btn:
        name: choice1
        id: choice2
        tags: input
        above: pass_label

Visual Relationships in a **Nested GuiWidget Finding Context**
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Arjuna wraps Selenium's relative locator feature. Selenium converts such usage to a JavaScript call which can be executed only at WebDriver level and not WebElement level. Because of this, Selenium currently throws an exception which relates to JSON serialization of RelativeBy object, but in simple words, means that it is not supported.

Arjuna has some contexts, where nested element finding is enforced on all elements depending on a specification. For example, if you define a root element for a GuiSection GNS file or specify the same in its constructor, all GuiWidgets in this GuiSection are found in a nested manner. Hence, default Selenium behavior will disrupt the model.

Arjuna follows a fallback approach to this problem. When Visual Relationships are used in a nested element finding context, the finding logic uses GuiAutomator and not GuiWidget for finding. In simple words, rather than nested element finding in this case, Arjuna will resort to finding the GuiWidget from the root of HTML page.

**Which Locators are Supported for Visual Relationships?**
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Currently Selenium supports relative locators only when the By type is a Tag name. This is an artificial limit imposed by the way Selenium's **relative_by** module is structured.

Arjuna gets rid of this artificial limit and supports **ALL** Arjuna built-in as well as locator extensions created by you in **withx.yaml** or **withx** sections, except the following few cases:
    * js locator
    * point locator
    * Any withx extensions built on top of js and point locators.


**Selection-Time Position (pos) Based Filtering**
-------------------------------------------------

Although you can filter elements by finding multiple elements as **GuiMultiElement** and then using its method calls, you might want to do the filtering at selection time itself.

For this purpose, Arjuna provides you with a special **pos** meta data key which can be provided in locator calls as well as GNS label specification.

The **pos** filter acts based on the **Extractor** object it is assigned.

.. note::
    Position filters are not supported for Radio Group widget.

.. note::
    Position filters use human counting. First position is 1.

Following sections discuss various position based extractor strategies which are made available by the factory methods of **pos** class.

**at** Extractor
^^^^^^^^^^^^^^^^

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
^^^^^^^^^^^^^^^^^^^

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
^^^^^^^^^^^^^^^^^^

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
^^^^^^^^^^^^^^^^^

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
^^^^^^^^^^^^^^^^^^

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
^^^^^^^^^^^^^^^^^^^^

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

    multi_elem1:
        type: multi_element
        tags: input
        pos:
            random:
                count: 3

**slice** Extractor
^^^^^^^^^^^^^^^^^^^

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

