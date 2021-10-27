.. _security_http_builtin:

**Simple Built-in HTTP Layer Security Tests** for **GET** Requests
==================================================================

Introduction
------------

Arjuna makes conducting various security tests very straight-foward.

For this purpose, Arjuna makes various HTTP actions directly available to all HTTP services and end-points created using its :ref:`seamful`.

This section discusses tests which can be conducted for requests that use HTTP **GET** method.

**Auto-complete** Should be Disabled
------------------------------------

Auto complete field in an HTML form are a security vulnerability as it could lead to sensitive information stored in browser cache. In systems which are used by multiple users, one user's information could be leaked to another user including passwords.

Validate Auto-compelete Off for a Form
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

You can check whether autocomplete is off by using **autocomplete_form** HTTP action.

.. code-block:: python

    service.action.autocomplete_form.perform(
        route="/a/b/c",
        form="login-form"
    )

* **route** is the absolute or relative URI.
* **form** is the value of the **id** field in HTML for this form.

You can also use some other attribute like **name** by using the **attr** argument:

.. code-block:: python

    service.action.autocomplete_form.perform(
        route="/a/b/c",
        attr="name",
        form="login-form"
    )

Validate Auto-compelete Off for a Field
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

You can check whether autocomplete is off for a field by using **autocomplete_field** HTTP action.

This action checks whether the autocomplete is off at a field level or for its containing form.

.. code-block:: python

    service.action.autocomplete_field.perform(
        route="/a/b/c",
        form="login-form",
        field="some-field-id"
    )

* **route** is the absolute or relative URI.
* **form** is the value of the **id** field in HTML for this form.
* **field** is the value of the **id** field in HTML for this field.

You can also use some other attribute like **name** by using the **attr** argument:

.. code-block:: python

    service.action.autocomplete_field.perform(
        route="/a/b/c",
        attr="name",
        form="login-form",
        field="some-field-id"
    )

**Private Resource** Disclosure
-------------------------------

Some resources are not meant for public consumption.

However, at times by configuration or deployment mistakes, they become accessible. An example is that if debug configuration is not switched off in public deployment, an internal debugging link could be exposed leading to critical information disclosure.

As it is a common occurence, Arjuna let's you validate this using **private_resource** HTTP action.

.. code-block:: python

    service.action.private_resource.perform(
        route="/a/b/c",
    )

* **route** is the absolute or relative URI.

**Private IP** Disclosure
-------------------------

HTML responses might contain Private IPs and this considered an information disclosure vulnerability.

Arjuna let's you validate this using **private_ip_disc** HTTP action.

.. code-block:: python

    service.action.private_ip_disc.perform(
        route="/a/b/c",
    )

* **route** is the absolute or relative URI.

**Cross-Origin Resource Sharing (CORS)**
----------------------------------------

A server must restrict origins other than itself from where its resources can be loaded by a browser.

Arjuna let's you validate this using **cors_policy** HTTP action.

.. code-block:: python

    service.action.cors_policy.perform(
        route="/a/b/c",
    )

* **route** is the absolute or relative URI.


**Frameable Response** (Potential **Clickjacking**)
---------------------------------------------------

A malicious website can embed a server's response and carry out clickjacking attacks.

A server should disbale its responses to be frameable.

Arjuna let's you validate this using **frameable_response** HTTP action.

.. code-block:: python

    service.action.frameable_response.perform(
        route="/a/b/c",
    )

* **route** is the absolute or relative URI.

**Strict Transport Policy**
---------------------------

Implementation of strict transport policy forces browsers to load the content only using HTTPS (encrypted) for a server.

Arjuna let's you validate this using **strict_transport** HTTP action.

.. code-block:: python

    service.action.strict_transport.perform(
        route="/a/b/c",
    )

* **route** is the absolute or relative URI.

**Information Disclosure**
--------------------------

Many a times HTTP response contents have sensitive information. An example can be a detailed error trace divulging database table names.

Arjuna let's you validate this using **info_disc** HTTP action.

You can pass a regular Python string or a regular expression for a match.

.. code-block:: python

    service.action.info_disc.perform(
        route="/a/b/c",
        regex="\\d+(Some pattern)"
    )

* **route** is the absolute or relative URI.
* **regex** is a plain string or regular expression.

.. note::
    As the regular expession is used to format an internal YAML file duing pre-loading, you'd need to double escape in regular expressions.

    To avoid this, use Python raw string and use single escaping as demonstrated above.

**Minium Secure JS Version**
----------------------------

Many a times, applications use JavaScript library versions that have known vulnerabilities.

Arjuna let's you validate minimum secure JavaScript library version using **min_js_version** HTTP action.

You can pass a a regular expression for a match. Put parenthesis around the version part to enable proper extraction. 

.. code-block:: python

    service.action.min_js_version.perform(
        route="/a/b/c",
        regex=r"jQuery\\s+v(.*?)\\s+",
        min="3.5.1"
    )

* **route** is the absolute or relative URI for the JavaScript file.
* **regex** is the regular expression for extracting JS version.
* **min** is the minimum expected secure JavaScript library version.

.. note::
    As the regular expession is used to format an internal YAML file during pre-loading, you'd need to double escape in regular expressions.

    To avoid this, use Python raw string and use single escaping as demonstrated above.

**Vulnerable JS Version**
-------------------------

Sometimes, rather than checking a minium secure version, you might want to directly check for a vulberable version of a JavaScript library being used.

Arjuna let's you validate this using **vulnerable_js_version** HTTP action.

You can pass a a regular expression for a match.

.. code-block:: python

    service.action.min_js_version.perform(
        route="/a/b/c",
        regex=r"jQuery\\s+v(3.0.0)\\s+"
    )

* **route** is the absolute or relative URI for the JavaScript file.
* **regex** is the regular expression for macthing JS version.

.. note::
    As the regular expession is used to format an internal YAML file during pre-loading, you'd need to double escape in regular expressions.

    To avoid this, use Python raw string and use single escaping as demonstrated above.

**Cookie - HttpOnly Flag**
--------------------------

Cookies containing sensitive data should have HttpOnly flag set to prevent them to be accessed by client side JavaScript.

This prevents from an abuse case in case Cross Site Scripting vulberabilties are present in the application.

Arjuna let's you validate this using **cookie_httponly** HTTP action.

.. code-block:: python

    service.action.cookie_httponly.perform(
        route="/a/b/c",
        name="some_cookie_name"
    )

* **route** is the absolute or relative URI for the JavaScript file.
* **name** is the name of the cookie.

**Cookie - secure Flag**
------------------------

Cookies containing sensitive data must be sent by browser only on secure connection.

Arjuna let's you validate this using **cookie_secure** HTTP action.

.. code-block:: python

    service.action.cookie_secure.perform(
        route="/a/b/c",
        name="some_cookie_name"
    )

* **route** is the absolute or relative URI for the JavaScript file.
* **name** is the name of the cookie.

.. note::

    This test should be conducted **after** the server has issued the cookies.