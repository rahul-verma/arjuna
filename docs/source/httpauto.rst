.. _httpauto:

HTTP Automation
===============

Test automation at the HTTP layer in case of web applications and services is increasingly becoming popular and rightly so. 

At HTTP layer, you get faster and more stable test automation.

Arjuna supports writing tests at this layer by wrapping various related Python modules (primarily `requests` and `requests_oauthlib`), all in one framework.

**Note** This is currently a beta quality feature. The TPI for the classes and functions is fairly finalized, but prone to minor changes and extensions.


Making HTTP Requests with **HttpSession**
-----------------------------------------

Arjuna provides :py:class:`HttpSession <arjuna.tpi.httpauto.session.HttpSession>` class to create an HTTP session, which automatically manages cookies.

Following is an example of the most basic construct for creating an HttpSession:

    .. code-block:: python

        svc = HttpSession(url="https://svc.com/api")


The **url** argument sets the base/default URL for this HttpSession. If relative path is used as a route in sender methods like `get()`, then this URL is prefixed to their provided routes.

You can add request headers, add OAuth bearer token, set default content type and so on. Explore the :py:class:`HttpSession <arjuna.tpi.httpauto.session.HttpSession>` class documentation.

Supported HTTP Methods 
----------------------

Currently :py:func:`GET <arjuna.tpi.httpauto.session.HttpSession.get>`, :py:func:`POST <arjuna.tpi.httpauto.session.HttpSession.post>`, :py:func:`PUT <arjuna.tpi.httpauto.session.HttpSession.put>` and :py:func:`DELETE <arjuna.tpi.httpauto.session.HttpSession.delete>` methods/verbs in HTTP are supported.

Simulating a request with a given HTTP method is achieved by making correspindingly named methods in :py:class:`HttpSession <arjuna.tpi.httpauto.session.HttpSession>`.

Following are basic examples of these calls:

    .. code-block:: python

        svc.get("https://another.com/api/res/someid")
        # With relative route. Base/Default URL of Session is prefixed.
        svc.get("/res/someid") 

        svc.delete("/res/someid")

        # Content sent as URL encoded or session's default content type
        svc.post("/res", content={'a' : 1, 'b': 2}) 
        # Content sent as serialized JSON
        svc.post("/res", content={'a' : 1, 'b': 2}, content_type="application/json") 

        svc.put("/res", content={'a' : 1, 'b': 2})

All types of requests return an :py:class:`HttpResponse <arjuna.tpi.httpauto.session.HttpResponse>` object, which can be inquired to validate or extract data.

You can set custom headers and content type for invidual requests. Explore the :py:class:`HttpSession <arjuna.tpi.httpauto.session.HttpSession>` class documentation.

Setting a Request Label
-----------------------

All session request methods accept a `label` argument. This is used in reports and logging to give a user-defined representation of an HTTP request.

Following are basic examples of these calls:

    .. code-block:: python

        svc.get("/api/res/someid", label="Authorization Request")


Setting Arbitrary Query String Parmaters in URL
-----------------------------------------------

A common need in HTTP automation is to set the query parameters in the URL.

One can ofcourse do it with Python string formatting. However, Arjuna makes it easier fpr url-encoded params, the most commonly used format.

You can achieve this for all types of session requests. Following is a get example, where arbitrary key-value arguments are passed to become query parameters:

    .. code-block:: python

        svc.get("https://app.com/somepath", a=1, something="test")

In the above example, the URL will be

    .. code-block:: text

        https://another.com/somepath?a=1&something=test


Checking Expected HTTP Status Code(s)
-------------------------------------

Inquiring
^^^^^^^^^

Status code can be easily inquired:

    .. code-block:: python

        response = svc.get("/obj/someid")
        print(response.status_code)    


Asserting
^^^^^^^^^

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

Basic Data Extraction
^^^^^^^^^^^^^^^^^^^^^

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

Redirections
^^^^^^^^^^^^

An `HttpResponse` object maintains all redirect history.

You can get a sequence of all redirect `HttpResponse` objects using `redir_history` property.

You can get the last redirect response using `last_redir_response` property.

Handling Response Content
^^^^^^^^^^^^^^^^^^^^^^^^^

You can get formatted as well as un-formatted response content using following properties:
    * `text`: Unformatted content as plain text
    * `html`: Response as an :py:class:`HtmlNode <arjuna.tpi.helper.html.HtmlNode>` object.
    * `json`: Response as a :py:class:`JsonDict <arjuna.tpi.helper.json.JsonDict>` or :py:class:`JsonList <arjuna.tpi.helper.json.JsonList>` object.

Check **Parsing JSON, XML, HTML Files and Strings** section in documentation to know more about how to parse and extract data from these content type.

Support for Open Authentication (OAuth)
---------------------------------------

Arjuna supports the following OAuth grant types with its custom HTTP session objects:


OAuth Client Grant Session
^^^^^^^^^^^^^^^^^^^^^^^^^^

It wraps the `BackendApplicationClient` object from `requests_oauthlib` package.

Once created, the session supports all methods in :py:class:`HttpSession <arjuna.tpi.httpauto.session.HttpSession>` object discussed above.

Explore :py:class:`OAuthClientGrantSession <arjuna.tpi.httpauto.oauth.OAuthClientGrantSession>` for constructor.

OAuth Implicit Grant Session
^^^^^^^^^^^^^^^^^^^^^^^^^^^^

It wraps the `MobileApplicationClient` object from `requests_oauthlib` package.

Once created, the session supports all methods in :py:class:`HttpSession <arjuna.tpi.httpauto.session.HttpSession>` object discussed above.

Explore :py:class:`OAuthImplicitGrantSession <arjuna.tpi.httpauto.oauth.OAuthImplicitGrantSession>` for constructor.

Creating a New Session from an OAuth Session
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Many a times, you will want to reuse the OAuthToken to connect to multiple services for testing.

Rather than creating a token each time, you can create it once by creating :py:class:`OAuthClientGrantSession <arjuna.tpi.httpauto.oauth.OAuthClientGrantSession>` or :py:class:`OAuthImplicitGrantSession <arjuna.tpi.httpauto.oauth.OAuthImplicitGrantSession>`.

Now you can use this OAuth session to create a new `HttpSession` object for any base URL using `create_new_session` call.

    .. code-block:: python

        oauth_session.create_new_session("https://someapp.com/api")










