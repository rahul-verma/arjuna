.. _configuration:

Test Configuration
==================

Understanding Configuration System of Arjuna
--------------------------------------------

Arjuna has possibly the most advanced configuration system amongst any test frameworks or tools that you will come across.

You can start simple. Even without defining a single configuration file of your own. And as your needs unfold, you can benefit by the variety of options provided by Arjuna.

**Configuration** object and Configuration Options
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
- Options in Arjuna can be defined with various configuration files, command line and/or programmatically.
- Arjuna supports tweaking its built in options which are represented by **ArjunaOption** enum. 
- Arjuna also supports user defined options. So, you can create your own project related options and use the same eco-system which Arjuna uses for its built-in options.
- A :py:class:`Configuration<arjuna.tpi.config.Configuration>` object represents fixed values for configured settings (Arjuna options as well user defined options).
- A :py:class:`Configuration<arjuna.tpi.config.Configuration>` is immutable which means that once created it can not be modified. This saves you from a lot of debugging overhead as configuration objects are large global objects. Arjuna makes them read-only.

Default **Reference Configuration**
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
- As a part of initialation, Arjuna creates the reference :py:class:`Configuration<arjuna.tpi.config.Configuration>` object which combines the following to create the reference :
    - Default settings for Arjuna options
    - Project level settings included in **<Project root directory>/config/project.yaml** file.
    - Options in data configuration with name **data** in **<Project root directory>/config/data.yaml** file, if present.
    - Options in environment configuration with name **env** in **<Project root directory>/config/envs.yaml** file, if present.
    - CLI options represtedn by Arjuna's named CLI switches (e.g. for logging options)
- You can get the reference configuration by calling **Arjuna.get_config()** and any other configuration with **Arjuna.get_config(<name>)** call.
- Within test or test fixture code, you can also get the reference configuration object (if not re-assigned by test author to a non-reference configuration) using **request.config** or use **request.get_config** to retrieve any configuration.

Each :py:class:`Configuration<arjuna.tpi.config.Configuration>` object ever created in a run in any manner takes reference configuration as its basis at its root. So, in case of you have a chain of configurations as C1 -> C2 -> C3 where C1 was used to create C2 which was then used to create C3, either C1 is the reference configuration itself or it has reference configuration used by its parent/grandparent.


Using a non-default Configuration as Reference Configuration
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

You can instruct Arjuna to use any of the following Configuration objects to be used as a Reference Configuration:
    * Default Reference Configuration.
    * Any Data Configuration
    * Any Environment Configuration
    * Any combination of Data and Enviroment configurations
    * Any configuration defined in **register_ref_confs** hook in **<Project Root Directory/hook/arjuna_config.py** module.

There are various places to pass on this instruction:
    * Test Run:
        - **-c / --ref-conf** command line switch with any **run-x** commands in Arjuna CLI. 
        - This becomes reference configuration for this test run, current test session, all stages and groups in the session, unless overriden in their YAML definition.
    * Test Session definition:
        - **conf** attribute in YAML. This becomes reference configuration for this session, all stages and groups in this session, unless overriden in their YAML definition.
        - This also overrides -c switch if passed.
    * Test Stage definition:
        - **conf** attribute in YAML. This becomes reference configuration for this stage and all groups in this stage, unless overriden in their YAML definition.
        - This also overrides -c switch if passed.
    * Test Group definition:
        - **conf** attribute in YAML. This becomes reference configuration for this group and all test modules and test functions, unless programmatically overriden.
        - This also overrides -c switch if passed.    

All calls to the reference configuration are replaced with the configuration object that you attached. This means that this configuration becomes the reference configuration.

As discussed in above section, the core reference configuration is the basis of all Configuration obejcts. So, you have access to all options in their original form except the ones that were overriden in the Configuration object that you attached to the group.


**project.yaml** - Setting Project Level Configuration Options
--------------------------------------------------------------

Many a times, it is useful to change the defaults of Arjuna at project level to avoid writing code every time. It is also a much better way when you need to tweak quite a few settings and you know that those settings are applicable to most of your tests.

In Arjuna you can do this by providing options under **arjuna_options** section in **<Project root directory>/config/project.yaml** file.

For example:

.. code-block:: YAML

    arjuna_options:
        browser.name: firefox

The above entry tweaks **ArjunaOption.BROWSER_NAME**. You can also use **BROWSER_NAME** instead of **brower.name**. 

For being more intuitive and less mistake prone, Arjuna supports keys in this section as **case-insensitive** and treats **. (dot)** and **_ (underscore)** as interchangeable. 

**Configuration Builder** - Creating Custom Configurations
----------------------------------------------------------

In Arjuna, you can create your own configurations as well. You can do this by using reference Configuration or any other configuration created by you as the source object.

Given a :py:class:`Configuration<arjuna.tpi.config.Configuration>` object (say **config**), you can get a **ConfigBuilder** object with **config.builder** property. You can add options to the builder and then call its **register** method to create a new configuration. This newly created configuration is returned by the **register** call.

Sometimes it is useful to provide your own name to the custom configuration that you are creating. Arjuna helps you in creating the configuration in one place and retrieving it in another place. You need not pass the configuration object around for simple needs of this nature. To achieve this pass the name while registering: **register(<name>)**. It can also now be retrived anywhere in your project with the **Arjuna.get_config(<name>)** call. Within a test, it can also be retrieve by using **request.get_config(<name>)** call.

**ConfigBuilder** also provides direct methods for some commonly used Arjuna Options. For example **.firefox()** is equivalent to **.option("browser.name", BrowserName.FIREFOX)**

Defining and Handling **User Options**
--------------------------------------

Just like Arjuna options, you can define your own options in **project.yaml** file as well as programmatically. Rest of the fundamentals remain same as Arjuna options. That's the key point! Arjuna provides you the same facilities for your own defined options that it provides to built-in **ArjunaOptions**.

User Options in Project Conf
^^^^^^^^^^^^^^^^^^^^^^^^^^^^

In Arjuna you can define your own option under **user_options** section in **<Project root directory>/config/project.yaml** file.

.. code-block:: YAML

    user_options:
        target.url: "https://google.com"


Adding User Options Programmatically
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

You can also add user options programmatically using the **ConfigBuilder** object just like we use it for tweaking Ajuna's builtin-options.

Retrieving the values is same as retrieving an **ArjunaOption**.

Configuration Builder - **Adding options from a .yaml File**
------------------------------------------------------------

**ConfigBuilder** can also load Arjuna options as well user options from **.yaml** files. It comes handy when you have a controlled set of configurations which want to create at run-time. It could be also helpful if for some reasons your logic involves clubbing of options from multiple files.

You can load options from any file using **from_file** method of **ConfigBuilder** and providing the file path.

The Magic **C** Function
------------------------

Purpose 
^^^^^^^

Arjuna provides a special function **C** for retrieving values from the reference configuration as it is a very common operation to do on test code. You can pass an **ArjunaOption** enum constant or an option name. The name string has all the flexibility seen in previous example.

**Configuration Query Format**
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

As Arjuna supports a multi-configuration system, it also provides a special query syntax for retrieving configuration values.

You can use the configuration query syntax **<confname>.<option>** to retrieve configuration values for a given configuration. 

Let's say we have custom configuration with name **nconf**. 
- **browser.name** refers to the property in reference configuration.
- You can prefix a configuration name with a configuration name. For example **reference.browser.name** and **nconf.browser.name** will retrieve **browser.name** from **reference** and **nconf** configurations respectively.

**Data Configurations and Environment Configurations**
------------------------------------------------------


Defining Data Configurations
^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Many a times, you end up using Data Driven testing when what you need is a simple data separation. 

Added to this, you might have different sets of data for different runs. 

One simple option in Arjuna is to define such data as user defined options in data configuration file. 

You can define any number of data configurations in **<Project Root Dir>/config/data.yaml>** file.


.. code-block:: YAML

    data_conf_1:
        arjuna_options:
            <options>
        user_options:
            <options>
    data_conf_2:
        arjuna_options:
            <options>
        user_options:
            <options>



Defining Environment Configuration
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

You might have multiple test environments or deployments against which you run the tests. 

For example, your web application could have a dev, staging, system and production deployment with respective URLs and other associated options. 

You can define any number of environment configurations in **<Project Root Dir>/config/envs.yaml>** file.


.. code-block:: YAML

    env1:
        arjuna_options:
            <options>
        user_options:
            <options>
    env2:
        arjuna_options:
            <options>
        user_options:
            <options>



Combining Data and Environment Configurations
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Another need is that you might want to use data and environment information in combination.

Arjuna has built-in support for this and does it by default for you.

Arjuna automatically loads these combinations of data confs and environment confs when it loads. For each combination:
    - Reference config is taken as base (which means Arjuna's internal defaults + Options that you have passed in project.yaml + Default data conf (if defined) + Default env conf (if defined))
        * For default data and env conf, see the next section.
    - A given data conf is superimposed
    - A given env conf is superimposed
    - CLI options are superimposed

The config name is set to **<dataconfname>_<envconfname>** e.g. **data1_env1**.

You can retrieve an environment config by its name using **Arjuna.get_config** (anywhere in your project) or **request.get_config** call (in a test fixture or test function). Now you can inquire the values just like you deal with any configuration in Arjuna. 

You can also retrieve their options using the magic **C** function, for example **C("data1_env1.browser.name")**

Default Data Configuration and Environment Configuration
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

A data configuration with name **data** is considered a default.

An environment configuration with name **env** is considered a default.

What it means is that if these configurations are defined, then Arjuna uses options contained in them to update the reference configuration.

This feature has the following side-effects:
    * A configuration with name **data_env** is same as the reference configuration.
    * A configuration with name **data1_env** is same as **data1**
    * A configuration with name **data_env1** is same as **env1**

Arjuna Options Reference for Overriding
---------------------------------------

Arjuna has a well defined control over which options can be overriden in which type of configuration.

Refer :py:class:`ArjunaOption Enum <arjuna.tpi.constant.ArjunaOption>` for purpose of each option.

Options Overridable in a Coded Configuration
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

When you create a configuration using :py:class:`ConfigBuilder<arjuna.tpi.config.ConfigBuilder>` in your code, the following options can be overriden:

	* REPORT_NETWORK_FILTER
	* APP_URL
	* BROWSER_NAME
	* BROWSER_HEADLESS
	* BROWSER_VERSION
	* BROWSER_MAXIMIZE
	* BROWSER_DIM_HEIGHT
	* BROWSER_DIM_WIDTH
	* BROWSER_BIN_PATH
	* BROWSER_NETWORK_RECORDER_AUTOMATIC
	* SCROLL_PIXELS
	* GUIAUTO_MAX_WAIT
	* GUIAUTO_SLOMO_ON
	* GUIAUTO_SLOMO_INTERVAL
	* MOBILE_OS_NAME
	* MOBILE_OS_VERSION
	* MOBILE_DEVICE_NAME
	* MOBILE_DEVICE_UDID
	* MOBILE_APP_FILE_PATH
	* SELENIUM_DRIVER_DOWNLOAD
	* SELENIUM_SERVICE_URL
	* APPIUM_SERVICE_URL
	* APPIUM_AUTO_LAUNCH
	* IMG_COMP_MIN_SCORE

Options Overridable in a Reference Configuration
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

A reference configuration is defined in any of the following manner and combinations:

    * project.yaml
    * Entry in data.yaml
    * Entry in envs.yaml
    * Configuration created via Arjuna's **register_ref_confs** hook in arjuna_config.py

A reference configuration can override what can be overriden in a coded configuration. In addition, you can also override the following:

	* LOG_ALLOWED_CONTEXTS
	* REPORT_SCREENSHOTS_ALWAYS
	* REPORT_NETWORK_ALWAYS
	* L10N_LOCALE
	* L10N_STRICT
	* BROWSER_NETWORK_RECORDER_ENABLED

Options Overridable via Command Line
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Via command line's **-ao** / **--arjuna-option** switches, you can override Arjuna options across every configuration created by Arjuna.

You can override options that you can override in a Reference configuration (and hence a coded configuration too). In addition, you can override the following:

	* RUN_SESSION_NAME
	* LOG_FILE_LEVEL
	* LOG_CONSOLE_LEVEL
	* REPORT_FORMATS

Read-Only Options
^^^^^^^^^^^^^^^^^

In addition to the overridable options, Arjuna also has various options that are inquirable, but not oveeridable, because of the following reasons:

    * These are auto-determined by Arjuna based on the machine on which the tests are running.
    * To impose a strict directory structure for an Arjuna test project for consistency across projects.
    * The values are determined based on other Arjuna options provided by the test author.

Following is the list:

	* ARJUNA_ROOT_DIR
	* ARJUNA_EXTERNAL_IMPORTS_DIR
	* LOG_NAME
	* RUN_HOST_OS
	* L10N_DIR
	* PROJECT_NAME
	* PROJECT_ROOT_DIR
	* CONF_PROJECT_FILE
	* TESTS_DIR
	* HOOKS_DIR
	* REPORTS_DIR
	* REPORT_DIR
	* REPORT_XML_DIR
	* REPORT_HTML_DIR
	* LOG_DIR
	* SCREENSHOTS_DIR
	* TOOLS_DIR
	* TOOLS_BMPROXY_DIR
	* TEMP_DIR
	* CONF_DIR
	* CONF_DATA_FILE
	* CONF_ENVS_FILE
	* CONF_SESSIONS_FILE
	* CONF_STAGES_FILE
	* CONF_GROUPS_FILE
	* CONF_WITHX_FILE
	* DATA_DIR
	* DATA_SRC_DIR
	* DATA_REF_DIR
	* DATA_REF_CONTEXTUAL_DIR
	* DATA_REF_INDEXED_DIR
	* DATA_FILE_DIR
	* GUIAUTO_NAME
	* GUIAUTO_DIR
	* GUIAUTO_NAMESPACE_DIR
	* GUIAUTO_DEF_MULTICONTEXT
	* GUIAUTO_CONTEXT
	* SELENIUM_DRIVER_PROP
	* SELENIUM_DRIVERS_DIR
	* SELENIUM_DRIVER_PATH
	* RUN_ID
