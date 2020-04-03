.. _configuration:

Test Configuration
==================

Understanding Configuration System of Arjuna
--------------------------------------------

- Arjuna supports tweaking its built in options which are represented by `ArjunaOption` enum. 
- Arjuna also supports user defined options.
- A `Configuration` object represents fixed values for configured settings (Arjuna options as well user defined options).
- A `Configuration` is immutable which means that once created it can not be modified.
- As a part of initialation, Arjuna creates the reference `Configuration` object which combines the following to create the reference :
    - Default settings for Arjuna options
    - Project level settings included in `<Project root directory>/config/project.conf` file.
    - Environment configuration represented by its name passed as `--run-env` switch.
    - Run-time configuration file provided with `--run-conf` switch.
    - CLI options represtedn by Arjuna's named CLI switches (e.g. for logging options)
- You can get the reference configuration by calling `Arjuna.get_config()`.
- Within test or test fixture code, we can also get the reference configuration object (if not re-assigned by test author to a non-reference configuration) using `request.config`.

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

Just like Arjuna options, you can define your own options in `project.conf` file as well as programmatically. Rest of the fundamentals remain same as Arjuna options. That's the key point! Arjuna provides you the same facilities for your own defined options that it provides to built-in `ArjunaOption`s.

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

Retrieving the values is same as retrieving `ArjunaOption`s.

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

Environment Configurations
--------------------------

Purpose
^^^^^^^

In today's Agile environments, typically testers run automated tests on multiple environments. These environments could have their own respective properties (e.g. Application URL, user name, password and so on.)

In Arjuna, you can define configurations for environments and use them very easily in your test automation framework.

Defining and Using Environment Configurations
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

You can define one or more `environment_name.conf` files exactly like a `project.conf` file. Place these files in `<Project Root>/config/env` directory. Arjuna automatically loads these files.

You can retrieve an environment config by its name using `Arjuna.get_config` or `request.get_config` call. Now you can inquire the values just like you deal with any configuration in Arjuna. You can also retrieve their options using the magic `C` function, for example `C("tevn.browser.name")`

Making an environment configuration as the default
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

You can do a session wide update that the reference configuration should utilize configuration values from a given environment config.

You can do this by providing `--run-env <env_name>` CLI switch.

Run Configuration: Overriding Configuration with a Configuration File for a Test Run 
------------------------------------------------------------------------------------

With today's integration needs, at times you might need to create a configuration outside of Arjuna test project's structure and instruct Arjuna to do a session wide update that the reference configuration should utilize configuration values from a configuration file at a given path.

You can do this by providing `--run-conf <file name or path>` CLI switch.

Combining Environment and Run Configuration
-------------------------------------------

If you pass the `--run-env` and `run-conf` switches together:
1. Arjuna first does a reference config update from run-env named conf file.
2. Then it updates the configuration with the one at run-conf path.

