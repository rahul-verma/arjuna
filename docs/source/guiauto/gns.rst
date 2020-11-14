.. _gns:

**Gui Namespace - Externalizing Locators**
==========================================

After launching a **GuiApp**, apart from basic browser operations, most of times an automated test finds and interacts with Gui elements. If locators can be externalized outside of the code, it has a significant impact on the maintainbility of the Gui test automation implementation.

Externalizing of identifiers is built into Arjuna. The object which contains identification information and related meta-data of a Gui is referred to as **GuiNamespace (GNS)** in Arjuna.

**The GNS File**
----------------

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


**Associating GNS File with GuiApp**
------------------------------------

Arjuna picks up GNS files relative to the defaut GNS directory: **<Project Root>/guiauto/namespace**. You can give the **label** argument while constructing a **GuiApp** to associate it with the GNS file as follows:

.. code-block:: python

   app = GuiApp(label="SomeName")

There are many advanced ways for this association, which are documented later in this doc.

.. _basic_locator_gns:

**Externalizing** **ID**, **Name**, **Tags**, **Class**, **Link Text**, **Partial Link Text**, **XPath** and **CSS Selector**
-----------------------------------------------------------------------------------------------------------------------------

The locator strategy in GNS files is expressed using locator type names supported by Arjuna. These are simple locators and hence are expressed as basic key value pairs, almost equivalent to the way you pass them as keyword arguments in **app.element** calls. Functionality is equivalent as well.

Following is a sample GNS file showing externalized basic locators:

.. code-block:: yaml

   labels:
   
    user_id:
        id: user_login
   
    user_name:
        name: log
   
    user_tag:
        tags: input

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

**title** Locator
^^^^^^^^^^^^^^^^^

Externalization uses a simple format with **title** as key and value as the title content.

.. code-block:: yaml

   labels:
   
    lost_pass_title:
        title: Password Lost and Found

**value** Locator
^^^^^^^^^^^^^^^^^

Externalization uses a simple format with **value** as key and value as content of **value** attribute.

.. code-block:: yaml

   labels:
   
    user_value:
        value: Log In

**tags** Locator
^^^^^^^^^^^^^^^^

This locator is externalized in multiple formats:
    - a single string with a single word
    - multiple space separated words
    - a list of strings

.. code-block:: yaml

   labels:
   
    tags_1:
        tags: form

    tags_2:
        tags: body form

    tags_3:
        tags: 
            - body 
            - form

When you use wildcard '*', you should use quotes around it for valid YAML:

.. code-block:: yaml

   labels:

    tags_4:
        tags: 
            - body 
            - '*'

You can use **any** instead of specifying it as '*'.

.. code-block:: yaml

   labels:

    tags_5:
        tags: 
            - body
            - any

**classes** Locator
^^^^^^^^^^^^^^^^^^^

This locator is externalized in multiple formats:
    - a single string with a single word
    - multiple space separated words
    - a list of strings

.. code-block:: yaml

   labels:
   
    cls_1:
        classes: button-large

    tags_2:
        classes: button button-large

    tags_3:
        classes: 
            - button 
            - button-large

**point** Locator
^^^^^^^^^^^^^^^^^

This locator is externalized as a YAML mapping with **x** and **y** keys.


.. code-block:: yaml

   labels:
   
    elem_xy:
        point:
            x: 1043
            y: 458

**js** Locator 
^^^^^^^^^^^^^^

Externalization uses a simple format with **js** as key and value as the JavaScript string.


.. code-block:: yaml

   labels:

    elem_js:
        js: "return document.getElementById('wp-submit')"


**Text Based Locators**
^^^^^^^^^^^^^^^^^^^^^^^

These are externalized as a single key-value pair with key as the locator name and value as the full or partial content based on the locator.

**text** Locator
""""""""""""""""

.. code-block:: yaml

   labels:

    lost_pass_text:
        text: Lost

**ftext** Locator
"""""""""""""""""

.. code-block:: yaml

   labels:

    lost_pass_ftext:
        ftext: "Lost your password?"

**btext** Locator
"""""""""""""""""

.. code-block:: yaml

   labels:

    lost_pass_ftext:
        btext: Lost your

**Attribute Based Locators**
^^^^^^^^^^^^^^^^^^^^^^^^^^^^

These are externalized as a single key-value pair with key as the attribute name and value as the full or partial content attribute based on the locator.

**attr** Locator 
""""""""""""""""

.. code-block:: yaml

   labels:

    user_attr:
        attr:
            for: _login


**fattr** Locator 
"""""""""""""""""

.. code-block:: yaml

   labels:

    user_fattr:
        fattr:
            for: user_login

**battr** Locator 
"""""""""""""""""

.. code-block:: yaml

   labels:

    user_battr:
        fattr:
            for: user_


**eattr** Locator 
"""""""""""""""""

.. code-block:: yaml

   labels:

    user_eattr:
        eattr:
            for: _login

**Node Definition Based Locators**
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Node definition based locators are specified as a YAML mapping that contains:
    - Full tag name(s) if specified as a single tag string, space separated string with multiple tags or a YAML list of tags.
    - Full class name(s() if specified as a single class string, space separated string with multiple classes or a YAML list of classes.
    - Attributes as key-value pairs of attribute name and Full or partial values depending on type of node locator.
    - Full or partial text content depending on type of node locator using **text**, **star_text** or **dot_text** key.
    - **use_xpath** key to enforce XPath generation instead of CSS Selector.


**node** Locator
""""""""""""""""

Following are various samples:

.. code-block:: yaml

    labels:

        n1:
            node:
                title: Found
                tags: a
                text: Lost

        n2:
            node:
                title: Found
                tags: html *
                classes: cl1 cl2
                star_text: Lost

        n3:
            node:
                title: Found
                tags: 
                    - html 
                    - '*'
                classes: 
                    - cl1 
                    - cl2
                .text: Lost

        n4:
            node:
                title: Found
                tags: 
                    - html 
                    - any
                classes: 
                    - cl1 
                    - cl2
                .text: Lost

    n5:
        node:
            id: er_l
            size: 20
            tags: input
            use_xpath: true

**fnode** Locator
"""""""""""""""""

Following are various samples:

.. code-block:: yaml

   labels:

    n1:
        node:
            title: Password Lost and Found
            tags: a
            text: Lost your Password?

    n2:
        node:
            title: Password Lost and Found
            tags: html *
            classes: cl1 cl2
            star_text: Lost your Password?

    n3:
        node:
            title: Password Lost and Found
            tags: 
                - html 
                - '*'
            classes: 
                - cl1 
                - cl2
            .text: Lost your Password?

    n4:
        node:
            title: Password Lost and Found
            tags: 
                - html 
                - any
            classes: 
                - cl1 
                - cl2
            .text: Lost your Password?

    n5:
        node:
            id: user_login
            size: 20
            tags: input
            use_xpath: true

**bnode** Locator
"""""""""""""""""

Following are various samples:

.. code-block:: yaml

   labels:

    n1:
        node:
            title: Password
            tags: a
            text: Lost

    n2:
        node:
            title: Password
            tags: html *
            classes: cl1 cl2
            star_text: Lost

    n3:
        node:
            title: Password
            tags: 
                - html 
                - '*'
            classes: 
                - cl1 
                - cl2
            dot_text: Lost

    n4:
        node:
            title: Password
            tags: 
                - html 
                - any
            classes: 
                - cl1 
                - cl2
            .text: Lost

    n5:
        node:
            id: user_
            size: 20
            tags: input
            use_xpath: true

.. _gns_locator_exts:

**Coding with Arjuna's Extended Locators Defined in GNS**
---------------------------------------------------------

You can refer the element labels defined using extended locators in code just like those for externalized basic locators. Following is sample code (assume **app** to be a **GuiApp** object). For example:

.. code-block:: python

    element = wordpress.gns.lost_pass_text


**Dynamic Locators in GNS**
---------------------------

:ref:`dynamic_locators` using :ref:`placeholder_dollars` can be defined in a GNS file as well.

.. _locator_auto_format_gns:

**Auto-Formatting** using **C,L,R** Magic Functions in GNS
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Auto-formatting using **C.,L.,R.** prefixes** works just like it does in code (:ref:`placeholder_dollars`):

.. code-block:: yaml

    labels:

        nav_link1:
            link: $C.link.name$

        nav_link2:
            link: $R.links.test1.navlink$

        nav_link3:
            link: $L.links.posting$

Using **GNS**'s **formatter()** Method for Formatting Placeholders
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Placeholdrs can also be defined so that programmatically values can be passed to format the locators:


.. code-block:: yaml

    labels:

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

    wordpress.gns.formatter(text="Media").nav_link1
    wordpress.formatter(tg="input", attr1='id', idx="er_l", attr2='size', sz=20).password


**GuiApp GNS** as **Fallback GNS** for Pages, Sections and Widgets
------------------------------------------------------------------

The GNS file for GuiApp acts as a fallback for labels not defined in GNS of a corresponding **GuiPage**, **GuiSection** or **GuiWidget**.

This comes handy when there are locators that are relevant for multiple pages, sections or widgets.

This also helps to start small with externalization by putting all locators in **GuiApp** GNS file and then expanding the model further as you go along by creating more externalized GNS files for pages, sections and widgets.