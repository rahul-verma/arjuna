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

Check :ref:`basic_locators` to know how to externalize a specific locator.

**Associating GNS File with GuiApp**
------------------------------------

Arjuna picks up GNS files relative to the defaut GNS directory: **<Project Root>/guiauto/namespace**. You can give the **label** argument while constructing a **GuiApp** to associate it with the GNS file as follows:

.. code-block:: python

   app = GuiApp(label="SomeName")

There are many advanced ways for this association, which are documented later in this doc.

**Using GNS Labels in Code**
----------------------------

You can create elements using these identifiers by using **<app object>.gns.<GNS label>` syntax in your code as follows (assume **app** to be the **GuiApp** object). For example:

.. code-block:: python

   element = app.gns.user_id

Arjuna uses operator overloading to tie the **gns** attribute to the **GNS file** label, locates it and creates the **GuiElement**.

**GuiApp GNS** as **Fallback GNS** for Pages, Sections and Widgets
------------------------------------------------------------------

The GNS file for GuiApp acts as a fallback for labels not defined in GNS of a corresponding **GuiPage**, **GuiSection** or **GuiWidget**.

This comes handy when there are locators that are relevant for multiple pages, sections or widgets.

This also helps to start small with externalization by putting all locators in **GuiApp** GNS file and then expanding the model further as you go along by creating more externalized GNS files for pages, sections and widgets.