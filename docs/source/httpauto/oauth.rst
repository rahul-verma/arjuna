.. _oauth:


Support for **Open Authentication (OAuth)**
-------------------------------------------

Arjuna supports the following OAuth grant types with its custom HTTP session objects:


OAuth **Client Grant Session**
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

    .. code-block:: python

        Http.oauth_client_grant_session

It wraps the `BackendApplicationClient` object from `requests_oauthlib` package.

Once created, the session supports all methods in :py:class:`HttpSession <arjuna.tpi.httpauto.session.HttpSession>` object discussed above.

Explore :py:class:`OAuthClientGrantSession <arjuna.tpi.httpauto.oauth.OAuthClientGrantSession>` for constructor.

OAuth **Implicit Grant Session**
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

    .. code-block:: python

        Http.oauth_implicit_grant_session

It wraps the `MobileApplicationClient` object from `requests_oauthlib` package.

Once created, the session supports all methods in :py:class:`HttpSession <arjuna.tpi.httpauto.session.HttpSession>` object discussed above.

Explore :py:class:`OAuthImplicitGrantSession <arjuna.tpi.httpauto.oauth.OAuthImplicitGrantSession>` for constructor.

Creating a New Session from an OAuth Session
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Many a times, you will want to reuse the OAuthToken to connect to multiple services for testing.

Rather than creating a token each time, you can create it once by creating :py:class:`OAuthClientGrantSession <arjuna.tpi.httpauto.oauth.OAuthClientGrantSession>` or :py:class:`OAuthImplicitGrantSession <arjuna.tpi.httpauto.oauth.OAuthImplicitGrantSession>`.

Now you can use this OAuth session to create a new `HttpSession` object for any base URL using `create_new_session` call.

    .. code-block:: python

        oauth_session.create_new_session(url="https://someapp.com/api")
