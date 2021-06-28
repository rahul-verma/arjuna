.. _request:

Customizing HTTP Requests
=========================

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
        Http.post("http://abc.com/res", content={'a' : 1, 'b': 2}) 
        Http.put("http://abc.com/res", content={'a' : 1, 'b': 2})

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
        Http.post("http://abc.com/res", content=Http.content.json({'a' : 1, 'b': 2}))

In the above example, the content will be sent as following:

    .. code-block:: text

        {"a" : 1, "b": 2}

In addition, the **Content-Type** header is set to **application/json**.

Using **HttpSession**'s **request_content_handler** Global Handler
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Arjuna's HttpSession object makes content handling very straight-forward as you will mostly likely use the same content handling tpye across multiple requests.

You can set the content handler in one go across all the requests that are sent by a given session.

So, instead of doing this

    ..  code-block:: python

        Http.post("http://abc.com/res1", content=Http.content.json({'a' : 1, 'b': 2}))
        Http.post("http://abc.com/res2", content=Http.content.json({'c' : 1, 'd': 2}))
        Http.post("http://abc.com/res3", content=Http.content.json({'e' : 1, 'f': 2}))

you can do the following

    ..  code-block:: python

        svc = Http.session(url="http://abc.com", request_content_handler=Http.content.json)
        svc.post("/res1", content={'a' : 1, 'b': 2})
        svc.post("/res2", content={'c' : 1, 'd': 2})
        svc.post("/res3", content={'e' : 1, 'f': 2})

Setting a **Request Label**
---------------------------

All session request methods accept a `label` argument. This is used in reports and logging to give a user-defined representation of an HTTP request.

Following are basic examples of these calls:

    .. code-block:: python

        svc.get("/api/res/someid", label="Authorization Request")


Setting **Arbitrary Query String Parmaters** in URL
---------------------------------------------------

A common need in HTTP automation is to set the query parameters in the URL.

One can ofcourse do it with Python string formatting. However, Arjuna makes it easier fpr url-encoded params, the most commonly used format.

You can achieve this for all types of session requests. Following is a get example, where arbitrary key-value arguments are passed to become query parameters:

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
