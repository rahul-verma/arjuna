.. _gns:

**Gui Namespace - Externalizing Locators**
==========================================

After launching a **GuiApp**, apart from basic browser operations, most of times an automated test finds and interacts with Gui elements. If locators can be externalized outside of the code, it has a significant impact on the maintainbility of the Gui test automation implementation.

Externalizing of identifiers is built into Arjuna. The object which contains identification information and related meta-data of a Gui is referred to as **GuiNamespace (GNS)** in Arjuna.

The GNS File
------------

Arjuna uses **YAML** as the format for externalization of identifiers. Fow now, we will discuss basic usage of the format.

Following is the high level format for simple usage:

.. code-block:: yaml

   labels:
   
    <label1>:
        <locator type>: <locator data>
   
    <label2>:
        <locator type>: <locator data>
   
    <labelN>:
        <locator type>: <locator data>


#. This file has a **YAML** extension.
#. All labels are placed under **labels** heading.
#. Each label represents element identification information which can be later referenced by this label.
#. The label should be a valid Arjuna name.
#. In its basic usage format, the section has a key value pair for a given locator type. For example 

    .. code-block:: YAML

        id: user_login

#. Labels are treated as case-insensitive by Arjuna.


Associating GNS File with App
-----------------------------

Arjuna picks up GNS files relative to the defaut GNS directory: **<Project Root>/guiauto/namespace**. You can give the **label** argument while constructing a **GuiApp** to associate it with the GNS file as follows:

.. code-block:: python

   app = GuiApp(label="SomeName")

There are many advanced ways for this association, which are documented later in this doc.

.. _basic_locator_gns:

**Externalizing** **ID**, **Name**, **Tag**, **Class**, **Link Text**, **Partial Link Text**, **XPath** and **CSS Selector**
----------------------------------------------------------------------------------------------------------------------------

The locator strategy in GNS files is expressed using locator type names supported by Arjuna. These are simple locators and hence are expressed as basic key value pairs, almost equivalent to the way you pass them as keyword arguments in **app.element** calls. Functionality is equivalent as well.

Following is a sample GNS file showing externalized basic locators:

.. code-block:: yaml

   labels:
   
    user_id:
        id: user_login
   
    user_name:
        name: log
   
    user_tag:
        tag: input

    user_class:
        classes: input
   
    lost_pass_link:
        link: password
   
    lost_pass_flink:
        flink: "Lost your password?"
   
    lost_pass_text_content:
        xpath: "//*[contains(text(), 'Lost')]"
   
    button_compound_class:
        selector: ".button.button-large"

You can create elements using these identifiers by using **<app object>.gns.<GNS label>` syntax in your code as follows (assume **app** to be the **GuiApp** object). For example:

.. code-block:: python

   element = app.gns.user_id

Arjuna uses operator overloading to tie the **gns** attribute to the **GNS file** label, locates it and creates the **GuiElement**.

.. _ext_locator_gns:

**Externalizing Arjuna's Locator Extensions**
---------------------------------------------

All of Arjuna's locator extensions can be externalizd in GNS as well.

GNS Locator Externalization Format
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

- Following are externalized as simple key value pairs:
    - **text**
    - **ftext**
    - **btext**
    - **title**
    - **value**
    - **js**
- Following are externlized with content as a YAML mapping attribute specified as a single key value pair:
    - **attr**
    - **fattr**
    - **battr**
    - **eattr**
- Following are externalized with content as a YAML mapping with attribute names as key value pairs and optioanlly a **tag** and/or **text** key.
    - **node**
    - **fnode**
    - **bnode**
- **classes** is externalized as a single string or a YAML list of strings:
- **point** is externlized with content as a YAML mapping with **x** and **y** keys.


.. _gns_locator_exts:

Examples of Arjuna's Extended Locators in GNS
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Following is a sample GNS file for the above locators:

.. code-block:: yaml

   labels:
   
    lost_pass_text:
        text: Lost
   
    lost_pass_ftext:
        ftext: "Lost your password?"
   
    lost_pass_title:
        title: Password Lost and Found
   
    user_value:
        value: Log In
   
    user_attr:
        attr:
            for: _login
   
    user_fattr:
        fattr:
            for: user_login

    user_battr:
        fattr:
            for: user_

    user_eattr:
        eattr:
            for: _login

    user_node_1:
        node:
            title: Found
            tag: a
            text: Lost

    user_node_1:
        fnode:
            title: Password Lost and Found
            tag: a
            text: Lost your Password?

    user_node_1:
        bnode:
            title: Lost
            tag: a
            text: Lost

    button_classes_str:
        classes: button button-large

    button_classes_list:
        classes: 
            - button 
            - button-large
   
    elem_xy:
        point:
            x: 1043
            y: 458
   
    elem_js:
        js: "return document.getElementById('wp-submit')"

You can refer the element labels defined using extended locators in code just like those for externalized basic locators. Following is sample code (assume **app** to be a **GuiApp** object). For example:

.. code-block:: python

    element = wordpress.gns.lost_pass_text


Dynamic Locators in GNS
-----------------------

:ref:`dynamic_locators` using :ref:`placeholder_dollars` can be defined in a GNS file as well.

**Auto-Formatting** using **C,L,R** Magic Functions
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Auto-formatting using **C.,L.,R.** prefixes** works just like it does in code (:ref:`placeholder_dollars`):

.. code-block:: yaml

    labels:

        nav_link1:
            link: $C.link.name$

        nav_link2:
            link: $R.links.test1.navlink$

        nav_link3:
            link: $L.links.posting$

Using **GNS**'s **formatter()** Method for Formatting Plaeholders
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Placeholdrs can also be defined so that programmatically values can be passed to format the locators:


.. code-block:: yaml

    labels:

        nav_link1:
            link: $text$

        password:
            node:
                tag: $tg$
                $attr1$: $idx$
                $attr2$: $sz$

Rather than using the **element** method of a **GNS**, you use **formatter** call and use the **element** method of formatter object.

Using **formatter** you pass one or more keyword arguments to format the locator.

.. code-block:: python

    wordpress.gns.formatter(text="Media").nav_link1
    wordpress.formatter(tg="input", attr1='id', idx="er_l", attr2='size', sz=20).password


**GuiApp GNS** as **Fallback GNS** for Pages, Sections and Widgets
------------------------------------------------------------------

The GNS file for GuiApp acts as a fallback for labels not defined in GNS of a corresponding **GuiPage**, **GuiSection** or **GuiWidget**.

This comes handy when there are locators that are relevant for multiple pages, sections or widgets.

This also helps to start small with externalization by putting all locators in **GuiApp** GNS file and then expanding the model further as you go along by creating more externalized GNS files for pages, sections and widgets.