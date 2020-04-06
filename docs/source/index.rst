.. Arjuna documentation master file, created by
   sphinx-quickstart on Fri Apr  3 20:14:29 2020.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

*****************
Welcome to Arjuna
*****************

.. image:: _static/Arjuna.png
    :align: center

Arjuna is a Python based test automation framework developed by Rahul Verma (www.rahulverma.net). Rahul has implemented smaller variants of features in Arjuna across frameworks and organizations, or given advise around it. However Arjuna being a generic library has the most complete implementation of his ideas, away from project specific contexts and constraints.

Arjuna uses `pytest <https://docs.pytest.org/en/latest/>`_ as its recommended test engine. Arjuna also provides its markup for some common use cases on top of pytest. If you like, you can make use of Arjuna with any other test engine or custom frameworks as well.

You'd need Python 3.5+ to make use of Arjuna.

Note: On Linux, the built-in Python3 build has issues with the Python's built-in enum module which is heavily used in Arjuna. One alternative is to install ActiveState Python on linux. Advanced users can go for installing a custom Python build.

You can find the example code in [arjex project](https://github.com/rahul-verma/arjuna/tree/master/arjuna-samples/arjex).

**************
Tester's Guide
**************

Fundamentals
============

.. toctree::
   :maxdepth: 6

   installation
   test_project
   cli
   test_function

Handling Configuration Options
==============================

.. toctree::
   :maxdepth: 6

   configuration

Data Driven Testing with Arjuna
===============================

.. toctree::
   :maxdepth: 6

   ddt

Contextual Data References and Localization
===========================================

.. toctree::
   :maxdepth: 6

   data_ref
   l10n

Web GUI Automation
==================

.. toctree::
   :maxdepth: 6

   guiauto/index

********************************************
Tester Programming Interface (TPI) Reference
********************************************

All classes, functions, enums and exceptions that are supposed to be directly used by a test author are a part of Arjuna's Tester Programming Interface (TPI).

This interface is fully encapsulated in :py:mod:`arjuna.tpi` package.

You can either do a fully qualified import for a public name, for example:

.. code-block:: python

    from arjuna.tpi.log import log_info

or an easy, simple import that imports all public TPI names from Arjuna:

.. code-block:: python

    from arjuna import *

Following links direct you to documentation for all public names:

Test Configuration
==================
* :py:mod:`arjuna.tpi.config.Configuration`
* :py:mod:`arjuna.tpi.config.ConfigBuilder`

Helpers
=======

* Logging: Log Module - :py:mod:`arjuna.tpi.log`


Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`


