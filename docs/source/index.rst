.. Arjuna documentation master file, created by
   sphinx-quickstart on Fri Apr  3 20:14:29 2020.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

*****************
Welcome to Arjuna
*****************

.. image:: _static/Arjuna.png
    :align: center

Arjuna is a Python based test automation framework developed by `Rahul Verma <http://www.rahulverma.net>`_. 

It is an open source, Apache Licensed software: `Arjuna on GitHub <https://github.com/rahul-verma/arjuna>`_.

Rahul has implemented smaller variants of features in Arjuna across frameworks and organizations, or given advice around it. However Arjuna being a generic library has the most complete implementation of his ideas, away from project specific contexts and constraints.

Arjuna uses `pytest <https://docs.pytest.org/en/latest/>`_ as its recommended test engine. Arjuna also provides its own markup for some common use cases on top of pytest. If you like, you can make use of Arjuna with any other test engine or custom frameworks as well.

You'd need Python 3.5+ to make use of Arjuna.

Note: On Linux, the built-in Python3 build has issues with the Python's built-in enum module which is heavily used in Arjuna. One alternative is to install ActiveState Python on linux. Advanced users can go for installing a custom Python build.

You can find a lot of example code for using Arjuna in `Arjex project on GitHub <https://github.com/rahul-verma/arjuna/tree/master/arjuna-samples/arjex>`_.

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
* :py:class:`ArjunaOption Enum <arjuna.tpi.enums.ArjunaOption>`
* :py:class:`Configuration<arjuna.tpi.config.Configuration>`
* :py:class:`ConfigBuilder<arjuna.tpi.config.ConfigBuilder>`

The Magic Functions
===================
* :py:func:`The Magic C Function <arjuna.tpi.magic.C>`
* :py:func:`The Magic L Function <arjuna.tpi.magic.L>`
* :py:func:`The Magic R Function <arjuna.tpi.magic.R>`

Data Driven Testing
===================
* :py:class:`Random <arjuna.tpi.engine.data.generator.Random>`
* :py:mod:`Data Source Markup <arjuna.tpi.engine.data.markup>`
    * :py:class:`record <arjuna.tpi.engine.data.markup.record>`
    * :py:class:`records <arjuna.tpi.engine.data.markup.records>`
    * :py:class:`data_function <arjuna.tpi.engine.data.markup.data_function>`
    * :py:class:`data_class <arjuna.tpi.engine.data.markup.data_class>`
    * :py:class:`data_file <arjuna.tpi.engine.data.markup.data_file>`
    * :py:class:`many_data_sources <arjuna.tpi.engine.data.markup.many_data_sources>`
* :py:class:`DataRecord <arjuna.tpi.engine.data.record.DataRecord>`

Helpers
=======


Logging
=======

* :py:mod:`Log <arjuna.tpi.log>`
    * :py:func:`log_trace <arjuna.tpi.log.log_trace>`
    * :py:func:`log_debug <arjuna.tpi.log.log_debug>`
    * :py:func:`log_info <arjuna.tpi.log.log_info>`
    * :py:func:`log_warning <arjuna.tpi.log.log_warning>`
    * :py:func:`log_error <arjuna.tpi.log.log_error>`
    * :py:func:`log_fatal <arjuna.tpi.log.log_fatal>`

Arjuna Exceptions
=================

* :py:mod:`Exceptions <arjuna.tpi.exceptions>`
    * :py:class:`GuiElementForLabelPresentError <arjuna.tpi.exceptions.GuiElementForLabelPresentError>`
    * :py:class:`GuiElementPresentError <arjuna.tpi.exceptions.GuiElementPresentError>`
    * :py:class:`GuiElementForLabelNotPresentError <arjuna.tpi.exceptions.GuiElementForLabelNotPresentError>`
    * :py:class:`GuiElementNotPresentError <arjuna.tpi.exceptions.GuiElementNotPresentError>`
    * :py:class:`GuiNamespaceLoadingError <arjuna.tpi.exceptions.GuiNamespaceLoadingError>`
    * :py:class:`GuiNotLoadedError <arjuna.tpi.exceptions.GuiNotLoadedError>`
    * :py:class:`GuiLabelNotPresentError <arjuna.tpi.exceptions.GuiLabelNotPresentError>`






Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`


