.. _visual_relation:

**Visual Relationships** for Selection of GuiElements 
=====================================================

Arjuna supports specifying visual relationships with other **GuiElements**.

This feature is built on top of Selenium's relative locators but is extended to provide much more powerful way of using it as compared to directly using Selenium.

Visual relationships act as selection-time filters. Depending on usage (coded vs GNS, direct vs nested locating) the relationship is specified with respect to a:
    * GuiElement
    * GuiPartialElement
    * GuiWidgetDefinition
    * GNS Label

**Types** of Visual Relationships
---------------------------------

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
---------------------------------------

**Coded**
"""""""""

All relationships in code are provided as a keyword argument in the locator calls of a Gui.

The object can be a GuiElement or GuiWidgetDefinition.

Following is an example of locating a submit button to the right of remember me checkbox. Other relations can be used in the same manner:

.. code-block:: python

    # right_of with GuiElement as its value
    app.element(classes="button", right_of=app.element(id="rememberme"))

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
--------------------------------------------

You can specify multiple visual relationships together.

Following coded and GNS examples locate Publish date link which is in Date Column (below Date heading) and for the row cell containing "Test1" (to right of this entry in the same row).

**Coded**
"""""""""

.. code-block:: python

    test1 = app.element(link="Test1")
    date_col = app.element(id="date")
    test1_date = app.element(classes="column-date", right_of=test1, below=date_col)

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
-------------------------------------------------------------------

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
--------------------------------------------------------------

Arjuna wraps Selenium's relative locator feature. Selenium converts such usage to a JavaScript call which can be executed only at WebDriver level and not WebElement level. Because of this, Selenium currently throws an exception which relates to JSON serialization of RelativeBy object, but in simple words, means that it is not supported.

Arjuna has some contexts, where nested element finding is enforced on all elements depending on a specification. For example, if you define a root element for a GuiSection GNS file or specify the same in its constructor, all GuiWidgets in this GuiSection are found in a nested manner. Hence, default Selenium behavior will disrupt the model.

Arjuna follows a fallback approach to this problem. When Visual Relationships are used in a nested element finding context, the finding logic uses GuiAutomator and not GuiWidget for finding. In simple words, rather than nested element finding in this case, Arjuna will resort to finding the GuiWidget from the root of HTML page.

**Which Locators are Supported for Visual Relationships?**
----------------------------------------------------------

Currently Selenium supports relative locators only when the By type is a Tag name. This is an artificial limit imposed by the way Selenium's **relative_by** module is structured.

Arjuna gets rid of this artificial limit and supports **ALL** Arjuna built-in as well as locator extensions created by you in **withx.yaml** or **withx** sections, except the following few cases:
    * js locator
    * point locator
    * Any withx extensions built on top of js and point locators.

