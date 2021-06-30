.. _seam_message:

**SEAMful - HTTP Message**
==========================

Introduction
------------

Arjuna's **Http facade class** as well as **HttpSession** object can read and send abstracted Http messages in YAML based externalization files.

In addition, any checks and extractions specified in the YAML file are also performed.

These files are placed under **<Arjuna Test Project root dir>/httpauto/message** directory.

To keep the documentation terse, we will assume **svc** as an **HttpSession** object.

    .. code-block:: python

        svc.message("abc")
    
The above code will look for a file **abc.yaml** in the **<Arjuna Test Project root dir>/httpauto/message** directory and then perform corresponding HTTP message as per specification.

You can also create sub-directories to organize messages.

    .. code-block:: python

        svc.message("some_dir/abc")

The above code will look for a file **abc.yaml** in the **<Arjuna Test Project root dir>/httpauto/message/some_dir** directory and then perform corresponding HTTP message as per specification.

Blank Message File
------------------

A blank message file means the following:
    * Send a GET request
    * Route is the root of session i.e. same as default URL of HttpSession object
    * Perform no checks on response

Technically it means the same as following:

    .. code-block:: python

        svc.message()

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

You can specify the YAML in a dynamic way so that you can pass data to it from code.

.. note:: 

    Arjuna will use the data to format the raw YAML text before loading it as YAML object.

For example

    .. code-block:: yaml

        request:
            method: get
            route: "$url$"
            a: b

        codes: 404
        url: "$url$?$param_str$"

in the above YAML specifies **$url$** and **$param_str** plaecholders.

You can pass values to these named placeholders as follows (assume abc.yaml as the message file name)

    .. code-block:: python

        svc.message('abc', url="/get", param_str="a=b")

Here **url** construct is used to validate the URL for which the response was yielded.

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

**Content Validation** - Using **has** Construct 
------------------------------------------------

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

        response = svc.message("/abc")
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

The following example uses **store** construct with **regex** & puts its value in **error_trace** variable. Then it validates whether it was found using the **exists** command in **validate** construct.

    .. code-block:: yaml

        label: Check Error Message

        request:
            route: "/res"

        store:
            error_trace:
                regex: "(SomeErrorStr)"

        validate:
            error_trace: 
                exists: False

Other validations which are available under **validate** construct are
    * **min**: Check value >= specified value
    * **max**: Check value <= specified value
    * **contains** Check the specified one of more values are contained in the object.



