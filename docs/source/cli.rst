.. _cli:

Arjuna Command Line Interface
=============================

Arjuna provides a very comprehensive yet intuitive Command Line Interface (CLI).

-h or --help
------------
You can check the available options using `-h` or `--help` switch:

.. code-block:: bash

   python -m arjuna -h

.. _cli_dl_ll:

Control Logging Level using -dl and -ll Options
-----------------------------------------------

Each to Arjuna logger is associated with console as well as file logging. You can control what gets displayed on console as well as what gets logged in the log file independently of each other. This is done by specifying the minimum message level.

- **-dl or --display-level** to control which log messages are displayed on console. Default is `INFO`.
- **-ll or --log-level** to control which log messages are logged in log file. Default is `DEBUG`.

Rest of the options are available in respective commands as discussed next.

Arjuna Commands
---------------

Arjuna's CLI is Command-Driven. Following are the current available commands:
- **create-project**: Create a new project
- **run-project**: Run all tests in an Arjuna Test Project.
- **run-selected**: Run tests selected based on selectors specified.

You can see the help for a given command by running `python -m arjuna <command> -h`, for example

.. code-block:: bash

   python -m arjuna create-project -h

The create-project command - Creating a New Project Skeleton
------------------------------------------------------------

[Arjuna Test Project](#arjuna-test-project) follows a [strict test project structure](#arjuna-test-project). You can easily create the project skeleton using `create-project` command in Arjuna CLI.

It is a simple to run command. For example:

.. code-block:: bash

   python -m arjuna create-project -p /path/to/proj_name

This command creates a test project with name `proj_name` at the path provided. `proj_name` must be a valid Arjuna name.

The run-project command
-----------------------

This command is used to run all tests in the project. The tests are picked up from the `<Project Root Dir>/test/module` directory.

.. code-block:: bash

   python -m arjuna run-project -p /path/to/proj_name <run_options>

Following run options can be provided in command line:

- **-h or --help**: To check all the run options
- **rid or --runid**: The id/name of this test run. It is `mrun` by default. Run ID is used to create the report directory name.
- **static-rid**: Instructs Arjuna NOT to use the run id without appending timestap to it. It is very helpful to us this during script development as for every run a new report directory is not created.
- **-rf or --report-formats**: Report formats for test report generation. Allowed values are `XML` and `HTML`.
- **--dry-run**: Do not run tests, just enumerate them.
- **--run-envs**: Provide the test environment names (e.g. `tenv`). Arjuna automatically picks up the configuration file corresponding to this name from `<Project Root Dir>/config/env` directory (e.g. `tenv.conf`). 
- **--run-confs**: Provide the run configuration names (e.g. `trun1`). Arjuna automatically picks up the configuration file corresponding to this name from `<Project Root Dir>/config/run` directory (e.g. `trun1.conf`). 
- **-ao or --arjuna-option**: Provide any arjuna option as a key value pair. Highest precedence amongst all ways of configurations. Superimposed on all configurations that Arjuna creates. You can provide any number of these switches.
- **-uo or --user-option**: Provide any user option as a key value pair. Highest precedence amongst all ways of configurations. Superimposed on all configurations that Arjuna creates.  You can provide any number of these switches.

The run-selected command
------------------------

This command is used to run a sub-set of tests in the project. The tests are picked up from the `<Project Root Dir>/test/module` directory as per the selectors provided.

.. code-block:: bash

   python -m arjuna run-selected -p /path/to/proj_name <run_options> <selectors>

All the command line options specified for [the `run-project` command](#the-run-project-command) are supported. In addition, following selection related options are available:

- **-im or --include-modules**: One or more names/patterns for including test modules.
- **-em or --exclude-modules**: One or more names/patterns for excluding test modules.
- **-it or --include-tests**: One or more names/patterns for including test functions.
- **-et or --exclude-tests**: One or more names/patterns for excluding test functions.

Using arjuna_launcher.py Script instead of python -m arjuna
-----------------------------------------------------------

As Arjuna needs a reference to the test project root directory, Arjuna provides you with a handy runner script: `<project_root>/script/arjuna_launcher.py` script. It automatically picks up the project root directory initializes Arjuna with it along with the other command line options provided.

You can execute `run-project` or `run-selected` commands as:

.. code-block:: bash

   python arjuna_launcher.py run-project <run_options>
   python arjuna_launcher.py run-selected <run_options> <selectors>

without providing the `-p` switch for project directory.
