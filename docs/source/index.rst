.. Arjuna documentation master file, created by
   sphinx-quickstart on Fri Apr  3 20:14:29 2020.
   You can adapt this file completely to your liking, but it should at least
   contain the root **toctree** directive.

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


Writing an Automated Test
=========================

.. toctree::
   :maxdepth: 6

   test_function


Handling Test Resources
=======================

.. toctree::
   :maxdepth: 6

   resources

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


Test Selection Rules
====================

.. toctree::
   :maxdepth: 6

   selection_rules


Test Sessions, Stages, Groups
=============================

.. toctree::
   :maxdepth: 6

   sessions_stages_groups


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

Test, Test Resources and Assertions
===================================
* :py:func:`@test <arjuna.tpi.engine.test.test>`
    * :py:func:`skip <arjuna.tpi.engine.test.skip>`
    * :py:func:`xfail <arjuna.tpi.engine.test.xfail>`
    * :py:func:`problem_in <arjuna.tpi.engine.relation.problem_in>`
* :py:class:`Asserter <arjuna.tpi.engine.asserter.Asserter>`
* :py:mod:`Test Resources <arjuna.tpi.engine.resource>`
    * :py:func:`@for_test <arjuna.tpi.engine.resource.for_test>`
    * :py:func:`@for_module <arjuna.tpi.engine.resource.for_module>`
    * :py:func:`@for_group <arjuna.tpi.engine.resource.for_group>`

Test Configuration
==================
* :py:class:`ArjunaOption Enum <arjuna.tpi.constant.ArjunaOption>`
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


Web GUI Automation
==================

* :py:class:`Gui <arjuna.tpi.guiauto.model.gui.Gui>`: It represents all type of Guis and is the base class for the following classes:
    * :py:class:`GuiApp <arjuna.tpi.guiauto.model.app.GuiApp>`
    * :py:class:`GuiAppContent <arjuna.tpi.guiauto.model.content.GuiAppContent>`: It represents the content of a **GuiApp** and is the base class of the following classes:
        * :py:class:`GuiPage <arjuna.tpi.guiauto.model.page.GuiPage>`
        * :py:class:`GuiSection <arjuna.tpi.guiauto.model.section.GuiSection>`
        * :py:class:`GuiDialog <arjuna.tpi.guiauto.model.dialog.GuiDialog>`
* Defining and formatting Gui Widget Locators:
    * :py:class:`GuiWidgetLocator <arjuna.tpi.guiauto.meta.locator.GuiWidgetLocator>`
    * Classes related to formatting of **GuiWidgetLocator**:
        * :py:class:`GNSLabelFormatter <arjuna.tpi.guiauto.meta.formatter.GNSLabelFormatter>`
        * :py:class:`GuiWidgetLocatorFormatter <arjuna.tpi.guiauto.meta.formatter.GuiWidgetLocatorFormatter>`
* Different Gui Widgets
    * :py:class:`GuiElement <arjuna.tpi.guiauto.widget.element.GuiElement>`
    * :py:class:`GuiMultiElement <arjuna.tpi.guiauto.widget.multielement.GuiMultiElement>`
        * Filtering a GuiMultiElement - :py:class:`GuiMultiElementFilter <arjuna.tpi.guiauto.widget.multielement.GuiMultiElementFilter>`
    * :py:class:`GuiDropDown <arjuna.tpi.guiauto.widget.dropdown.GuiDropDown>`
    * :py:class:`GuiRadioGroup <arjuna.tpi.guiauto.widget.radio_group.GuiRadioGroup>`
* Inquiring Gui Source
    * :py:class:`GuiPageSource <arjuna.tpi.guiauto.source.page.GuiPageSource>`
    * :py:class:`GuiElementSource <arjuna.tpi.guiauto.source.element.GuiElementSource>`
    * :py:class:`GuiMultiElementSource <arjuna.tpi.guiauto.source.multielement.GuiMultiElementSource>`
    * :py:class:`GuiSourceContent <arjuna.tpi.guiauto.source.content.GuiSourceContent>` - Encapsulates source content for all Guis and GuiWidgets.

Objects In Arjuna Hooks
=======================

* :py:class:`Configurator <arjuna.tpi.hook.config.Configurator>`

Helpers
=======
* :py:meth:`HardCoded.sleep <arjuna.tpi.helper.audit.HardCoded.sleep>`
* :py:class:`Json <arjuna.tpi.helper.json.Json>`
* :py:mod:`XML <arjuna.tpi.helper.xml>`
    * :py:class:`XmlNode <arjuna.tpi.helper.xml.XmlNode>`
    * :py:class:`NodeLocator <arjuna.tpi.helper.xml.NodeLocator>`
* :py:class:`Image <arjuna.tpi.helper.image.Image>`
* :py:meth:`Arjuna Types <arjuna.tpi.helper.arjtype>`
    * :py:class:`CIStringDict <arjuna.tpi.helper.arjtype.CIStringDict>`
    * :py:class:`ProcessedKeyDict <arjuna.tpi.helper.arjtype.ProcessedKeyDict>`
    * :py:class:`OnceOnlyKeyCIStringDict <arjuna.tpi.helper.arjtype.OnceOnlyKeyCIStringDict>`
    * :py:class:`Point <arjuna.tpi.helper.arjtype.Point>`
    * :py:class:`Offset <arjuna.tpi.helper.arjtype.Offset>`
    * :py:class:`Screen <arjuna.tpi.helper.arjtype.Screen>`
    * :py:class:`NVPair <arjuna.tpi.helper.arjtype.NVPair>`
    * :py:class:`NVPairs <arjuna.tpi.helper.arjtype.NVPair>`
    * :py:class:`Attr <arjuna.tpi.helper.arjtype.Attr>`


Logging
=======

* :py:mod:`Log <arjuna.tpi.log>`
    * :py:func:`log_trace <arjuna.tpi.log.log_trace>`
    * :py:func:`log_debug <arjuna.tpi.log.log_debug>`
    * :py:func:`log_info <arjuna.tpi.log.log_info>`
    * :py:func:`log_warning <arjuna.tpi.log.log_warning>`
    * :py:func:`log_error <arjuna.tpi.log.log_error>`
    * :py:func:`log_fatal <arjuna.tpi.log.log_fatal>`
* :py:func:`@track <arjuna.tpi.tracker.track>`

Arjuna Exceptions
=================

* Tests
    * :py:class:`TestDecoratorError <arjuna.tpi.error.TestDecoratorError>`
    * :py:class:`TestSelectorNotFoundError <arjuna.tpi.error.TestSelectorNotFoundError>`
* Configuration
    * :py:class:`UndefinedConfigError <arjuna.tpi.error.UndefinedConfigError>`
    * :py:class:`ConfigCreationError <arjuna.tpi.error.ConfigCreationError>`
* Test Session, Stage and Group
    * :py:class:`TestSessionsFileNotFoundError <arjuna.tpi.error.TestSessionsFileNotFoundError>`
    * :py:class:`UndefinedTestSessionError <arjuna.tpi.error.UndefinedTestSessionError>`
    * :py:class:`InvalidTestSessionDefError <arjuna.tpi.error.InvalidTestSessionDefError>`
    * :py:class:`TestStagesFileNotFoundError <arjuna.tpi.error.TestStagesFileNotFoundError>`
    * :py:class:`UndefinedTestStageError <arjuna.tpi.error.UndefinedTestStageError>`
    * :py:class:`InvalidTestStageDefError <arjuna.tpi.error.InvalidTestStageDefError>`
    * :py:class:`TestGroupsFileNotFoundError <arjuna.tpi.error.TestGroupsFileNotFoundError>`
    * :py:class:`UndefinedTestGroupError <arjuna.tpi.error.UndefinedTestGroupError>`
* Gui Automation
    * :py:class:`GuiWidgetForLabelPresentError <arjuna.tpi.error.GuiWidgetForLabelPresentError>`
    * :py:class:`GuiWidgetPresentError <arjuna.tpi.error.GuiWidgetPresentError>`
    * :py:class:`GuiWidgetForLabelNotPresentError <arjuna.tpi.error.GuiWidgetForLabelNotPresentError>`
    * :py:class:`GuiWidgetNotPresentError <arjuna.tpi.error.GuiWidgetNotPresentError>`
    * :py:class:`GuiNamespaceLoadingError <arjuna.tpi.error.GuiNamespaceLoadingError>`
    * :py:class:`GuiNotLoadedError <arjuna.tpi.error.GuiNotLoadedError>`
    * :py:class:`GuiLabelNotPresentError <arjuna.tpi.error.GuiLabelNotPresentError>`


******************
Indices and tables
******************

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`


