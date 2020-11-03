.. _withx:

**Defining Your Own Locator Extensions** using **withx**
========================================================

As seen in :ref:`coded_locator_exts` section, Arjuna defines its own locator extensions to provide advanced identification facilities. These can be externalised and used in GNS as well - :ref:`gns_locator_exts`.

This leads to a lot of reuse of custom locator strings as well as representing complex reusable locators in an easy manner.

The **withx.yaml** File
-----------------------

You can create a file with the name **withx.yaml** in **<Your test project root>/config** directory. The locators extensions defined in this file are auto-loaded when Arjuna run is triggered.

This is a global GNS file in which you can define your own locator extensions.

Following is an example:

.. code-block:: yaml

    nav_link:
        wtype: xpath
        wvalue: "//li[contains(*//text(), '$lname$')]"

In the above example, a new locator extension **nav_link** has been defined:
    * **wtype** key has been set to **xpath** which means that this locator extension is built on top of **xpath**. Here you can use any of :ref:`locators` or you can also use :ref:`coded_locator_exts`.
    * **wvalue** defines the locator value and uses the corresponding GNS format (Refer :ref:`basic_locator_gns` and :ref:`ext_locator_gns`)


Using **withx** Locators in Code
--------------------------------

You can use the defined locator extension in your code just like other locators in Arjuna.

A locator extension has one or more **$$** placeholders to be formatted. This can be done using the **withx** construct.

Following code uses the **nav_link** locator extension defined in previous section:

.. code-block:: python

    wordpress.element(nav_link=withx(lname="Posts"))


Using **withx** Locators in GNS
-------------------------------

You can also use the defined locator extension in a GNS file.

Following GNS Yaml file uses the **nav_link** locator extension:

.. code-block:: yaml

    labels:
        posts:
            nav_link: Posts

Now you can use the **posts** label as usual in code:

.. code-block:: python

    wordpress.gns.posts


Defining **Local Locator Extensions** for a given **Gui**
---------------------------------------------------------

Rather than defining locator extensions at a global level, you can also define them for a particular **GuiApp**, **GuiPage**, **GuiSection** or **GuiWidget** by defining a **withx** section in the corresponding GNS file.

Let's say you have a **LeftNav.yaml** to represent a GuiSection's externalized locators. Then you can do the following in its GNS yaml file:

.. code-block:: yaml

    withx:
        nav_link:
            wtype: xpath
            wvalue: "//li[contains(*//text(), '$lname$')]"

    labels:
        posts:
            nav_link: Posts

Now you can use the **posts** label as usual in code (assuming left_nav property in wordpress GuiApp corresponds to Left navigation GuiSection object):

.. code-block:: python

    wordpress.left_nav.gns.posts