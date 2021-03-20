.. _faq:


Introduction
------------

This section lists and answers frequently asked questions about usage of Arjuna. 

Although some information might be repeated from elsewhere, it extends the overall documentation coverage by providing new, additional insights and pointers.

.. _link_project:

Can I Make an Arjuna Test Project depend on another Arjuna Test Project?
------------------------------------------------------------------------

Yes.

Method 1 (Basic): ArjunaOption.DEPS_DIR
=======================================

For simple dependency, where you just want to use the library from another Arjuna Test Project, you can set ArjunaOption.DEPS_DIR in your reference configuration (e.g. project.yaml) or CLI option to point to the directory that contains the project.

For example let's say "parent" project depends on "child" and "child" is contained in the **/abc/def/root/child** location. Then:
    * You can set **deps.dir = /abc/def/root** in **project.yaml**
    * You can as well pass ``--ao deps.dir /abc/def/root`` in the command line.

The path can also be a relative path. Arjuna will consider it relative to the root of parent Arjuna project.

For example, let's consider the following directory structre:
    * Child project: /abc/def/root/child
    * Parent project: /abc/def/xyz/parent

In the above case **deps.dir** can be passed as **../../root**.


Method 2 (Advanced): ``--link`` CLI Option
==========================================

In an Arjuna test project, you typically define many externalized files like configurations, data files, reference files and so on. A simple Python import resolution like Method 1 can not automatically make these available to dependent project. You will need to write quite a bit of complex code to achieve this.

Arjuna provides a feature to make an Arjuna test project linked to one or more other Arjuna test projects and automatically makes their artifacts available to the top project.

To achieve this, you can pass ``--link`` CLI option.

For example to link to "linked1" project present at **/abc/def/root/linked**:

    .. code-block:: text

        --link /abc/def/root/linked

The path can also be a relative path. Arjuna will consider it **relative to the current directory**.

For example, let's consider the following directory structre:
    * Linked project: /abc/def/root/linked
    * Parent project: /abc/def/xyz/parent

In the above case Linked project path can be passed as **root/linked**, if current working directory is **/abc/def**

With this linking, following will happen automatically:
    * Configurations
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

        --link /abc/def/root/linked1 --link /abc/def/root/linked2 --link /abc/def/root/linked3

In the above case, merging/overriding order is as follows:
    * linked2 overrides linked1
    * linked3 overrides linked2 and linked1
    * parent project overrides linked3, linked2 and linked1

Pay attention to the order of multiple ``--link`` switches as it determines the overriding order.

Can I Maintain **Local Configuration (.local) Files** That Override the Default Configuration Files?
----------------------------------------------------------------------------------------------------

Yes!

Need for Local Config Files
===========================

When you work as team then at times you need to create configuration files that are **local** to your development machine.

There are various reasons to need this feature:
    * You are experimenting with a configuration value.
    * You have local deployed environments.
    * You want to use a temporary user account to test a transient/under-development feature.

and so on.

Supported Local Config Files
============================

Arjuna supports maintaining local versions of all its configuration files. Following table provides the names of the **local** files and corresponding default files:

.. list-table:: Local Config File Names
   :widths: 50 50
   :header-rows: 1

   * - Local Config File Name
     - Corresponding Default Config File Name
   * - project.local.yaml
     - project.yaml
   * - data.local.yaml
     - data.yaml
   * - envs.local.yaml
     - envs.yaml
   * - groups.local.yaml
     - groups.yaml
   * - withx.local.yaml
     - withx.yaml

What Happens When a Local Config File is Present?
=================================================

When a local file is present then Arjuna loads this file and IGNORES the default corresponding config file.

Creating local config files is optional and you can create one or more of them as paer your need.

Configuring Version Control To Avoid Check-In of Local Config Files
===================================================================

A suggested practice is to set your version control software to ignore local config files during check-in so that different people in your team can maintain their own versions of these local config files.

For example, if you are using Git, then you can add the following to **.gitignore**:

.. code-block:: text

    **/*.local.*

Can I use an HTTP Proxy with Arjuna where applicable?
-----------------------------------------------------

Yes. Arjuna allows you to set an HTTP/S Proxy for Web UI Automation and HTTP layer automation.

Setting Proxy across Test Project
=================================

You can set a global proxy in **project.yaml** file. You can also provide the options with ``--ao`` switch in CLI.

Following 3 options are the relevant Arjuna options:
    * **HTTP_PROXY_ENABLED**: Enables/Disables proxy. Can be set to True/False. False by default.
    * **HTTP_PROXY_HOST**: Host/IP of proxy. Default is **localhost**.
    * **HTTP_PROXY_PORT**: Network port of proxy. Default is **8080**.

Setting Proxy for a Particular HTTP Session
===========================================

Rather than a global proxy setting, which applies to all Web GUI Automation as well as HTTP Automation, you can also set the proxy for a particular HttpSession as follows:

.. code-block:: python

    # Direct Session
    session = Http.session(proxy=Http.proxy('proxyhost', 9000))

    # From ouathsession
    session = ouathsession.create_new_session("https://someurl.com", proxy=Http.proxy('proxyhost', 9000))


