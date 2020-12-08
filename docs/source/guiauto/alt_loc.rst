.. _alt_loc:

**Alternative Locators** - Specifying Multiple Locators with **OR Relationship**
================================================================================

You can also pass multiple locators as arugment in **element** calls. 

Arjuna will try all of these one by one in a dynamic wait mechanism. The total maximum wait time does not add up, it remains same as that for using a single identifier.

Using **Different Locator Types**
---------------------------------

Coded
^^^^^

.. code-block:: python

   wordpress.element(tags="input", classes="someclass")

**GNS**
^^^^^^^

.. code-block:: yaml

    some_label:
        tags: input
        classes: someclass

Using **Same Locator Type**
---------------------------

As you would have observed above, that identifiers are provided as a dictionary:
    - In code, these are kwargs (Keyword Arguments in Python) which get stored in a dictionary by Python.
    - In GNS, they are provided as a YAML mapping.

For most situations it will work well, but as dictionaries can not have duplicate keys, this way of providing identifiers does not support providing different values for same locator type when you need an OR relationship.

The solution for this varies depending on whether you are using this in coded or GNS formats.

**Coded**
^^^^^^^^^

In code, you can use Arjuna's **oneof** call to specify different values for same locator:

.. code-block:: python

    app.element(name=oneof("choice1", "choice2"), tags="input")

The above code gives an OR relationship in following order:
    - name = "choice1"
    - name = "choice2"
    - tags = "input"

**GNS**
^^^^^^^

The solution in GNS is to use a use a YAML list format instead of a YAML mapping. Each list entry is a single key-value pair dictionary:

.. code-block:: yaml

    user_box:
        - name: choice1
        - name: choice2
        - tags: input