.. _response:

Analyzing HTTP Response
=======================

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
