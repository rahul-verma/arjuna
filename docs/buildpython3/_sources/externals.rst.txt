.. _help_third_party:


Introduction
------------

Arjuna uses a lot of third party libraries to provide its functionality:

    * lxml
    * requests
    * requests-toolbelt
    * selenium
    * webdriver_manager
    * xlrd
    * xlwt
    * pyparsing
    * pyhocon
    * pytest
    * pytest-html
    * pytest-dependency
    * PyYAML
    * mimesis
    * jsonpath-rw
    * jsonpath-rw-ext
    * genson
    * jsonschema
    * Pallets-Sphinx-Themes
    * oauthlib
    * requests_oauthlib
    * bs4
    * browsermob-proxy
    * haralyzer
    * mysql-connector-python

Some of this is completely wrapped which means you need not worry about them. 

However, some libraries like pytest, selenium or PyYAML etc have an indirect impact on the way testers write code or create input files in Arjuna.

This section contains helpful information about such libraries.

Beware of the Boolean Interpretation in YAML
--------------------------------------------

YAML specification as used by PyYAML converts many strings to their boolean counterparts (True/False). Arjuna uses YAML for most of its input file formats. When you are creating such YAML files, you need to be aware of this YAML parsing behavior.

One example is let's say you use a locator in GNS files where value of attribute **abc** is **Yes**. You end up writing something like following in GNS:

.. code-block:: YAML

    labels:

        some_button:
            fattr:
                abc: Yes

What you later see is that there is an error in finding the element and the corresponding CSS Selector generated is shown as the following in exception message:

.. code-block:: javascript

    *[abc='True']

The above CSS Selector is obviously not what you intented for the situation. What you meant was:

.. code-block:: javascript

    *[abc='Yes']

This is because of YAML's support for intuitively converting some string literals to boolean. Following are some strings that are converted to True/False by PyYAML:

.. code-block:: YAML

    a: Yes
    b: y
    c: n
    d: No
    e: on
    f: off

.. note::

    Following is the regex from YAML 1.1 specification:

    .. code-block:: python

     y|Y|yes|Yes|YES|n|N|no|No|NO|true|True|TRUE|false|False|FALSE|on|On|ON|off|Off|OFF

As a rule of thumb:
    - For true/false, when you mean boolean, use True/true/False/false.
    - For other strings mentioned above or when you mean True/true/False/false as strings, then provide them in quotes.

.. code-block:: YAML

    # as string
    a: "y"

    # True as boolean
    b: True

    # True as string
    c: "True"

