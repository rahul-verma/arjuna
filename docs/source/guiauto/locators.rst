.. _locators:

**Basic GuiWidget Locators**
============================

Following are the basic locators supported and corresponding Selenium **By** locators.

The locator strategy in GNS files is expressed using locator type names supported by Arjuna. These are simple locators and hence are expressed as basic key value pairs, almost equivalent to the way you pass them as keyword arguments in **app.element** calls. Functionality is equivalent as well.

**id** Locator
--------------

Locates a GuiWidget by the content of its **id** attribute.

**Coded**

.. code-block:: python

   app.element(id="user_login")

**GNS**

.. code-block:: yaml

    user_id:
        id: user_login

**name** Locator
----------------

Locates a GuiWidget by the content of its **name** attribute.

**Coded**

.. code-block:: python

   app.element(name="log")

**GNS**

.. code-block:: yaml

    user_name:
        name: log

**tags** Locator
----------------

Locates a GuiWidget by the content of its tag name. For more advanced usage, see :ref:`locator_exts`.

**Coded**


.. code-block:: python

   app.element(tags="input")

**GNS**

.. code-block:: yaml

    user_tag:
        tags: input


**classes** Locator
-------------------

Locates a GuiWidget by a class name contained in its class attribute. For more advanced usage, see :ref:`locator_exts`.

**Coded**


.. code-block:: python

   app.element(classes="cls")

**GNS**

.. code-block:: yaml

    user_class:
        classes: input

**link** Locator
----------------

Locates a GuiWidget by its PARTIAL link text.

.. code-block:: python

   app.element(link="password")

**GNS**

.. code-block:: yaml

    lost_pass_link:
        link: password

**flink** Locator
-----------------

Locates a GuiWidget by its FULL link text.

**Coded**

.. code-block:: python

   app.element(flink="Lost your password?")

**GNS**

.. code-block:: yaml

    lost_pass_flink:
        flink: "Lost your password?"


**xpath** Locator
-----------------

Locates a GuiWidget by the specifield XML Path (xpath).

**Coded**

.. code-block:: python

   app.element(xpath="//*[contains(text(), 'Lost')]")

**GNS**

.. code-block:: yaml

    lost_pass_text_content:
        xpath: "//*[contains(text(), 'Lost')]"


**selector** Locator
--------------------

Locates a GuiWidget by the specifield CSS Selector.

**Coded**

.. code-block:: python

   app.element(selector=".button.button-large")
   
**GNS**

.. code-block:: yaml

    button_compound_class:
        selector: ".button.button-large"
