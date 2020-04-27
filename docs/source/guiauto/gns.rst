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

Externalizing ID, Name, Tag, Class, Link Text, Partial Link Text, XPath and CSS Selector
----------------------------------------------------------------------------------------

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

Externalizing Arjuna's Locator Extensions
-----------------------------------------

All of Arjuna's locator extensions can be externalizd in GNS as well.

- Following are externalized as simple key value pairs:
    - ****text****
    - ****ftext****
    - ****title****
    - ****value****
    - ****js****
- Following are externlized with content as a YAML mapping with **name** and **value** keys:
    - ****attr****
    - ****fattr****
- ****classes**** is externalized as a single string or a YAML list of strings:
- ****point**** is externlized with content as a YAML mapping with **x** and **y** keys.

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
            name: for
            value: _login
   
    user_fattr:
        fattr:
            name: for
            value: user_login

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

You can use them in code just like externalized basic locators. Following is sample code (assume **app** to be a **GuiApp** object). For example:

.. code-block:: python

    element = wordpress.gns.lost_pass_text
