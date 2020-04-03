.. Arjuna documentation master file, created by
   sphinx-quickstart on Fri Apr  3 20:14:29 2020.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

Welcome to Arjuna
=================

Welcome to Arjuna's documentation. 

Arjuna is a Python based test automation framework developed by Rahul Verma (www.rahulverma.net). Rahul has implemented smaller variants of features in Arjuna across frameworks and organizations, or given advise around it. However Arjuna being a generic library has the most complete implementation of his ideas, away from project specific contexts and constraints.

Arjuna uses `pytest <https://docs.pytest.org/en/latest/>`_ as its recommended test engine. Arjuna also provides its markup for some common use cases on top of pytest. If you like, you can make use of Arjuna with any other test engine or custom frameworks as well.

You'd need Python 3.5+ to make use of Arjuna.

Note: On Linux, the built-in Python3 build has issues with the Python's built-in enum module which is heavily used in Arjuna. One alternative is to install ActiveState Python on linux. Advanced users can go for installing a custom Python build.

You can find the example code in [arjex project](https://github.com/rahul-verma/arjuna/tree/master/arjuna-samples/arjex).

Tester's Guide
--------------

.. toctree::
   :maxdepth: 6

   installation
   test_project
   cli
   test_function
   configuration
   ddt
   data_ref
   l10n
   guiauto/index



Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
