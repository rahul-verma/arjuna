.. _session:

**HTTP Session**
================

Beyond basic automation, you will need to send requests as a part of the same session so that cookie management is done automatically for you.

Along with this you also get other benefits in the form of common settings across all requests that are sent as a part of this session.

Creating an **HTTP Session**
----------------------------

You can create a new session using :py:func:`Http.session <arjuna.tpi.httpauto.http.Http.session>` method to create an object of :py:class:`HttpSession <arjuna.tpi.httpauto.session.HttpSession>`.

It supports all the HTTP methods that are supported by :py:class:`Http <arjuna.tpi.httpauto.http.Http>` class.

Following is an example of the most basic construct for creating an HttpSession:

    .. code-block:: python

        svc = Http.session(url="https://svc.com/api")

The **url** argument sets the base/default URL for this HttpSession. If relative path is used as a route in sender methods like `get()`, then this URL is prefixed to their provided routes.

Basic GET Example
-----------------
Simulating a request with a given HTTP method is achieved by making correspindingly named methods in :py:class:`Http <arjuna.tpi.httpauto.http.Http>`.

Following is an example of a basic GET request:

    .. code-block:: python

        svc.get("https://svc.com/api/res/someid1")
        svc.get("https://svc.com/api/res/someid2")

        # With relative route. Base/Default URL of Session is prefixed.
        Http.delete("/res/someid1") # Same as https://svc.com/api/res/someid1
        Http.delete("/res/someid2") # Same as https://svc.com/api/res/someid2

HTTP Response
-------------
All types of requests return an :py:class:`HttpResponse <arjuna.tpi.httpauto.session.HttpResponse>` object, which can be inquired to validate or extract data.

Customizing HTTP Requests
-------------------------
You can add request headers, add OAuth bearer token, set default content handler and so on. Explore the :py:class:`HttpSession <arjuna.tpi.httpauto.session.HttpSession>` class documentation.
