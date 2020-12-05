.. _withx:

**Defining Your Own Locators** using **withx**
==============================================

As seen in :ref:`locator_exts` section, Arjuna defines its own locator extensions to provide advanced identification facilities.

This leads to a lot of reuse of custom locator strings as well as representing complex reusable locators in an easy manner.

**Global Locators** in The **withx.yaml** File
----------------------------------------------

You can create a file with the name **withx.yaml** in **<Your test project root>/config** directory. 

The locators extensions defined in this file are auto-loaded when Arjuna run is triggered.

This is a global GNS file and hence the locators defined here can be used anywhere in the project (Code as well as GNS files).

**Defining and Using** a New Locator with **Anonymous/Positional Placeholders** (**$$**)
----------------------------------------------------------------------------------------

A straight-forward way to define new locators is to use any of the existing locator types and then define a placeholder to parameterize when this locator is used.

Consider a situation where you see that many form elements are defined in HTML and corresponding easiest way for locating is by content of an attribute called **formcontrolname** (an attribute specific to this application unlike the usual **name** attribute.)

In the absence of creating a custom locator, using Arjuna you would have used the following code:

.. code-block:: python

    app.element(attr=attr(formcontrolname='username'))

And in GNS you would have put the following entry:

.. code-block:: yaml

    labels:

        user_field:
            attr:
                formcontrolname: username

This is still better than writing an XPath as supported by Arjuna. However for such situations, you can choose to create a locator of your own.

**Single Placeholder**
^^^^^^^^^^^^^^^^^^^^^^

For most of the situations, you will end up defining a locator that has a single placeholder.

Definition
""""""""""

For the context discussed above, let's create a locator **fcn** to represent a locator that matches partial content of **formcontrolname** attribute of an HTML element.

Following is an example:

.. code-block:: yaml

    fcn:
        wtype: attr
        wvalue:
            formcontrolname: $$

In the above example, a new locator type **fcn** has been defined:
    * **wtype** key has been set to **xpath** which means that this locator extension is built on top of **attr**. Here you can use any of :ref:`basic_locators` or you can also use :ref:`locator_exts`.
    * **wvalue** defines the locator value and uses the corresponding GNS format
    * $$ placeholder specifies the anonymous/positional placeholder.

Coded
"""""

You can use the defined locator type in your code just like other locators in Arjuna.

As here only one placeholder is used, a string needs to be supplied as the value.

Following code uses the **fcn** locator extension defined in previous section:

.. code-block:: python

    app.element(fcn="username")
    app.element(fcn="password")

Notice how the code starts representing your application in a much cleaner way.


GNS
"""

You can also use the defined locator type in a GNS file.

As here only one placeholder is used, a string needs to be supplied as the value.

Following GNS Yaml file uses the **fcn** locator:

.. code-block:: yaml

    username:
        fcn: username

    pwd:
        fcn: password

Now you can use the labels as usual in code:

.. code-block:: python

    app.gns.username
    app.gns.pwd

.. note::

    The placeholder can be used in keys too.

    Let's say you have a situation where either the name or formcontrolname is used for a given control, but the content remains same.

    .. code-block:: yaml

        username:
            wtype: attr
            wvalue:
                $$: username

    Now you can do something like this in code:

    .. code-block:: python
    
        if condition:
            app.element(username="formcontrolname")
        else:
            app.element(username="name")


**Multiple Placeholders**
^^^^^^^^^^^^^^^^^^^^^^^^^

This feature is provided for completeness sake to allow using multiple placeholders. The preferred approach is to use named placeholders when you use multiple placeholders. 

The only exception is when the placeholders share the same context, for example, all of them correspond to classes.

Definition
""""""""""

Let's say you have multiple types of buttons where **button** is a common class for all of them but other 2 classes whicha are critical for identification change from one control to another.

Let's define a **cbutton** locator to tackle this:

.. code-block:: yaml

    cbutton:
        wtype: classes
        wvalue:
            formcontrolname: button $$ $$

Coded
"""""

You can use the defined locator type in your code just like other locators in Arjuna.

As multiple placeholders are used, s list or tuple needs to be provided as value.

.. code-block:: python

    app.element(cbutton=('button-large', 'button-visible'))
    app.element(cbutton=('button-small', 'button-hidden'))

GNS
"""

You can also use the defined locator type in a GNS file.

As here only one placeholder is used, a YAML list needs to be supplied as the value.

Following GNS Yaml file uses the **cbutton** locator:

.. code-block:: yaml

    button1:
        cbutton:
            - button-large
            - button-visible

    button2:
        cbutton:
            - button-small
            - button-hidden

Now you can use the labels as usual in code:

.. code-block:: python

    app.gns.button1
    app.gns.button2


**Defining and Using** a **New Locator** with **Named Placeholders** (**$<name>$**)
-----------------------------------------------------------------------------------

Instead of anonymous/positional placeholders, you can also use named placeholders for more understandable definitions.

**Single Placeholder**
^^^^^^^^^^^^^^^^^^^^^^

Definition
""""""""""

Following is an example:

.. code-block:: yaml

    nav_link:
        wtype: xpath
        wvalue: "//li[contains(*//text(), '$lname$')]"

In the above example, a new locator type **nav_link** has been defined:
    * **wtype** key has been set to **xpath** which means that this locator extension is built on top of **xpath**. Here you can use any of :ref:`locators` or you can also use :ref:`locator_exts`.
    * **wvalue** defines the locator value and uses the corresponding GNS format (Refer :ref:`locators`)
    * **$lname$** is an example of named placeholder.


Coded
"""""

You can use the newly defined locator in your code just like other locators in Arjuna.

This locator type has one or more **$<name>$** placeholders to be formatted. This can be done using the **withx** construct.

Following code uses the **nav_link** locator extension defined in previous section:

.. code-block:: python

    wordpress.element(nav_link=withx(lname="Posts"))

Note how the placeholder name is used as a keyword argument to pass the value.

GNS
"""

You can also use the defined locator extension in a GNS file.

For named placeholders, even in case of a single placeholder, the value(s) must be supplied as a YAML mapping (key-value pairs).

Following GNS Yaml file uses the **nav_link** locator extension:

.. code-block:: yaml

    posts:
        nav_link: 
            lname: Posts

Now you can use the **posts** label as usual in code:

.. code-block:: python

    wordpress.gns.posts

**Multiple Placeholders**
^^^^^^^^^^^^^^^^^^^^^^^^^

Sometimes, the definition of a new locator is complex and contains many placeholders.

In general, it is advised that if you have more than one placeholders which don't share the same context, use named placeholders as discussed in this section.

This approach also leads to more readable (though verbose) code.


Definition
""""""""""

Consider the following example where a complex locator is defined with multiple placeholders:

.. code-block:: yaml

    dyn:
        wtype: node
        wvalue:
            $aname$: $aval$
            tags: "form $tag$"

Here, the name of attribute is dynamic along with its value. The tag sequence is also dynamic.

Coded
"""""

Following code uses the **dyn** locator extension defined in previous section:

.. code-block:: python

    app.element(dyn=withx(aname="name", aval="user", tag="input"))
    app.element(dyn=withx(aname="custom", aval="city", tag="select"))

Note how the placeholder names are used as a keyword arguments to pass the value.

GNS
"""

You can also use the defined locator extension in a GNS file.

The values must be supplied as a YAML mapping (key-value pairs).

Following GNS Yaml file uses the **nav_link** locator extension:

.. code-block:: yaml

    user:
        dyn: 
            aname: name
            aval: user
            tag: input

    city:
        dyn:
            aname: custom
            aval: city
            tag: select

Now you can use the **posts** label as usual in code:

.. code-block:: python

    app.gns.user
    app.gns.city


Defining **New Locator Locally** for a given **Gui**
----------------------------------------------------

Rather than defining locator extensions at a global level, you can also define them for a particular **GuiApp**, **GuiPage**, **GuiSection** or **GuiWidget** by defining a **withx** section in the corresponding GNS file.

Let's say you have a **LeftNav.yaml** to represent a GuiSection's externalized locators. Then you can do the following in its GNS yaml file:

.. code-block:: yaml

    withx:

        fcn:
            wtype: attr
            wvalue:
                formcontrolname: $$

        nav_link:
            wtype: xpath
            wvalue: "//li[contains(*//text(), '$lname$')]"

    labels:

        username:
            fcn: username

        posts:
            nav_link: 
                lname: Posts

Now you can use the **username** and **posts** labels as usual in code (assuming left_nav property in app GuiApp corresponds to Left navigation GuiSection object):

.. code-block:: python

    app.left_nav.gns.posts


**Mixing Anonymous/Positional ($$) and Named ($<name>$) Placeholders**
----------------------------------------------------------------------

You **CAN NOT** mix **$$ and $<name>$ placeholders** unless the named placeholders are CLR references (see :ref:`locator_auto_format`)

.. code-block:: yaml

    # INVALID
    loc1:
        wtype: node
        wvalue:
            abc: $$
            xyz: $whatever$

    # VALID
    loc2:
        wtype: node
        wvalue:
            abc: $$
            xyz: $C.whatever$

    loc3:
        wtype: node
        wvalue:
            abc: $$
            xyz: $L.whatever$

    loc4:
        wtype: node
        wvalue:
            abc: $$
            xyz: $R.whatever.something$
