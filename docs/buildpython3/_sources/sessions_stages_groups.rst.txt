.. _sessions_stages_groups:


Test **Sessions**, **Stages**, **Groups**
=========================================

Although Arjuna provides an advanced Command Line Interface, in professional test automation a CLI switch based approach very soon gives up for complex test selection and configuration.

To define what to run needs most of the following features:
* An overall way to define what to run
* Splitting the run into sequential steps
* Running tests in parallel
* Precise selection of tests across this definition of what and how to run.


**Test Groups**
===============

A test group represents a re-usable, yet indvidually runnable test selection unit in Arjuna. It defines:
* What all tests should be run by defining selection rules
* What is the reference configuation for these tests

Each test group is run in a thread using **pytest.main** invocation.

Note: pytest is not designed to be used in this manner. Running pytest as a subprocess or running Arjuna sub-process for a test group is being considered for future.

Defining a Test Group
---------------------

Groups are defined in **<Project root directory>/config/groups.yaml** file. For example:

.. code-block:: yaml

    gp1:
        conf: data1_env1
        im:
            - check_delegate_1

    gp2:
        conf: data2_env2
        im:
            - check_delegate_2

* Each group is mentioned as a label e.g. **gp1**
* **conf** is used to specify the reference configuration. If not specified:

    * With **run-group** command, 
        * Configuration specified by **--c/--ref-conf** switch in CLI.
        * If above is not specified, then **ref**, the default reference configuration is considered.
    * With **run-stage** command or **run-session** command, configuration of test stage in which this group is included is considered.

* It can include one or more of selection rules e.g. **im** just like command line and provide one or more rules as a YAML list.


Directly Running a Test Group
-----------------------------

You can run a test group by running **arjuna** module or running **arjuna_launcher.py** script with **run-group** command:

.. code-block:: bash

    python -m arjuna run-group -p path/to-proj_name -g <group_name>
    python arjuna_launcher.py run-group -g <group_name>


**Test Stages**
===============

A test group represents a re-usable, yet indvidually runnable test selection unit in Arjuna. It defines:
* What all test groups should be included.
* How many threads should be used to run these test groups.
* What is the reference configuation for these groups, overridable in individual group definitions.

**A test stage is the only selection unit in Arjuna in which you can specify parallelism.**


Defining a Test Stage
---------------------

Test Stages are defined in **<Project root directory>/config/stages.yaml** file. For example:

.. code-block:: yaml

    simple_stage:
        include:
            - gp1
            - gp2

    complex_stage:
        conf: abc
        threads: 2
        include:
            - gp3
            - gp4

* Each stage is mentioned as a label e.g. **simple_stage**
* **conf** is used to specify the reference configuration. If not specified:

    * With **run-stage** command, 
        * Configuration specified by **--c/--ref-conf** switch in CLI.
        * If above is not specified, then **ref**, the default reference configuration is considered.
    * With **run-session** command, configuration of test session in which this stage is included is considered.

* It can include one or more test groups by their names using the **include** key and providing a YAML list of names.
* **threads** key can be used to specify number of threads to execute the test groups.

Directly Running a Test Stage
-----------------------------

You can run a test stage by running **arjuna** module or running **arjuna_launcher.py** script with **run-stage** command:

.. code-block:: bash

    python -m arjuna run-stage -p path/to-proj_name -s <stage_name>
    python arjuna_launcher.py run-stage -s <stage_name>


**Test Sessions**
=================

A test session represents a runnable test selection unit in Arjuna. It defines:
* What all test stages should be included.
* What is the reference configuation for these test stages, overridable in individual stage and group definitions.

Each run of Arjuna represents running of a test session, whether or not explcitly specified.


Defining a Test Session
-----------------------

Test Sessions are defined in **<Project root directory>/config/sessions.yaml** file. For example:

.. code-block:: yaml

    daily:
        include: 
            - base_test_stage
            - deeper_test_stage

    debugging:
        conf: abc
        include: 
            - base_test_stage
            - new_test_stage

* Each session is mentioned as a label e.g. **daily**
* **conf** is used to specify the reference configuration. If not specified:

    * Configuration specified by **--c/--ref-conf** switch in CLI is considered.
    * If above is not specified, then **ref**, the default reference configuration is considered.

* It can include one or more test stages by their names using the **include** key and providing a YAML list of names.
* Test stages in a test session are always executed **sequentially**.

Running a Test Session
----------------------

You can run a test session by running **arjuna** module or running **arjuna_launcher.py** script with **run-session** command:

.. code-block:: bash

    python -m arjuna run-session -p path/to-proj_name -s <session_name>
    python arjuna_launcher.py run-session -s <session_name>


**Default Test Session, Stage and Group**
=========================================

Arjuna gives the flexibility to run a project, a test selection, a session, a stage or a group via its Command Line Interface.

Internally, all of these are mapped to defaults when not explicitly:

* With **run-project**, a test session containing a single stage containing a single group of all the tests in the test project is assumed. Defaults are specified below:
    * Test Session is considered as Magic session. Its name will appear as **msession**.
    * Test Stage is considered as Magic stage. Its name will appear as **mstage**.
    * Test Group is considered as Magic group. Its name will appear as **mgroup**.
* With **run-selected**, a test session containing a single stage containing a single group of all the tests as per the selection rules is assumed. Defaults are specified below:
    * Test Session is considered as Magic session. Its name will appear as **msession**.
    * Test Stage is considered as Magic stage. Its name will appear as **mstage**.
    * Test Group is considered as Magic group. Its name will appear as **mgroup**.
* With **run-group**, a test session containing a single stage containing the specified group is assumed. Defaults are specified below:
    * Test Session is considered as Magic session. Its name will appear as **msession**.
    * Test Stage is considered as Magic stage. Its name will appear as **mstage**.
* With **run-group**, a test session containing a the specified stage is assumed. Defaults are specified below:
    * Test Session is considered as Magic session. Its name will appear as **msession**.
* **run-session** is the most specific run command in Arjuna. All considerations are as per the exact session definition.
