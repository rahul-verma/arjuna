.. _cli:

Arjuna Command Line Interface
=============================

Arjuna provides a very comprehensive yet intuitive Command Line Interface (CLI).

Short and Long Form Switches
----------------------------

Different CLI switches might have a short form or long form or both.

Short form is prefixed with a single hyphen e.g. **-h**. Typically these forms have one or two letters.

Long form is prefixed with a two consecutive hyphens e.g. **--help**. (In this HTML doc it will visually look like a long single hyphen.). These forms are comprised of one or more words.

-h or --help
------------
You can check the available options using **-h** or **--help** switch:

.. code-block:: bash

   python -m arjuna -h

.. _cli_dl_ll:



Arjuna Commands
---------------

Arjuna's CLI is Command-Driven. Following are the current available commands:
    - **create-project**: Create a new project
    - **run-project**: Run all tests in an Arjuna Test Project.
    - **run-selected**: Run tests selected based on selectors specified.
    - **run-session**: Run a session defined in **<Project Root Directory/config/sessions.yaml>**.
    - **run-stage**: Run a session defined in **<Project Root Directory/config/stages.yaml>**.
    - **run-group**: Run a session defined in **<Project Root Directory/config/groups.yaml>**.

.. note::

    For using **run-session**, **run-stage** or **run-group**, the config directory must contain **sessions.yaml**, **stages.yaml** and **groups.yaml** files (even if empty).

You can see the help for a given command by running **python -m arjuna <command> -h**, for example

.. code-block:: bash

   python -m arjuna create-project -h

The **create-project** command
------------------------------

:ref:`Arjuna Test Project <test_project>` follows a strict test project structure. You can easily create the project skeleton using **create-project** command in Arjuna CLI.

It is a simple to run command. For example:

.. code-block:: bash

   python -m arjuna create-project -p /path/to/proj_name

This command creates a test project with name **proj_name** at the path provided. **proj_name** must be a valid Arjuna name.

.. _run_project:

The **run-project** command
---------------------------

This command is used to run all tests in an :ref:`Arjuna Test Project <test_project>`. The tests are picked up from the **<Project Root Dir>/test/module** directory.

.. code-block:: bash

   python -m arjuna run-project -p /path/to/proj_name <run_options>

Following run options can be provided in command line:

- **-p** or **--project-root-dir**: Valid absolute path of an existing Arjuna test project. 
    * Needed with python -m arjuna call only. 
    * (See last section on this page) With python arjuna_launcher.py you can skip this argument as the script determines its container Arjuna test project automatically.
- **-h** or **--help**: To check all the run options
- **-r** or **--run-id**: The id/name of this test run. It is **mrun** by default. Run ID is used to create the report directory name.
- **-o** or **--output-formats**: Report formats for test report generation. Allowed values are **XML** and **HTML**.
- **--update**: Instructs Arjuna to use the run id without appending timestap to it. It is very helpful to us this during script development as for every run a new report directory is not created.
- **--dry-run**: Does a dry run. Tests are not executed. Behavior depends on the type passed as argument. 
        * **SHOW_TESTS** - enumerate tests. 
        * **SHOW_PLAN** - enumerates tests fixtures. 
        * **CREATE_RES** - Create all resources and emuerates tests.
- **-c** or **--conf**: Configuration object name for this run.
- **-ao** or **--arjuna-option**: Provide any arjuna option as a key value pair. Highest precedence amongst all ways of configurations. Superimposed on all configurations that Arjuna creates. You can provide any number of these switches.
- **-uo** or **--user-option**: Provide any user option as a key value pair. Highest precedence amongst all ways of configurations. Superimposed on all configurations that Arjuna creates.  You can provide any number of these switches.
- **-dl** or **--display-level** to control which log messages are displayed on console. Default is **INFO**.
- **-ll** or **--log-level** to control which log messages are logged in log file. Default is **DEBUG**.

The **run-selected** command
----------------------------

This command is used to run a sub-set of tests in the project. The tests are picked up from the **<Project Root Dir>/test/module** directory as per the selectors provided.

.. code-block:: bash

   python -m arjuna run-selected -p /path/to/proj_name <run_options> <selectors>

All the command line options specified for :ref:`the run-project command <run_project>` are supported. In addition, following selection related options are available:

- **-im** or **--include-modules**: One or more names/patterns for including test modules.
- **-em** or **--exclude-modules**: One or more names/patterns for excluding test modules.
- **-it** or **--include-tests**: One or more names/patterns for including test functions.
- **-et** or **--exclude-tests**: One or more names/patterns for excluding test functions.


The **run-session** command
---------------------------

This command is used to run tests as per a session definition in **<Project Root Directory>/config/sessions.yaml** file.

.. code-block:: bash

   python -m arjuna run-session -p /path/to/proj_name -s <session_name>

All the command line options specified for :ref:`the run-project command <run_project>` are supported. In addition, following selection related options are available:

- **-s** or **--session-name**: Name of session definition file (without .yaml extension)


The **run-stage** command
-------------------------

This command is used to run tests as per a test stage definition in **<Project Root Directory>/config/stages.yaml** file.

.. code-block:: bash

   python -m arjuna run-stage -p /path/to/proj_name -s <stage_name>

All the command line options specified for :ref:`the run-project command <run_project>` are supported. In addition, following selection related options are available:

- **-s** or **--stage-name**: Name of a defined stage


The **run-group** command
-------------------------

This command is used to run tests as per a test group definition in **<Project Root Directory>/config/groups.yaml** file.

.. code-block:: bash

   python -m arjuna run-group -p /path/to/proj_name -g <group_name>

All the command line options specified for :ref:`the run-project command <run_project>` are supported. In addition, following selection related options are available:

- **-g** or **--group-name**: Name of a defined group.


Using **arjuna_launcher.py** Script instead of python -m arjuna
---------------------------------------------------------------

As Arjuna needs a reference to the test project root directory, Arjuna provides you with a handy runner script: **<project_root>/script/arjuna_launcher.py** script. It automatically picks up the project root directory initializes Arjuna with it along with the other command line options provided.

You can execute **run-project** or **run-selected** commands as:

.. code-block:: bash

   python arjuna_launcher.py run-project <run_options>
   python arjuna_launcher.py run-selected <run_options> <selectors>

without providing the **-p** switch for project directory.
