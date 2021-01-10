.. _cli:

-h or --help
------------
You can check the available options using **-h** or **--help** switch:

.. code-block:: bash

   pytest -h

The command line options specific to Arjuna are listed under "Arjuna Test Automation Framework" heading.

.. _cli_dl_ll:

Specifying Test Project
-----------------------

- **--project**: Valid absolute path of an existing Arjuna test project. 
    * If not provided, then value of "--rootdir" option from pytest is used.
    * If **--rootdir** is also not provided, then the current working directory is used.

Controlling Test Reporting
--------------------------

- **--rid**: The id/name of this test run. It is **mrun** by default. Run ID is used to create the report directory name.
- **--otype**: Report formats for test report generation. Allowed values are **XML** and **HTML**. Each value is provided as a separate option value pair.
- **--update**: Instructs Arjuna to use the run id without appending timestap to it. It is very helpful to us this during script development as for every run a new report directory is not created.

Performing a Dry Run
--------------------

- **--dry-run**: Does a dry run. Tests are not executed. Behavior depends on the type passed as argument. 
        * **SHOW_TESTS** - enumerate tests. 
        * **SHOW_PLAN** - enumerates tests fixtures. 
        * **CREATE_RES** - Create all resources and emuerates tests.

Specifying Reference Configuration
----------------------------------

- **--rconf**: Run/Reference Configuration name.

Providing Arjuna Options and/or User Defined Options
----------------------------------------------------
- **--ao**: Provide any arjuna option as a key value pair. Highest precedence amongst all ways of configurations. Superimposed on all configurations that Arjuna creates. You can provide any number of these switches.
- **--uo**: Provide any user option as a key value pair. Highest precedence amongst all ways of configurations. Superimposed on all configurations that Arjuna creates.  You can provide any number of these switches.

Controlling Logging Level
-------------------------

- **--display-level** to control which log messages are displayed on console. Default is **INFO**.
- **--logger-level** to control which log messages are logged in log file. Default is **DEBUG**.

Controlling Test Selection
--------------------------

- **--group** to run tests as per a test group definition in **<Project Root Directory>/config/groups.yaml** file.
- **--ipack**: One or more names/patterns for including test packages. Each pattern is provided as a separate option-pattern pair.
- **--epack**: One or more names/patterns for excluding test packages. Each pattern is provided as a separate option-pattern pair.
- **--imod**: One or more names/patterns for including test modules. Each pattern is provided as a separate option-pattern pair.
- **--emod**: One or more names/patterns for excluding test modules. Each pattern is provided as a separate option-pattern pair.
- **--itest**: One or more names/patterns for including test functions. Each pattern is provided as a separate option-pattern pair.
- **--etest**: One or more names/patterns for excluding test functions. Each pattern is provided as a separate option-pattern pair.
- **--irule**: One or more rules for including test functions. Each rule is provided as a separate option-pattern pair. Test Function is included if any of the inclusion rules matches.
- **--erule**: One or more rules for excluding test functions. Each rule is provided as a separate option-pattern pair. Test Function is excluded if any of the exclusion rules matches. Evaluated before any inclusion rules.


Linking Other Arjuna Test Projects to Your Project
--------------------------------------------------

- **--link**: Link other Arjuna test projects to current project.