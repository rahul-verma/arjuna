.. _session:

**HTTP Service**
================

Beyond basic automation, you will need to send requests as a part of the same session so that cookie management is done automatically for you.

Along with this you also get other benefits in the form of common settings across all requests that are sent as a part of this session.

Arjuna's :py:class:`HttpService <arjuna.tpi.httpauto.service.HttpService>` class offers this style of automation in an approachable and comprehensive manner.

Creating an **HTTP Service**
----------------------------

You can create a new service using :py:func:`Http.service <arjuna.tpi.httpauto.http.Http.service>` method to create an object of :py:class:`HttpSerive <arjuna.tpi.httpauto.service.HttpService>`.

Following is an example of the most basic construct for creating an HttpService:

    .. code-block:: python

        svc = Http.service(url="https://svc.com/api")

The **url** argument sets the base/default URL for this HttpService. If relative path is used as a route in sender methods like `get()`, then this URL is prefixed to their provided routes.

Supported HTTP Methods in Arjuna
--------------------------------

Currently the following HTTP methods/verbs are supported:
    * :py:func:`GET <arjuna.tpi.httpauto.service.HttpService.get>`
    * :py:func:`POST <arjuna.tpi.httpauto.service.HttpService.post>`
    * :py:func:`PUT <arjuna.tpi.httpauto.service.HttpService.put>`
    * :py:func:`DELETE <arjuna.tpi.httpauto.service.HttpService.delete>`
    * :py:func:`HEAD <arjuna.tpi.httpauto.service.HttpService.head>`
    * :py:func:`OPTIONS <arjuna.tpi.httpauto.service.HttpService.options>`
    * :py:func:`PATCH <arjuna.tpi.httpauto.service.HttpService.patch>`

Basic GET Example
-----------------
Simulating a request with a given HTTP method is achieved by making correspindingly named methods in :py:class:`Http <arjuna.tpi.httpauto.service.HttpService>` object.

Following is an example of a basic GET request:

    .. code-block:: python

        svc = Http.service(url="https://svc.com/api")

        # Using absolute routes in requests
        svc.get("https://svc.com/api/res/someid1")
        svc.get("https://svc.com/api/res/someid2")

        # With relative route. Base/Default URL of Session is prefixed.
        svc.delete("/res/someid1") # Same as https://svc.com/api/res/someid1
        svc.delete("/res/someid2") # Same as https://svc.com/api/res/someid2

HTTP Response
-------------
All types of requests return an :py:class:`HttpResponse <arjuna.tpi.httpauto.response.HttpResponse>` object, which can be inquired to validate or extract data.

Customizing HTTP Requests
-------------------------
You can add request headers, add OAuth bearer token, set default content handler and so on. Explore the :py:class:`HttpService <arjuna.tpi.httpauto.service.HttpService>` class documentation.
