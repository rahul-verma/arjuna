.. _configuration:

Test Configuration
==================

Understanding Configuration System of Arjuna
--------------------------------------------

Arjuna has possibly the most advanced configuration system amongst any test frameworks or tools that you will come across.

You can start simple. Even without defining a single configuration file of your own. And as your needs unfold, you can benefit by the variety of options provided by Arjuna.

`Configuration` object and Configuration Options
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
- Options in Arjuna can be defined with various configuration files, command line and/or programmatically.
- Arjuna supports tweaking its built in options which are represented by `ArjunaOption` enum. 
- Arjuna also supports user defined options. So, you can create your own project related options and use the same eco-system which Arjuna uses for its built-in options.
- A `Configuration` object represents fixed values for configured settings (Arjuna options as well user defined options).
- A `Configuration` is immutable which means that once created it can not be modified. This saves you from a lot of debugging overhead as configuration objects are large global objects. Arjuna makes them read-only.

Reference Configuration (Non-session run)
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
- As a part of initialation, Arjuna creates the reference `Configuration` object which combines the following to create the reference :
    - Default settings for Arjuna options
    - Project level settings included in `<Project root directory>/config/project.conf` file.
    - Data Configuration options in `<Project root directory>/config/data/data.conf` file.
    - Environment Configuration options in `<Project root directory>/config/env/env.conf` file.
    - CLI options represtedn by Arjuna's named CLI switches (e.g. for logging options)
- You can get the reference configuration by calling `Arjuna.get_config()` and any other configuration with `Arjuna.get_config(<name>)` call.
- Within test or test fixture code, you can also get the reference configuration object (if not re-assigned by test author to a non-reference configuration) using `request.config` or use `request.get_config` to retrieve any configuration.

Each `Configuration` object ever created in a run in any manner takes reference configuration as its basis at its root. So, in case of you have a chain of configurations as C1 -> C2 -> C3 where C1 was used to create C2 which was then used to create C3, either C1 is the reference configuration itself or it has reference configuration used by its parent/grandparent.


Reference Configuration (Session run)
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
When you run tests using a session file, each group in each stage is run separately.

You can attach a group definition with a configuration object of choice.

Once you do this, when this group is executed, all calls to the reference configuration are replaced with the configuration object that you attached. This means that this configuration becomes the reference configuration.

As discussed in above section, the core reference configuration is the basis of all Configuration obejcts. So, you have access to all options in their original form except the ones that were overriden in the Configuration object that you attached to the group.


project.conf - Setting Project Level Configuration Options
----------------------------------------------------------

Many a times, it is useful to change the defaults of Arjuna at project level to avoid writing code every time. It is also a much better way when you need to tweak quite a few settings and you know that those settings are applicable to most of your tests.

In Arjuna you can do this by providing options under `arjunaOptions` section in `<Project root directory>/config/project.conf` file. The contents of `arjunaOptions` follow [HOCON](https://github.com/lightbend/config/blob/master/HOCON.md) syntax. This means that you can write settings in properties syntax, as JSON or as human-readable JSON syntax supported by HOCON.

For example:

.. code-block:: javascript

    arjunaOptions {
        browser.name = firefox
    }

Add the above content to `project.conf` file. We want to tweak `ArjunaOption.BROWSER_NAME`. Correspondingly you can add entry for `BROWSER_NAME` in `arjunaOptions`. For being more intuitive and less mistake prone, Arjuna supports keys in this section as **case-insensitive** and treats **. (dot)** and **_ (underscore)** as interchangeable. This is similar to the behavior of option name string seen in previous section.

Configuration Builder - Creating Custom Configurations
------------------------------------------------------

In Arjuna, you can create your own configurations as well. You can do this by using reference Configuration or any other configuration created by you as the source object.

Given a `Configuration` object (say `config`), you can get a `ConfigBuilder` object with `config.builder` property. You can add options to the builder and then call its `register` method to create a new configuration. This newly created configuration is returned by the `register` call.

Sometimes it is useful to provide your own name to the custom configuration that you are creating. Arjuna helps you in creating the configuration in one place and retrieving it in another place. You need not pass the configuration object around for simple needs of this nature. To achieve this pass the name while registering: `register(<name>)`. It can also now be retrived anywhere in your project with the `Arjuna.get_config(<name>)` call. Within a test, it can also be retrieve by using `request.get_config(<name>)` call.

`ConfigBuilder` also provides direct methods for some commonly used Arjuna Options. For example `.firefox()` is equivalent to `.option("browser.name", BrowserName.FIREFOX)`

Defining and Handling User Options
----------------------------------

Just like Arjuna options, you can define your own options in `project.conf` file as well as programmatically. Rest of the fundamentals remain same as Arjuna options. That's the key point! Arjuna provides you the same facilities for your own defined options that it provides to built-in `ArjunaOptions`.

User Options in Project Conf
^^^^^^^^^^^^^^^^^^^^^^^^^^^^

In Arjuna you can define your own option under `userOptions` section in `<Project root directory>/config/project.conf` file.

.. code-block:: javascript

    userOptions {
        target.url = "https://google.com"
    }

Adding User Options Programmatically
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

You can also add user options programmatically using the `ConfigBuilder` object just like we use it for tweaking Ajuna's builtin-options.

Retrieving the values is same as retrieving an `ArjunaOption`.

Configuration Builder - Adding options from a .conf File
--------------------------------------------------------

`ConfigBuilder` can also load Arjuna options as well user options from `.conf` files. It comes handy when you have a controlled set of configurations which want to create at run-time. It could be also helpful if for some reasons your logic involves clubbing of options from multiple files.

You can load options from any file using `from_file` method of `ConfigBuilder` and providing the file path.

The Magic C Function
--------------------

Purpose 
^^^^^^^

Arjuna provides a special function `C` for retrieving values from the reference configuration as it is a very common operation to do on test code. You can pass an `ArjunaOption` enum constant or an option name. The name string has all the flexibility seen in previous example.

Configuration Query Format
^^^^^^^^^^^^^^^^^^^^^^^^^^

As Arjuna supports a multi-configuration system, it also provides a special query syntax for retrieving configuration values.

You can use the configuration query syntax `<confname>.<option>` to retrieve configuration values for a given configuration. 

Let's say we have custom configuration with name `nconf`. 
- `browser.name` refers to the property in reference configuration.
- You can prefix a configuration name with a configuration name. For example `reference.browser.name` and `nconf.browser.name` will retrieve `browser.name` from `reference` and `nconf` configurations respectively.

Run Configurations and Environment Configurations
-------------------------------------------------

Purpose
^^^^^^^

In today's Agile environments, typically testers run automated tests with multiple configurations on multiple environments. 

These configurations could have their own respective properties (e.g. Application URL, user name, password and so on.)

In Arjuna, you can define run configurations and environment configurations very easily in your test automation framework.

Defining Data Configurations
^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Many a times, you end up using Data Driven testing when what you need is a simple data separation. 

Added to this, you might have different sets of data for different runs. 

One simple option in Arjuna is to define such data as user defined options in data configuration files. 

You can define any number of data configuration .conf files in `<Project Root Dir>/config/data>` directory.

Name of the configuration is same as the name of the file minus the extension. For example, **data1** is configuration name corresponding to **data1.conf**

Defining Environment Configuration
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

You might have multiple test environments or deployments against which you run the tests. 

For example, your web application could have a dev, staging, system and production deployment with respective URLs and other associated options. 

You can define any number of environment configuration .conf files in `<Project Root Dir>/config/env>` directory.

Name of the configuration is same as the name of the file minus the extension. For example, **tenv1** is configuration name corresponding to **tenv1.conf**


Combining Data and Environment Configurations
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Another need is that you might want to use data and environment information in combination.

Arjuna has built-in support for this and does it by default for you.

Arjuna automatically loads these files as combinations of data confs and env confs when it loads. For each combination:
    - Reference config is taken as base (which means Arjuna's internal defaults + Options that you have passed in project.conf + Default data conf (if defined) + Default env conf (if defined))
        * For default data and env conf, see the next section.
    - A given data conf is superimposed
    - A given env conf is superimposed
    - CLI options are superimposed

The config name is set to `dataconfname_envconfname` e.g. `data1_tenv1`.

You can retrieve an environment config by its name using `Arjuna.get_config` (anywhere in your project) or `request.get_config` call (in a test fixture or test function). Now you can inquire the values just like you deal with any configuration in Arjuna. 

You can also retrieve their options using the magic `C` function, for example `C("data1_tenv1.browser.name")`

Default Data Configuration and Environment Configuration
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

A data configuration with name `data.conf` is considered a default.

An environment configuration with name `env.conf` is considered a default.

What it means is that if these files are defined, then Arjuna uses options contained in them to update the reference configuration.

This feature has the following side-effects:
    * A configuration with name `data_env` is same as the reference configuration.
    * A configuration with name `data1_env` is same as `data1`
    * A configuration with name `data_tenv1` is same as `tenv1`