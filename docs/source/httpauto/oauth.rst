.. _oauth:


Support for **Open Authentication (OAuth)**
-------------------------------------------

Arjuna supports the following OAuth grant types with its custom HTTP service objects:


OAuth **Client Grant Service**
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

    .. code-block:: python

        Http.oauth_client_grant_service

It wraps the `BackendApplicationClient` object from `requests_oauthlib` package.

Once created, the session supports all methods in :py:class:`HttpService <arjuna.tpi.httpauto.session.HttpService>` object discussed above.

Explore :py:class:`OAuthClientGrantService <arjuna.tpi.httpauto.oauth.OAuthClientGrantService>` for constructor.

OAuth **Implicit Grant Service**
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

    .. code-block:: python

        Http.oauth_implicit_grant_service

It wraps the `MobileApplicationClient` object from `requests_oauthlib` package.

Once created, the session supports all methods in :py:class:`HttpService <arjuna.tpi.httpauto.session.HttpService>` object discussed above.

Explore :py:class:`OAuthImplicitGrantService <arjuna.tpi.httpauto.oauth.OAuthImplicitGrantService>` for constructor.

Creating a New Service from an OAuth Service
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Many a times, you will want to reuse the OAuthToken to connect to multiple services for testing.

Rather than creating a token each time, you can create it once by creating :py:class:`OAuthClientGrantService <arjuna.tpi.httpauto.oauth.OAuthClientGrantService>` or :py:class:`OAuthImplicitGrantService <arjuna.tpi.httpauto.oauth.OAuthImplicitGrantService>`.

Now you can use this OAuth session to create a new `HttpService` object for any base URL using `create_new_service` call.

    .. code-block:: python

        oauth_service.create_new_service(url="https://someapp.com/api")
