.. _seam_message:

**SEAMful - Message**
=====================

Introduction
------------

In addition to the coded way discussed in :ref:`http_service` documentation, Arjuna's **HttpService** object can read and send abstracted Http messages in YAML based externalization files.

In addition, any checks and extractions specified in the YAML file are also performed.

Defining **Messages** with **Anonymous Service**
------------------------------------------------

The message files are placed under **<Arjuna Test Project root dir>/httpauto/message** directory.

    .. code-block:: yaml

        myproj
          - httpauto
            - message
              - mymsg1.yaml
              - mymsg2.yaml


Defining **Messages** with **Named Service**
--------------------------------------------

The message files are placed under **<Arjuna Test Project root dir>/httpauto/service/<service_name>/message** directory.

    .. code-block:: yaml

        myproj
          - httpauto
            - service
              - myservice
                - message
                  - mymsg1.yaml
                  - mymsg2.yaml


Sending **Message using Service**
---------------------------------
Depending on whether the message file name is a valid Python name or not, you can use the following ways to send this HTTP message using the service:

    .. code-block:: python

        # Python name
        service.message.mymsg1.send()

        # Invalid Python name
        service.send("non python name")
        service.send("non/python/name") # With sub-directories

The service will look for the correspinding message in **<Arjuna Test Project root dir>/httpauto/message** or **<Arjuna Test Project root dir>/httpauto/service/<service_name>/message** directory depending on whether it is an anonymous service or named service respectively.

It will then send the corresponding HTTP message as per specification.

Blank Message File
------------------

A blank message file means the following:
    * Send a GET request
    * Route is the root of session i.e. same as default URL of HttpService object
    * Perform no checks on response

Technically it means the same as following:

    .. code-block:: python

        svc.message.send()
        # or
        svc.send()

GET is default method
---------------------

The following YAML

    .. code-block:: yaml

        request:
            route: "/get"

will send a GET request to **<session_url>/get**

Checking **Response Codes**
---------------------------

Aseerting Expected Response Codes
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

To check expected status code, you can specificy **codes** key.

The following YAML

    .. code-block:: yaml

        request:
            method: get
            route: "/get"

        codes: 200

will send a GET request to **<session_url>/get** and validate whether HTTP status code is 200.

You can also specify multiple status codes:

    .. code-block:: yaml

        codes:
            - 200
            - 201

Asserting Unexpected Response Codes
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

To check unexpected status code, you can specificy **codes** key under **unexpected** section.

The following YAML

    .. code-block:: yaml

        request:
            method: get
            route: "/get"

        unexpected:
            codes: 404

will send a GET request to **<session_url>/get** and validate whether HTTP status code **is not** 404.

You can also specify multiple status codes:

    .. code-block:: yaml

        unexpectd:
            codes:
                - 404
                - 500

Specifying **Request Label**
----------------------------

Just as in case of coded requests, Arjuna's test report can label requests for HTTP messages when network capturing is enabled.

You can use **label** construct in YAML as follows

    .. code-block:: yaml

        label: Simple Get

        request:
            method: get
            route: "/get"

        codes: 200

The label will also be used to increase the usefulness of exception messages to help in troubleshooting.

Sending Arbitrary Key-Values in **Query String**
------------------------------------------------

You can add arbitrary key values pairs in **request** section. These will be sent in query string in URL encoded format.

The following YAML

    .. code-block:: yaml

        request:
            method: get
            route: "/get"
            a: b
            c: d

        codes: 200

will send a GET request to **<session_url>/get?a=b&c=d** and validate whether HTTP status code is 200.

You can also specify whether the key-value pairs need to be sent in pretty-url format.

The following YAML

    .. code-block:: yaml

        request:
            method: get
            route: "/get"
            a: b
            c: d
            pretty_url: True

        codes: 200

will send a GET request to **<session_url>/get/a/b/c/d** and validate whether HTTP status code is 200.

**Dynamic Messages** using Arjuna's **$<name>$** Placeholders
-------------------------------------------------------------

Basic Formatting
^^^^^^^^^^^^^^^^

You can specify the YAML in a dynamic way so that you can pass data to it from code.

.. note:: 

    Arjuna will use the data to format the raw YAML text before loading it as YAML object.

For example

    .. code-block:: yaml

        label: Check creating of item

        request:
            method: post
            route: "/item"

        content_type: json
        
        content: {
            'name': "$name$",
            'price': "$price$"
        }

        codes: 200

in the above YAML specifies **$url$** and **$price$** plaecholders.

You can pass values to these named placeholders as follows (assume abc.yaml as the message file name)

    .. code-block:: python

        svc.mymsg.send(name="something", price=121)

Here **url** construct is used to validate the URL for which the response was yielded.

Using **data** Formatting Container with Dictionary
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Rather than passing individual values for formatting, you can also send all of them as a Python dictiionary:

    .. code-block:: python

        inputs = {'name'='something', price=121}

        svc.mymsg.send(**inputs)
        # is same as
        svc.mymsg.send(data=inputs)

In the yaml, you can now use:

    .. code-block:: yaml
        
        content: {
            'name': "$data.name$",
            'price': "$data.price$"
        }

Arjuna's formatter for look a name in directly supplied arguments and if not found then in the container named **data**. So, even the following is valid:

    .. code-block:: yaml

        content: {
            'name': "$name$",
            'price': "$price$"
        }

Handling **Content Type**
-------------------------

Default content type for POST/PUT/PATCH Requests
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Default content type is URL-encoded. A YAML dictionary in content section will be converted to url-encoded string and sent in request.

.. code-block:: yaml

    request:
        method: post
        route: "http://httpbin.org/post"
        content:
            a: b
            d: 1

Specifying Content Type
^^^^^^^^^^^^^^^^^^^^^^^

You can explicity specify any of the following content-types:
    * text
    * html
    * xml
    * json
    * urlencoded

Following example uses YAML dictionary.

.. code-block:: yaml

    request:
        method: post
        route: "http://httpbin.org/post"
        content_type: json
        content:
            {
                "a" : "b",
                "d": 1
            }

Following example uses YAML multiline text.

.. code-block:: yaml

    request:
        method: post
        route: "http://httpbin.org/post"
        content_type: json
        content: >
            {
                "a" : "b",
                "d": 1
            }

List type content can be sent as well as YAML list or YAML multiline string.

    .. code-block:: yaml

        request:
            method: post
            route: "http://httpbin.org/post"
            content_type: json
            content: ["a", "b"]

    .. code-block:: yaml

        request:
            method: post
            route: "http://httpbin.org/post"
            content_type: json
            content: >
                ["a", "b"]

Adding **HTTP Headers**
-----------------------

You can easily add one or more headers using **headers** sub-section in **request** section as follows

    .. code-block:: yaml

        request:
            route: "http://httpbin.org/user-agent"
            headers:
                'User-agent': 'Mozilla/5.0'

**Validating Headers** in Response
----------------------------------

You can also check headers in response by using **headers** section.

    .. code-block:: yaml

        request:
            route: "http://httpbin.org/response-headers?foo=bar"

        headers:
            foo: bar

You can also check unexpected headers

    .. code-block:: yaml

        label: Check CORS Header

        request:
            route: "/res"
            headers:
                Origin: "https://bqbiffmtswfl.com"

        unexpected:
            headers:
                Access-Control-Allow-Origin: "https://bqbiffmtswfl.com"

**Validating Cookies** in Response
----------------------------------

You can check cookie value in response by using **cookies** section.

    .. code-block:: yaml

        request:
            route: "http://httpbin.org/cookies/set?foo=bar"

        cookies:
            foo: bar

You can also use advanced construct to check attributes of a cookie.

For this, the value of cookie will be a YAML dictionary.

The following example validates the secure and HttpPnly flag along with value for a cookie with name scookie

    .. code-block:: yaml

        label: Check Cookie

        request:
            route: "/something"

        cookies:
            scookie:
                value: somevalue
                secure: True
                HttpOnly: True

**Content Validation** - Check Presence Using **has** Construct 
---------------------------------------------------------------

The **has** section in message YAML is used to check presence of patterns in the HTTP Response content.

Depending on the pattern type, the corresponding content is treated as text/HTML/json etc.

Following is an example of **regex** pattern

    .. code-block:: yaml

        request:
            route: "http://httpbin.org"

        has:
            regex: '<title>\s*httpbin.org\s*</title>'

You can also use **has** construct under **unexpected** section.

    .. code-block:: yaml

        request:
            route: "https://abc.com/res"

        unexpected:
            has:
                regex: 'ip\s*"\s*:\s*"\s*19'

**Content Validation** - Check Equality Using **match** Construct 
-----------------------------------------------------------------

The **match** section in message YAML is used to check presence of patterns in the HTTP Response content and matching the value that they represent.

Depending on the pattern type, the corresponding content is treated as text/HTML/json etc.

Using **jpath** in match
^^^^^^^^^^^^^^^^^^^^^^^^

Following is an example of **jpath** pattern

    .. code-block:: yaml

        request:
            route: "http://httpbin.org/user-agent"
            headers:
                'User-agent': 'Mozilla/5.0'

        match:
            jpath:
                'user-agent': 'Mozilla/5.0' # httpbin reflects it in root dict

You can also use **match** construct under **unexpected** section.

    .. code-block:: yaml

        request:
            route: "http://httpbin.org/user-agent"
            headers:
                'User-agent': 'Mozilla/5.0'

        unexpected:
            match:
                jpath:
                    'user-agent': 'Chrome' # httpbin reflects it in root dict

Using **content** in match
^^^^^^^^^^^^^^^^^^^^^^^^^^

You can match the complete content by specifying content_type section and then using **content** construct in match.

    .. code-block:: yaml

        label: Check fetching of item

        request:
            method: get
            route: "/item/$id$"

        content_type: json

        match:
            content: {
                'name': "$name$",
                'price': "$price$"
             }

        codes: 200


.. _message_data_extraction:

**Extracting and Storing** Data From Response - **store** Construct
-------------------------------------------------------------------

At times you will want to extract data from response for custom validation or using it as input for next message.

You can do this using **store** construct. Under this construct you specify the storage name and type of extraction.

The following example extracts and stores data in **form** and **password** containers using **xpath**.

    .. code-block:: yaml

        label: Check AutoComplete Off

        request:
            route: "$route$"

        codes: 200

        store:
            form:
                xpath: "//*[@id='login-form' and autocomplete='off']"
            password:
                xpath: "//*[@id='user-password' and autocomplete='off']"

You can also use the stored value in code:

    .. code-block:: python

        response = svc.mymessage.send(route="abc")
        # Following logic checks whether atleast one of them was matched (not None)
        if not response.store.form and not response.store.password:
            request.asserter.fail("Autocomplete is not disabled. Either form or password field should have automcomplete='off'")


The extractor types which are currently available are
    * **xpath** for XPath based extraction
    * **regex** for regular expression based extraction. You should use groups in regex (by marking appropriate parts with parenthesis)
    * **jpath** for JPath based extraction
    * **header** for extracting a header by name
    * **cookie** for extracting a cookie value by name

**Custom Validations** on Extracted and Stored Data in a Message
----------------------------------------------------------------

At times you will want to put custom validations on pieces of data in an HTTP Response beyond presence (as done in **has** construct) or equality of value (as done in **matches** construct.)

You can use **validate** construct for this purpose. To make use of this construct, you should first extract and store values in one or more variables using the **store** construct.

The following example uses **store** construct with **regex** & puts its value in **jvalue** variable. Then it validates whether is is greater than 9 by using **min** command in **validate** construct.

    .. code-block:: yaml

        label: Check Error Message

        request:
            route: "/res"

        store:
            jvalue:
                regex: "(SomeRegEx)"

        validate:
            jvalue: 
                min: 9

Validations which are available under **validate** construct are
    * **exists**: Check for presence
    * **empty**: Check whether value is empty
    * **min**: Check value >= specified value
    * **max**: Check value <= specified value
    * **contains** Check the specified one of more values are contained in the object.

**Optional Extractions**
------------------------

In some use cases, you want to make the extraction optional. It means that you are fine when if it is not found. In some cases, like security testing for presence of certain error messages, the absence is what you are looking for.

By default, Arjuna raises an exception if extraction fails. You can make it optional by speciffying **strict** as False.

The following example uses **store** construct with **regex** & puts its value in **error_trace** variable. Then it validates whether it was found using the **exists** command in **validate** construct.

    .. code-block:: yaml

        label: Check Error Message

        request:
            route: "/res"

        store:
            error_trace:
                regex: "(SomeErrorRegEx)"

        validate:
            error_trace: 
                exists: False

