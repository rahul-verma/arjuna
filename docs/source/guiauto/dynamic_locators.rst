.. _dynamic_locators:

**Dynamic/Formatted GuiWidget Locators**
========================================

There are many situations where you would like to use dyanamic or formattable locators.

.. _placeholder_dollars:

Arjuna's **$<name>$** Placeholder
---------------------------------

You can use Arjuna's **$<name>$** placeholders in locators to define dynamic locators.

The placeholder name can be:
    * A **C/L/R** query which Arjuna will auto-format (:ref:`locator_auto_format`)
    * Any name that you will parameterize in code using **formatter** call. (:ref:`locator_formatter`)

.. _locator_auto_format:

**Auto-Formatting** using **C,L,R** Magic Functions
---------------------------------------------------

The placeholder is more advanced than Python's **{}** placeholder:
    * Provides case-insensitive match for names in placeholders
    * Supports auto-parameterization of the placeholders with the following prefixes:
        * **C.<query>**: Reference configuation option value. For example C.abc
        * **L.<query>**: Localized value for the name. For example L.abc
        * **R.<query>**: Data Reference Value for the name. For example R.abc

    .. note::
        The **query** in each of the above formats corresponds to the query string format that you use for the magic **C()**, **L()** and **R()** calls.

In the following examples, the values are automatically formatted for dyanmic locators:

**Coded**
^^^^^^^^^

.. code-block:: python

    # From Reference Configuration
    app.element(link="$C.link.name$")

    # From Data Reference
    app.element(link="$R.links.test1.navlink$")

    # From Localizer
    app.element(link="$L.links.posting$")

**GNS**
^^^^^^^

.. code-block:: yaml

    nav_link1:
        link: $C.link.name$

    nav_link2:
        link: $R.links.test1.navlink$

    nav_link3:
        link: $L.links.posting$

.. _locator_formatter:

Formatting Placeholders using **formatter** Method
--------------------------------------------------

Arjuna provides an easy way to programmatically format dynamic identifiers.

**Coded**
^^^^^^^^^

Rather than using the **element** method of a **Gui**, you use **formatter** call and use the **element** method of formatter object.

.. code-block:: python

    app.formatter(text="Media").element(link="$text$")

In the above example, **$text$** placeholder is defined for the **link** locator.

Using **formatter** you pass one or more keyword arguments to format the locator.

The above call is equivalent to the following non-dynamic locator call:

.. code-block:: python

    app.element(link="Media")

Following is some more involved examples of the power of dyanmic identifiers:

.. code-block:: python
    
    app.formatter(tg="input", idx="er_l", sz=20).element(node=node(tags="$tg$", id="$idx$", size="$sz$"))
    app.formatter(tg="input", attr1='id', idx="er_l", attr2='size', sz=20).element(node=node(attrs={'tags':"$tg$", '$attr1$': "$idx$", '$attr2$': "$sz$"}))

**GNS**
^^^^^^^

Placeholdrs can also be defined in GNS so that programmatically values can be passed to format the locators:

.. code-block:: yaml

    nav_link1:
        link: $text$

    password:
        node:
            tags: $tg$
            $attr1$: $idx$
            $attr2$: $sz$

Rather than using the **element** method of a **GNS**, you use **formatter** call and use the **element** method of formatter object.

Using **formatter** you pass one or more keyword arguments to format the locator.

.. code-block:: python

    app.gns.formatter(text="Media").nav_link1
    app.gns.formatter(tg="input", attr1='id', idx="er_l", attr2='size', sz=20).password

.. note::

    Note that in case of placeholders in GNS, you use **app.gns.formatter** method instead of **app.formatter** method as seen in coded version of this situation.


