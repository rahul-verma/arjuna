.. _http_service:

**SEAMful: Service**
====================

Beyond basic automation, you will need to send requests as a part of the same session so that cookie management is done automatically for you.

Along with this you also get other benefits in the form of common settings across all requests that are sent as a part of this session.

Arjuna's :py:class:`HttpService <arjuna.tpi.httpauto.service.HttpService>` class offers this style of automation in an approachable and comprehensive manner.

Creating an **HTTP Service**
----------------------------

.. _anon_http_service:

**Anonymous Service**
^^^^^^^^^^^^^^^^^^^^^

You can create a new service using :py:func:`Http.service <arjuna.tpi.httpauto.http.Http.service>` method to create an object of :py:class:`HttpSerive <arjuna.tpi.httpauto.service.HttpService>`.

Following is an example of the most basic construct for creating an HttpService:

    .. code-block:: python

        svc = Http.service(url="https://svc.com/api")

The **url** argument sets the base/default URL for this HttpService. If relative path is used as a route in sender methods like `get()`, then this URL is prefixed to their provided routes.

.. _named_http_service:

**Named Service**
^^^^^^^^^^^^^^^^^

You can also create a named service, which is critical if you are planning to do more involved implementations for :ref:`seamful`.

Following is an example of the most basic construct for creating a named HttpService:

    .. code-block:: python

        svc = Http.service(name="myservice", url="https://svc.com/api")

A named service must have a corresponding directory with the same name in **<Project Root>/httpauto/service** directory. For example

    .. code-block:: yaml

        myproj
          - httpauto
            - service
              - myservice


All the sections that follow are applicable for anonymous as well as named services.

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


.. _request:

Customizing HTTP Requests
-------------------------
You can customize various parts of the HTTP requests using easy to use constructs as described in the following sections.

Handling **Content Types** in **POST/PUT/PATCH** Requests
---------------------------------------------------------

Purpose
^^^^^^^

POST/PUT/PATCH HTTP requests have content/body as a part of the HTTP packet which is sent.

This content is ultimately sent as plain text. So, Arjuna converts the content object to text before sending it to the HTTP server.

URL-Encoding as Default Content Type
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

By default Arjuna takes a dictionary (or other dictionary-like objects) as a content and uses URL-Encoding to convert it to text.

    .. code-block:: python

        # Content sent as URL encoded
        svc.post("http://abc.com/res", content={'a' : 1, 'b': 2}) 
        svc.put("http://abc.com/res", content={'a' : 1, 'b': 2})

For example, in the above code, the provided dictionary is converted to the following:

    .. code-block:: text

        a=1&b=2

In addition, the **Content-Type** header is set to **application/x-www-form-urlencoded**.

Specifying Content-Handlers
^^^^^^^^^^^^^^^^^^^^^^^^^^^

Http class provides various content specifiers. You can use any of the following:
    * :py:func:`Http.content.html <arjuna.tpi.httpauto.http.Http.content.html>`: Content-Type is sent as "text/html".
    * :py:func:`Http.content.text <arjuna.tpi.httpauto.http.Http.content.text>`: Content-Type is sent as "text/html".
    * :py:func:`Http.content.bytes <arjuna.tpi.httpauto.http.Http.content.bytes>`: Content-Type is sent as "text/html".
    * :py:func:`Http.content.utf8 <arjuna.tpi.httpauto.http.Http.content.utf8>`: Content-Type is sent as "text/html".
    * :py:func:`Http.content.urlencoded <arjuna.tpi.httpauto.http.Http.content.urlencoded>`: Content-Type is sent as "application/x-www-form-urlencoded".
    * :py:func:`Http.content.json <arjuna.tpi.httpauto.http.Http.content.json>`: Content-Type is sent as "application/json".
    * :py:func:`Http.content.xml <arjuna.tpi.httpauto.http.Http.content.xml>`: Content-Type is sent as "application/xml".
    * :py:func:`Http.content.file <arjuna.tpi.httpauto.http.Http.content.file>`: Content-Type is sent as the content type got from multipart encoding.
    * :py:func:`Http.content.multipart <arjuna.tpi.httpauto.http.Http.content.multipart>`: Content-Type is sent as the content type got from multipart encoding.
    * :py:func:`Http.content.custom <arjuna.tpi.httpauto.http.Http.content.custom>`: Content-Type is sent as specified.

Following is a simple example of sending JSON content:

    .. code-block:: python

        # Content sent as serialized JSON
        svc.post("http://abc.com/res", content=Http.content.json({'a' : 1, 'b': 2}))

In the above example, the content will be sent as following:

    .. code-block:: text

        {"a" : 1, "b": 2}

In addition, the **Content-Type** header is set to **application/json**.

Using **HttpService**'s **request_content_handler** Global Handler
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Arjuna's HttpService object makes content handling very straight-forward as you will mostly likely use the same content handling type across multiple requests.

You can set the content handler in one go across all the requests that are sent by a given session.

    ..  code-block:: python

        svc = Http.service(url="http://abc.com", request_content_handler=Http.content.json)
        svc.post("/res1", content={'a' : 1, 'b': 2})
        svc.post("/res2", content={'c' : 1, 'd': 2})
        svc.post("/res3", content={'e' : 1, 'f': 2})

Setting a **Request Label**
---------------------------

All service request methods accept a `label` argument. This is used in reports and logging to give a user-defined representation of an HTTP request.

Following are basic examples of these calls:

    .. code-block:: python

        svc.get("/api/res/someid", label="Authorization Request")


Setting **Arbitrary Query String Parmaters** in URL
---------------------------------------------------

A common need in HTTP automation is to set the query parameters in the URL.

One can ofcourse do it with Python string formatting. However, Arjuna makes it easier fpr url-encoded params, the most commonly used format.

You can achieve this for all types of service requests. Following is a get example, where arbitrary key-value arguments are passed to become query parameters:

    .. code-block:: python

        svc.get("https://app.com/somepath", a=1, something="test")

In the above example, the URL will be

    .. code-block:: text

        https://another.com/somepath?a=1&something=test

Sometimes, the names in query string are not valid Python names and hence can not be passed as keyword arguments. You can use **quer_params** argument in such situations.

    .. code-block:: python

        svc.get("https://app.com/somepath", query_params={'nonpy-name':1, 'something':"test"})


If used in combinations, the keyword arugments will override the values in **query_params**

    .. code-block:: python

        svc.get("https://app.com/somepath", query_params={'a':1, 'something':"test"}, a=2)

In the above case, the value of a will be 2:

    .. code-block:: text

        https://another.com/somepath?a=2&something=test

.. _response:

Analyzing HTTP Response
-----------------------

Test automation code is not just about interactions with HTTP server. You will typicallly place various checks on what it responds with for a given request.

Arjuna provides various easy to use features for this purpose.

Checking **Expected HTTP Status Code(s)**
-----------------------------------------

**Inquiring**
^^^^^^^^^^^^^

Status code can be easily inquired:

    .. code-block:: python

        response = svc.get("/obj/someid")
        print(response.status_code)    


**Asserting**
^^^^^^^^^^^^^

You can also assert status codes by inquiring `HttpResponse` object as follows:

    .. code-block:: python

        response = svc.get("/obj/someid")
        response.assert_status_codes(200, msg="Your context string")
        response.assert_status_codes({200, 404}, msg="Your context string")


**xcodes** Argument
^^^^^^^^^^^^^^^^^^^

You can set a session request to raise an `HttpUnexpectedStatusCode` exception if expected status code is not got:

    .. code-block:: python

        svc.get("/obj/someid", xcodes=200)


**xcodes** Argument in **strict** Mode
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

You can set a session request to raise an `AssertionError` exception if expected status code is not got:

    .. code-block:: python

        svc.get("/obj/someid", xcodes=200, strict=True)


The **HttpResponse** Object
---------------------------

If a session request is successful it returns an :py:class:`HttpResponse <arjuna.tpi.httpauto.session.HttpResponse>` object.

It provides you with various properties to assert or extract data.

Basic **Data Extraction**
^^^^^^^^^^^^^^^^^^^^^^^^^

You can easily extract the following data using response properties:

    .. code-block:: python

        #Response headers
        response.headers

        # Status Code
        response.status_code

        # Status Message
        response.status

        # Request Information
        # In case of redirects, this is for the last request
        response.request
        response.url
        response.query_params

**Redirections**
^^^^^^^^^^^^^^^^

An :py:class:`HttpResponse <arjuna.tpi.httpauto.session.HttpResponse>` object maintains all redirect history.

You can get a sequence of all redirect :py:class:`HttpResponse <arjuna.tpi.httpauto.session.HttpResponse>` objects using `redir_history` property.

You can get the last redirect response using `last_redir_response` property.

Handling **Response Content**
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

You can get formatted as well as un-formatted response content using following properties:
    * `text`: Unformatted content as plain text
    * `html`: Response as an :py:class:`HtmlNode <arjuna.tpi.parser.html.HtmlNode>` object.
    * `json`: Response as a :py:class:`JsonDict <arjuna.tpi.parser.json.JsonDict>` or :py:class:`JsonList <arjuna.tpi.parser.json.JsonList>` object.

Check **Parsing JSON, XML, HTML Files and Strings** section in documentation to know more about how to parse and extract data from these content type.
