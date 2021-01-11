.. _cli:

Arjuna's **Command Line Interface** as pytest plugin
====================================================

``-h`` or ``--help``
--------------------
You can check the available options using ``-h`` or ``--help`` switch:

.. code-block:: bash

   pytest -h

The command line options specific to Arjuna are listed under "Arjuna Test Automation Framework" heading.

.. _cli_dl_ll:

**Specifying Test Project**
---------------------------

- ``--project``: Valid absolute path of an existing Arjuna test project. 
    * If not provided, then value of "--rootdir" option from pytest is used.
    * If **--rootdir** is also not provided, then the current working directory is used.

.. _cli_testselect:

**Controlling Test Selection**
------------------------------

Running **All Tests** in the Project
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

This is the default. If you do not provide any of the selectors in the next sections, all tests in the project are run.

.. _cli_rules:

Running Tests Based on **Selection Rules**
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

You can precisely control which test are to be run by using selection rules.

You can use the following shortcut rules from the CLI (Refer :ref:`shortcut_testselect` for more details)

- ``--ipack``: One or more names/patterns for including test packages. Each pattern is provided as a separate option-pattern pair.
- ``--epack``: One or more names/patterns for excluding test packages. Each pattern is provided as a separate option-pattern pair.
- ``--imod``: One or more names/patterns for including test modules. Each pattern is provided as a separate option-pattern pair.
- ``--emod``: One or more names/patterns for excluding test modules. Each pattern is provided as a separate option-pattern pair.
- ``--itest``: One or more names/patterns for including test functions. Each pattern is provided as a separate option-pattern pair.
- ``--etest``: One or more names/patterns for excluding test functions. Each pattern is provided as a separate option-pattern pair.

You can also provide custom rules for test selection (Refer :ref:`selection_rules` and :ref:`cli_group_customrules` for more details)

- ``--irule``: One or more rules for including test functions. Each rule is provided as a separate option-pattern pair. Test Function is included if any of the inclusion rules matches.
- ``--erule``: One or more rules for excluding test functions. Each rule is provided as a separate option-pattern pair. Test Function is excluded if any of the exclusion rules matches. Evaluated before any inclusion rules.


.. _test_group:

Running Tests Based on **Test Group Definition**
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

For most common needs, providing rules directly in the CLI should suffice. However, Arjuna also gives you a provision to define re-usable rules in the form of one of more Test Group definitions.

A test group represents a re-usable, yet indvidually runnable test selection unit in Arjuna. It defines:
* What all tests should be run by defining selection rules
* What is the reference configuation for these tests

Groups are defined in **<Project root directory>/config/groups.yaml** file. For example:

.. code-block:: yaml

    gp1:
        conf: data1_env1
        imod:
            - check_delegate_1

    gp2:
        conf: data2_env2
        imod:
            - check_delegate_2

* Each group is mentioned as a label e.g. **gp1**
* **conf** is used to specify the reference configuration. This value is overriden by command line option "--rconf" if provided.
* It can include one or more of selection rules e.g. **imod** just like command line and provide one or more rules as a YAML list. (Refer :ref:`selection_rules` and :ref:`cli_group_customrules` for more details)

You can now a specific test group by providing the ``--group`` option in CLI:

.. code-block:: bash

    pytest -p arjuna --project path/to-proj_name --group gp1

Controlling **Test Reporting**
------------------------------

- ``--rid`` : The id/name of this test run. It is **mrun** by default. Run ID is used to create the report directory name.
- ``--otype``: Report formats for test report generation. Allowed values are **XML** and **HTML**. Each value is provided as a separate option value pair.
- ``--update``: Instructs Arjuna to use the run id without appending timestap to it. It is very helpful to us this during script development as for every run a new report directory is not created.

Refer :ref:`reporting` to learn more about test reporting in Arjuna.

Performing a **Dry Run**
------------------------

- ``--dry-run``: Does a dry run. Tests are not executed. Behavior depends on the type passed as argument. 
        * **SHOW_TESTS** - enumerate tests. 
        * **SHOW_PLAN** - enumerates tests fixtures. 
        * **CREATE_RES** - Create all resources and emuerates tests.

Specifying **Reference Configuration**
--------------------------------------

- ``--rconf``: Run/Reference Configuration name.

Refer :ref:`configuration` to learn more about test configuration and concept of Reference Configuration in Arjuna.

Providing **Arjuna Options** and/or **User Defined Options**
------------------------------------------------------------

You can provide Arjuna options allowed in CLI (refer :ref:`cli_overridable`) and any custom user defined user options via CLI using the following switches:

- ``--ao``: Provide any arjuna option as a key value pair. Highest precedence amongst all ways of configurations. Superimposed on all configurations that Arjuna creates. You can provide any number of these switches.
- ``--uo``: Provide any user option as a key value pair. Highest precedence amongst all ways of configurations. Superimposed on all configurations that Arjuna creates.  You can provide any number of these switches.

These option values will override every single configuration created by Arjuna by any means.

Controlling **Logging Level**
-----------------------------

- ``--display-level`` to control which log messages are displayed on console. Default is **INFO**.
- ``--logger-level`` to control which log messages are logged in log file. Default is **DEBUG**.

Refer :ref:`logging` to know more about logging in Arjuna.

**Linking Other Arjuna Test Projects** to Your Project
------------------------------------------------------

- ``--link``: Link other Arjuna test projects to current project.

Refer :ref:`link_project` for more details.