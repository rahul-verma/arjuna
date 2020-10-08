.. _faq:


Introduction
------------

This section lists and answers frequently asked questions about usage of Arjuna. 

Although some information might be repeated from elsewhere, it extends the overall documentation coverage by providing new, additional insights and pointers.


Can I Make an Arjuna Test Project depend on another Arjuna Test Project?
------------------------------------------------------------------------

Yes.

Method 1 (Basic): ArjunaOption.DEPS_DIR
=======================================

For simple dependency, where you just want to use the library from another Arjuna Test Project, you can set ArjunaOption.DEPS_DIR in your reference configuration (e.g. project.yaml) or CLI option to point to the directory that contains the project.

For example let's say "parent" project depends on "child" and "child" is contained in the **/abc/def/root/child** location. Then:
    * You can set **deps.dir = /abc/def/root** in **project.yaml**
    * You can as well pass **-ao deps.dir /abc/def/root** in the command line.

The path can also be a relative path. Arjuna will consider it relative to the root of parent Arjuna project.

For example, let's consider the following directory structre:
    * Child project: /abc/def/root/child
    * Parent project: /abc/def/xyz/parent

In the above case **deps.dir** can be passed as **../../root**.


Method 2 (Advanced): **-l**/**--link-project** CLI Option
=========================================================

In an Arjuna test project, you typically define many externalized files like configurations, data files, reference files and so on. A simple Python import resolution like Method 1 can not automatically make these available to dependent project. You will need to write quite a bit of complex code to achieve this.

Arjuna provides a feature to make an Arjuna test project linked to one or more other Arjuna test projects and automatically makes their artifacts available to the top project.

To achieve this, you can pass **-l**/**--link-project** CLI option.

For example to link to "linked1" project present at **/abc/def/root/linked**:

    .. code-block:: text

        -l /abc/def/root/linked
        --link-project /abc/def/root/linked

The path can also be a relative path. Arjuna will consider it relative to the root of parent Arjuna project.

For example, let's consider the following directory structre:
    * Child project: /abc/def/root/linked
    * Parent project: /abc/def/xyz/parent

In the above case **deps.dir** can be passed as **../../root/linked**.

With this linking, following will happen automatically:
    * Confiugurations
        * project.yaml gets merged.
        * All data confiturations in data.yaml get merged. 
        * All environment configurations in envs.yaml get merged.
        * All combinations of data and environment configurations get merged.
    * Data References
        * All data references from linked project become available.
        * If there is name conflict, linked project's references are overriden by parent project.
    * Test Resources/Fixtures
        * All test resources from linked project become available.
        * If there is name conflict, linked project's resources are overriden by parent project.
    * DBAuto Files
        * All DBAuto files from linked project become available.
        * If there is name conflict, linked project's files are overriden by parent project.

You can link multiple projects as well:

    .. code-block:: text

        -l /abc/def/root/linked1 -l /abc/def/root/linked2 -l /abc/def/root/linked3
        --link-project /abc/def/root/linked1 --link-project /abc/def/root/linked2 --link-project /abc/def/root/linked3

In the above case, merging/overriding order is as follows:
    * linked2 overrides linked1
    * linked3 overrides linked2 and linked1
    * parent project overrides linked3, linked2 and linked1

Pay attention to the order of multiple **-l**/**--link-project** switches as it determines the overriding order.


How Do I Use Custom Test Selection Rules?
-----------------------------------------

Arjuna defines an advanced grammar for selection of tests with its :ref:`selection_rules` (the linked page describes the rules grammar in detail.)

You can supply one or more selection rules in command line or write them in a group definition.

Command-Line
============

When you use :ref:`run_selected`, you can provide the following switches to provide rules:
    * **-ir**/**--include-rule**
    * **-er**/**--exclude-rule**

Any number of the above switches can be provided. Following are some examples:


:ref:`boolean_pattern_rule` Example

    .. code-block:: text

        -ir unstable -ir "not reviewed"


:ref:`iterable_pattern_rule` Example

    .. code-block:: text

        -ir "with tags a,b" -ir "without tags x,y"


:ref:`test_attr_rule` Example

    .. code-block:: text

        -ir "author is Rahul" -ir "priority < 3"


Group Definition in **groups.yaml**
===================================

You can also add rules to the group definition in **groups.yaml**. 

Any number of such rules can be added.

Following are some examples where **sample_group** is the group name.

:ref:`boolean_pattern_rule` Example

    .. code-block:: yaml

        sample_group:
            ir:
                - "unstable"
                - "not reviewed"


:ref:`iterable_pattern_rule` Example

    .. code-block:: yaml

        sample_group:
            ir:
                - "with tags slow"
                - "without tags x,y"


:ref:`test_attr_rule` Example

    .. code-block:: yaml

        sample_group:
            ir:
                - "author is Rahul"
                - "priority < 3"