.. _intro:

Introduction
============

Automating at HTTP Layer
------------------------

Test automation at the HTTP layer in case of web applications and services is increasingly becoming popular and rightly so. 

At HTTP layer, you get faster and more stable test automation.

Arjuna supports writing tests at this layer by wrapping various related Python modules (primarily `requests` and `requests_oauthlib`), all in one framework.

**Note** This is currently a beta quality feature. The TPI for the classes and functions is fairly finalized, but prone to minor changes and extensions.

Arjuna's **Http Facade Class**
------------------------------

Arjuna provides you with :py:class:`Http <arjuna.tpi.httpauto.http.Http>` as the facade class to start with HTTP automation.

Its features include creating an HTTP Service, handling content types and so on.