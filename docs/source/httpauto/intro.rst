.. _intro:

Introduction
============

Automating at HTTP Layer
------------------------

Test automation at the HTTP layer in case of web applications and services is increasingly becoming popular and rightly so. 

At HTTP layer, you get faster and more stable test automation.

Arjuna supports writing tests at this layer by wrapping various related Python modules (primarily `requests` and `requests_oauthlib`), all in one framework.

**Note** This is currently a beta quality feature. The TPI for the classes and functions is fairly finalized, but prone to minor changes and extensions.

Arjuna's **Http Facade Class**
------------------------------

Arjuna provides you with :py:class:`Http <arjuna.tpi.httpauto.http.Http>` as the facade class to start with HTTP automation.

Its features include sending various HTTP method requests, creating a session of requests, handling content types and so on.

Supported HTTP Methods in Arjuna
--------------------------------

Currently the following HTTP methods/verbs are supported:
    * :py:func:`GET <arjuna.tpi.httpauto.http.Http.get>`
    * :py:func:`POST <arjuna.tpi.httpauto.http.Http.post>`
    * :py:func:`PUT <arjuna.tpi.httpauto.http.Http.put>`
    * :py:func:`DELETE <arjuna.tpi.httpauto.http.Http.delete>`
    * :py:func:`HEAD <arjuna.tpi.httpauto.http.Http.head>`
    * :py:func:`OPTIONS <arjuna.tpi.httpauto.http.Http.options>`
    * :py:func:`PATCH <arjuna.tpi.httpauto.http.Http.patch>`

Basic GET Example
-----------------
Simulating a request with a given HTTP method is achieved by making correspindingly named methods in :py:class:`Http <arjuna.tpi.httpauto.http.Http>`.

Following is an example of a basic GET request:

    .. code-block:: python

        Http.get("https://another.com/api/res/someid1")
        Http.get("https://another.com/api/res/someid2")

HTTP Response
-------------
All types of requests return an :py:class:`HttpResponse <arjuna.tpi.httpauto.session.HttpResponse>` object, which can be inquired to validate or extract data.

Customizing HTTP Requests
-------------------------
You can set custom headers and content type for invidual requests. Explore the :py:class:`Http <arjuna.tpi.httpauto.http.Http>` class documentation.
