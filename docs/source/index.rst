.. Arjuna documentation master file, created by
   sphinx-quickstart on Fri Apr  3 20:14:29 2020.
   You can adapt this file completely to your liking, but it should at least
   contain the root **toctree** directive.

****************************************************************
Welcome to Arjuna - The Framework for Professional Coded Testing
****************************************************************

.. image:: _static/Arjuna.png
    :align: center

Arjuna is a Python based test automation framework developed by `Rahul Verma <http://www.rahulverma.net>`_. 

It is an open source, Apache Licensed software: `Arjuna on GitHub <https://github.com/rahul-verma/arjuna>`_.

Rahul has implemented smaller variants of features in Arjuna across frameworks and organizations, or given advice around it. However Arjuna being a generic library has the most complete implementation of his ideas, away from project specific contexts and constraints.

Arjuna provides its own markup over `pytest <https://docs.pytest.org/en/latest/>`_ as its underlying test engine. If you like, you can make use of Arjuna with any other test engine or custom frameworks as well.

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

Data Spaces - Shareable Data Objects for Tests
==============================================

.. toctree::
   :maxdepth: 6

   test_spaces

Data Generation and Data Entities
=================================

.. toctree::
   :maxdepth: 6

   datagen_entity

Data References
===============

.. toctree::
   :maxdepth: 6

   data_ref

Localization
============

.. toctree::
   :maxdepth: 6

   l10n

Logging
=======

.. toctree::
   :maxdepth: 6

   logging


Test Reporting
==============

.. toctree::
   :maxdepth: 6

   reporting


Web GUI Automation
==================

.. toctree::
   :maxdepth: 6

   guiauto/index


HTTP Automation
===============

.. toctree::
   :maxdepth: 4

   httpauto

Parsing Text, JSON, YAML, XML, HTML Files and Strings
=====================================================

.. toctree::
   :maxdepth: 4

   textparsing

Notes About Python Libraries and Tools Used in Arjuna
=====================================================

.. toctree::
   :maxdepth: 4

   externals

Frequently Asked Questions (FAQs)
=================================

.. toctree::
   :maxdepth: 4

   faq


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
* **Assertions**
    * :py:class:`Asserter <arjuna.tpi.engine.asserter.Asserter>`
    * :py:class:`AsserterMixIn <arjuna.tpi.engine.asserter.AsserterMixIn>`
    * :py:class:`IterableAsserterMixin <arjuna.tpi.engine.asserter.IterableAsserterMixin>`
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
* :py:mod:`Data Source Markup <arjuna.tpi.data_markup>`
    * :py:class:`record <arjuna.tpi.engine.data_markup.record>`
    * :py:class:`records <arjuna.tpi.engine.data_markup.records>`
    * :py:class:`data_function <arjuna.tpi.engine.data_markup.data_function>`
    * :py:class:`data_class <arjuna.tpi.engine.data_markup.data_class>`
    * :py:class:`data_file <arjuna.tpi.engine.data_markup.data_file>`
    * :py:class:`many_data_sources <arjuna.tpi.engine.data_markup.many_data_sources>`
* :py:class:`DataRecord <arjuna.tpi.data.record.DataRecord>`

Data Generation and Data Entities
=================================
* :py:class:`Random <arjuna.tpi.data.generator.Random>`
* :py:class:`generator <arjuna.tpi.data.generator.generator>`
* :py:class:`composite <arjuna.tpi.data.generator.composite>`
* :py:class:`composer <arjuna.tpi.data.generator.composer>`
* :py:class:`data_entity <arjuna.tpi.data.entity.data_entity>`

Data References
===============
* :py:class:`IndexedDataReference <arjuna.tpi.data.reference.IndexedDataReference>`
* :py:class:`ContextualDataReference <arjuna.tpi.data.reference.ContextualDataReference>`

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

HTTP Automation
===============
* :py:class:`Http <arjuna.tpi.httpauto.http.Http>`
* :py:class:`HttpSession <arjuna.tpi.httpauto.session.HttpSession>`
* :py:class:`HttpRequest <arjuna.tpi.httpauto.request.HttpRequest>`
* :py:class:`HttpResponse <arjuna.tpi.httpauto.response.HttpResponse>`
* OAuth Support
    * :py:class:`OAuthSession <arjuna.tpi.httpauto.oauth.OAuthSession>`
    * :py:class:`OAuthClientGrantSession <arjuna.tpi.httpauto.oauth.OAuthClientGrantSession>`
    * :py:class:`OAuthImplicitGrantSession <arjuna.tpi.httpauto.oauth.OAuthImplicitGrantSession>`

Reporting Protocols
===================

* :py:class:`ScreenShooter <arjuna.tpi.protocol.screen_shooter.ScreenShooter>`
* :py:class:`NetworkRecorder <arjuna.tpi.protocol.network_recorder.NetworkRecorder>`

Objects In Arjuna Hooks
=======================

* :py:class:`Configurator <arjuna.tpi.hook.config.Configurator>`

Parsers
=======

* :py:mod:`Text <arjuna.tpi.parser.text>`
    * :py:class:`Text <arjuna.tpi.parser.text.Text>`
    * :py:class:`TextFile <arjuna.tpi.parser.text.TextFile>`
    * :py:class:`TextFileAsLines <arjuna.tpi.parser.text.TextFileAsLines>`
    * :py:class:`DelimTextFileWithLineAsSeq <arjuna.tpi.parser.text.DelimTextFileWithLineAsSeq>`
    * :py:class:`DelimTextFileWithLineAsMap <arjuna.tpi.parser.text.DelimTextFileWithLineAsMap>`
* :py:mod:`JSON <arjuna.tpi.parser.json>`
    * :py:class:`Json <arjuna.tpi.parser.json.Json>`
    * :py:class:`JsonElement <arjuna.tpi.parser.json.JsonElement>`
    * :py:class:`JsonDict <arjuna.tpi.parser.json.JsonDict>`
    * :py:class:`JsonList <arjuna.tpi.parser.json.JsonList>`
    * :py:class:`JsonSchema <arjuna.tpi.parser.json.JsonSchema>`
    * :py:class:`JsonSchemaBuilder <arjuna.tpi.parser.json.JsonSchemaBuilder>`
* :py:mod:`YAML <arjuna.tpi.yaml.yaml>`
    * :py:class:`Yaml <arjuna.tpi.parser.yaml.Yaml>`
    * :py:class:`YamlElement <arjuna.tpi.parser.yaml.YamlElement>`
    * :py:class:`YamlDict <arjuna.tpi.parser.yaml.YamlDict>`
    * :py:class:`YamlList <arjuna.tpi.parser.yaml.YamlList>`
* :py:mod:`XML <arjuna.tpi.parser.xml>`
    * :py:class:`Xml <arjuna.tpi.parser.xml.Xml>`
    * :py:class:`XmlNode <arjuna.tpi.parser.xml.XmlNode>`
    * :py:class:`NodeLocator <arjuna.tpi.parser.xml.NodeLocator>`
* :py:mod:`HTML <arjuna.tpi.parser.html>`
    * :py:class:`Html <arjuna.tpi.parser.html.Html>`
    * :py:class:`HtmlNode <arjuna.tpi.parser.html.HtmlNode>`

Helpers
=======
* :py:meth:`HardCoded.sleep <arjuna.tpi.helper.audit.HardCoded.sleep>`
* :py:class:`Image <arjuna.tpi.helper.image.Image>`
* :py:meth:`Date Time Helper Classes <arjuna.tpi.helper.datetime>`
    * :py:class:`Time <arjuna.tpi.helper.datetime.Time>`
    * :py:class:`DateTime <arjuna.tpi.helper.datetime.DateTime>`
    * :py:class:`DateTimeDelta <arjuna.tpi.helper.datetime.DateTimeDelta>`
    * :py:class:`DateTimeDeltaBuilder <arjuna.tpi.helper.datetime.DateTimeDeltaBuilder>`
    * :py:class:`DateTimeStepper <arjuna.tpi.helper.datetime.DateTimeStepper>`
* :py:meth:`Arjuna Types <arjuna.tpi.helper.arjtype>`
    * :py:class:`CIStringDict <arjuna.tpi.helper.arjtype.CIStringDict>`
    * :py:class:`ProcessedKeyDict <arjuna.tpi.helper.arjtype.ProcessedKeyDict>`
    * :py:class:`OnceOnlyKeyCIStringDict <arjuna.tpi.helper.arjtype.OnceOnlyKeyCIStringDict>`
    * :py:class:`Point <arjuna.tpi.helper.arjtype.Point>`
    * :py:class:`Offset <arjuna.tpi.helper.arjtype.Offset>`
    * :py:class:`Screen <arjuna.tpi.helper.arjtype.Screen>`
    * :py:class:`nvpair <arjuna.tpi.helper.arjtype.nvpair>`
    * :py:class:`nvpairs <arjuna.tpi.helper.arjtype.nvpair>`
    * :py:class:`withx <arjuna.tpi.helper.arjtype.withx>`
    * :py:class:`attr <arjuna.tpi.helper.arjtype.attr>`


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
    * :py:class:`DisallowedArjunaOptionError <arjuna.tpi.error.DisallowedArjunaOptionError>`
    * :py:class:`ArjunaOptionValidationError <arjuna.tpi.error.ArjunaOptionValidationError>`
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
* HTTP Automation
    * :py:class:`HttpRequestCreationError <arjuna.tpi.error.HttpRequestCreationError>`
    * :py:class:`HttpConnectError <arjuna.tpi.error.HttpConnectError>`
    * :py:class:`HttpSendError <arjuna.tpi.error.HttpSendError>`
    * :py:class:`HttpUnexpectedStatusCodeError <arjuna.tpi.error.HttpUnexpectedStatusCodeError>`

******************
Indices and tables
******************

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`


************
Contributors
************

This package is authored and maintained by:

    `Rahul Verma <https://github.com/rahul-verma>`__  (`@rahul_verma <https://twitter.com/rahul_verma>`__)

with the help of patches submitted by `these contributors <https://github.com/rahul-verma/arjuna/graphs/contributors>`__.

*********************
Copyright and License
*********************

Copyright 2015 - Rahul Verma

Licensed under the Apache License, Version 2.0 (the “License”); you may not use this file except in compliance with the License. You may obtain a copy of the License at

::

    http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software distributed under the License is distributed on an “AS IS” BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the License for the specific language governing permissions and limitations under the License.






