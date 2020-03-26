# Arjuna Features Documentation

- [Arjuna Test Project](#arjuna-test-project)
- [Arjuna Command Line Interface](#arjuna-command-line-interface)
- [Defining a Test Function](#defining-a-test-function)
  * [The `@test` Decorator](#the---test--decorator)
  * [Running a Specific Test Function](#running-a-specific-test-function)
- [Defining Test Fixtures](#defining-test-fixtures)
- [Test Configuration](#test-configuration)
  * [Understanding Configuration System of Arjuna](#understanding-configuration-system-of-arjuna)
  * [project.conf - Setting Project Level Configuration Options](#projectconf---setting-project-level-configuration-options)
  * [Configuration Builder - Creating Custom Configurations](#configuration-builder---creating-custom-configurations)
  * [Defining and Handling User Options](#defining-and-handling-user-options)
    + [User Options in Project Conf](#user-options-in-project-conf)
    + [Adding User Options Programmatically](#adding-user-options-programmatically)
  * [Configuration Builder - Adding options from a `.conf` File](#configuration-builder---adding-options-from-a--conf--file)
  * [The Magic `C` Function](#the-magic--c--function)
    + [Purpose](#purpose)
    + [Configuration Query Format](#configuration-query-format)
  * [Environment Configurations](#environment-configurations)
    + [Purpose](#purpose-1)
    + [Defining and Using Environment Configurations](#defining-and-using-environment-configurations)
    + [Making an environment configuration as the default](#making-an-environment-configuration-as-the-default)
  * [Run Configuration: Overriding Configuration with a Configuration File for a Test Run](#run-configuration--overriding-configuration-with-a-configuration-file-for-a-test-run)
  * [Combining Environment and Run Configuration](#combining-environment-and-run-configuration)
- [Data Driven Testing](#data-driven-testing)
  * [Single data record](#single-data-record)
  * [Multiple Data Records](#multiple-data-records)
  * [Driving with Static Data Function](#driving-with-static-data-function)
  * [Driving with Static Data Generator](#driving-with-static-data-generator)
  * [Driving with Dynamic Data Function/Generator](#driving-with-dynamic-data-function-generator)
  * [Driving with Static Data Classes](#driving-with-static-data-classes)
  * [Driving with Dynamic Data Classes](#driving-with-dynamic-data-classes)
  * [Driving with Data Files](#driving-with-data-files)
    + [Driving with Excel File](#driving-with-excel-file)
    + [Driving with Delimiter-Separated File](#driving-with-delimiter-separated-file)
    + [Driving with INI File](#driving-with-ini-file)
  * [Data Files with Exclude Filter for Records](#data-files-with-exclude-filter-for-records)
  * [Driving with Multiple Data Sources](#driving-with-multiple-data-sources)
- [Contextual Data References](#contextual-data-references)
  * [Purpose](#purpose-2)
  * [Excel Data References](#excel-data-references)
  * [The Magic `R` Function](#the-magic--r--function)
- [Localizing Strings](#localizing-strings)
  * [Purpose](#purpose-3)
  * [Locale Enum](#locale-enum)
  * [Excel based Localization](#excel-based-localization)
  * [The `L` function for Localization](#the--l--function-for-localization)
  * [JSON Based Localization](#json-based-localization)
  * [Using the `L` Function with JSON Localizer](#using-the--l--function-with-json-localizer)
  * [Strict vs Non-strict mode for Localization](#strict-vs-non-strict-mode-for-localization)
- [Web Gui Automation](#web-gui-automation)
  * [The `WebApp` class](#the--webapp--class)
    + [Launching a `WebApp`](#launching-a--webapp-)
      - [Points to Note](#points-to-note)
    + [Associating a `WebApp` with a Base URL](#associating-a--webapp--with-a-base-url)
  * [Element Identification](#element-identification)
  * [The `element` Template](#the--element--template)
  * [Gui Element Locators - Using ID, Name, Tag, Class, Link Text, Partial Link Text](#gui-element-locators---using-id--name--tag--class--link-text--partial-link-text)
    + [Test Fixture for Example(s) in This Page](#test-fixture-for-example-s--in-this-page)
      - [Points to Note](#points-to-note-1)
    + [Identification using ID, Name, Class Name, Tag Name, Link Text, Partial Link Text](#identification-using-id--name--class-name--tag-name--link-text--partial-link-text)
      - [Points to Note](#points-to-note-2)
  * [Gui Element Locators - Using XPath](#gui-element-locators---using-xpath)
    + [Test Fixture for Example(s) in This Page](#test-fixture-for-example-s--in-this-page-1)
  * [Usage](#usage)
  * [Gui Element Locators - Using CSS Selectors](#gui-element-locators---using-css-selectors)
    + [Test Fixture for Example(s) in This Page](#test-fixture-for-example-s--in-this-page-2)
  * [Usage](#usage-1)
    + [Test Fixture for Example(s) in This Page](#test-fixture-for-example-s--in-this-page-3)
  * [Usage](#usage-2)
  * [Interaction with `element`](#interaction-with--element-)
    + [Test Fixture for Example(s) in This Page](#test-fixture-for-example-s--in-this-page-4)
    + [Usage](#usage-3)
      - [Points to Note](#points-to-note-3)
    + [Concise Basic Interactions with a Gui Element - You Can Write Concise Code If You Wish](#concise-basic-interactions-with-a-gui-element---you-can-write-concise-code-if-you-wish)
    + [Test Fixture for Example(s) in This Page](#test-fixture-for-example-s--in-this-page-5)
  * [Usage](#usage-4)
  * [Gui Namespace (GNS) - Externalizing Locators](#gui-namespace--gns----externalizing-locators)
    + [The GNS File](#the-gns-file)
      - [Points to note](#points-to-note)
    + [Change in project.conf](#change-in-projectconf)
  * [Gui Namespace - Externalizing ID, Name, Tag, Class, Link Text and Partial Link Text](#gui-namespace---externalizing-id--name--tag--class--link-text-and-partial-link-text)
    + [Test Fixture for Example(s) in This Page](#test-fixture-for-example-s--in-this-page-6)
      - [Points to Note](#points-to-note-4)
    + [The GNS File](#the-gns-file-1)
    + [Usage in code](#usage-in-code)
      - [Points to Note](#points-to-note-5)
  * [Gui Namespace - Externalizing XPath](#gui-namespace---externalizing-xpath)
    + [Test Fixture for Example(s) in This Page](#test-fixture-for-example-s--in-this-page-7)
      - [Points to Note](#points-to-note-6)
  * [The GNS File](#the-gns-file-2)
  * [Usage](#usage-5)
  * [Gui Namespace - Externalizing CSS Selectors](#gui-namespace---externalizing-css-selectors)
    + [Test Fixture for Example(s) in This Page](#test-fixture-for-example-s--in-this-page-8)
      - [Points to Note](#points-to-note-7)
  * [The GNS File](#the-gns-file-3)
  * [Usage](#usage-6)
  * [Gui Namespace - Externalizing Arjuna's Locator Extensions](#gui-namespace---externalizing-arjuna-s-locator-extensions)
    + [Test Fixture for Example(s) in This Page](#test-fixture-for-example-s--in-this-page-9)
      - [Points to Note](#points-to-note-8)
  * [The GNS File](#the-gns-file-4)
  * [Usage](#usage-7)
  * [Element Templates](#element-templates)
  * [Matching Multiple Elements as GuiMultiElement](#matching-multiple-elements-as-guimultielement)
    + [Test Fixture for Examples in This Page](#test-fixture-for-examples-in-this-page)
    + [Important point for GNS](#important-point-for-gns)
      - [Points to Note](#points-to-note-9)
    + [Test Code](#test-code)
      - [Points to Note](#points-to-note-10)
  * [Arjuna's DropDown Abstraction - Handling Default HTML Select](#arjuna-s-dropdown-abstraction---handling-default-html-select)
    + [Test Fixture for Examples in This Page](#test-fixture-for-examples-in-this-page-1)
    + [Important point for GNS](#important-point-for-gns-1)
      - [Points to Note](#points-to-note-11)
    + [Usage](#usage-8)
    + [Points to Note](#points-to-note-12)
  * [Arjuna's RadioGroup Abstraction - Handling Default HTML Radio Group](#arjuna-s-radiogroup-abstraction---handling-default-html-radio-group)
    + [Test Fixture for Examples in This Page](#test-fixture-for-examples-in-this-page-2)
    + [Important point for GNS](#important-point-for-gns-2)
      - [Points to Note](#points-to-note-13)
    + [Usage](#usage-9)
    + [Points to Note](#points-to-note-14)
  * [Gui Abstraction using `WebApp`, `Page` and `Section` classes](#gui-abstraction-using--webapp----page--and--section--classes)
  * [Arjuna's Gui Loading Model](#arjuna-s-gui-loading-model)
  * [Helper Classes, Functions and Enums](#helper-classes--functions-and-enums)
  * [Arjuna Exceptions](#arjuna-exceptions)

<small><i><a href='http://ecotrust-canada.github.io/markdown-toc/'>Table of contents generated with markdown-toc</a></i></small>



## Arjuna Test Project

A fixed project structure to be followed for an Arjuna test project. This brings consitency across mutliple test automation implementations within and outside your organization.

Following are critical project directories, sub-directories and files. *Arjuna could be creating other directories corresponding to some in-progress or experimental features. They are not listed here.*

Please also note that some of these directories are mandatory as a part of Arjuna test project structure. When you create project using `create-project` command from Arjuna CLI, Arjuna places `placeholder.txt` files so that when you check-in your code in a code repository, empty directories are not ignored during check-in. It is advised to retain them, until you make use of them by placing files in them as per your project needs.

- **config**: Contains configuration files.
  - **project.conf**: Your project's configuration file containing project-level configuration settings.
  - **env**: This directory can contain any number of conf files that correspond to options for run-environments.
  - If you place any `.conf` files directly in this directory or in a sub-directory herein, they can be found by Arjuna using the name or relative path.
- **data**: Contains files that act as data sources and data references (WIP).
    - **source**: Data source files go here.
    - **reference**: Data reference files go here.
        - **column**: Excel Column Data References for auto-loading
        - **row**: Excel Row Data References for auto-loading
- **l10n**: Contains localizaation files
    - **excel**: Excel based localization files go here.
    - **json**: Json based localization directories and files go here.
- **guiauto**: Contains GUI automation related files.
  - **driver**: Arjuna automatically downloads drivers. In case you switch this off in a configuration, Arjuna picks Selenium driver executables from this directory in respective OS folders.
  - **namespace**: GNS (Gui Namespace) files go here.
  - **withx**: Contains With extensions
    - **withx.yaml**: You can define custom identifiers in this file in YAML format. These can be referred to across the project in GNS files.
 - **report**: Reports are generated here. Each test run is associated with a run-id.
    - **Timestamp-RunID**: Root directory of report for a given run. If `--static-rid` is provided then the directory is named as the run id that you provide with `-rid` CLI option or as the default run id which is `mrun`.
      - **html**: HTML report (report.html) generated by pytest-html plugin goes here.
      - **log**: arjuna.log file can be found here.
      - **screenshot**: Contains screenshots taken for a test run.
      - **xml**: JUnit-style XML report (report.xml) goes here. It is primarily meant for Jenkins or other CI software intergrations with Arjuna.
 - **test**: Contains test files. As of now Arjuna supports coded tests only.
    - **module**: Coded tests are written as Python modules and are placed here. Sub-packaging of modules is allowed.
    - **conftest.py**: This is pytest's conftest.py file 
- **script**: This directory is meant to contain Arjuna scripts (or your own custom scripts or batch files.)
  - **arjuna_launcher.py**: This is the script which is used to run your tests by invoking Arjuna.

## Arjuna Command Line Interface

Pending

## Defining a Test Function

Writing a basic test in Arjuna is very easy. Following is a simple test skeleton:

### The `@test` Decorator

```python

from arjuna import *

@test
def check_test_name(request):
    pass
```

1. Create a test module in `<Project Root Directory>/test/module`. The module name should start with the prefix `check_`
2. In the python test module file, import all names from Arjuna: `from arjuna import *`. Ofcourse, as you become more aware of Arjuna's TPI (tester programming interface), you can do selective imports using Python.
3. Create a test. In Arjuna, a test is a function marked with `@test` decorator. It must start with the prefix `check_`. It should take **one mandatory argument**: `request`.
4. The contents of the test function depend on the test that you want to write.

### Running a Specific Test Function
You can run this test by running `arjuna_launcher.py` Python script in the `script` directory of the project:

`python arjuna_launcher.py run-selected -it check_test_name`

## Defining Test Fixtures

Pending

## Test Configuration

### Understanding Configuration System of Arjuna
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

### project.conf - Setting Project Level Configuration Options

Many a times, it is useful to change the defaults of Arjuna at project level to avoid writing code every time. It is also a much better way when you need to tweak quite a few settings and you know that those settings are applicable to most of your tests.

In Arjuna you can do this by providing options under `arjunaOptions` section in `<Project root directory>/config/project.conf` file. The contents of `arjunaOptions` follow [HOCON](https://github.com/lightbend/config/blob/master/HOCON.md) syntax. This means that you can write settings in properties syntax, as JSON or as human-readable JSON syntax supported by HOCON.

For example:

```javascript

arjunaOptions {
    browser.name = firefox
}
```

Add the above content to `project.conf` file. We want to tweak `ArjunaOption.BROWSER_NAME`. Correspondingly you can add entry for `BROWSER_NAME` in `arjunaOptions`. For being more intuitive and less mistake prone, Arjuna supports keys in this section as **case-insensitive** and treats **. (dot)** and **_ (underscore)** as interchangeable. This is similar to the behavior of option name string seen in previous section.

### Configuration Builder - Creating Custom Configurations

In Arjuna, you can create your own configurations as well. You can do this by using reference Configuration or any other configuration created by you as the source object.

Given a `Configuration` object (say `config`), you can get a `ConfigBuilder` object with `config.builder` property. You can add options to the builder and then call its `register` method to create a new configuration. This newly created configuration is returned by the `register` call.

Sometimes it is useful to provide your own name to the custom configuration that you are creating. Arjuna helps you in creating the configuration in one place and retrieving it in another place. You need not pass the configuration object around for simple needs of this nature. To achieve this pass the name while registering: `register(<name>)`. It can also now be retrived anywhere in your project with the `Arjuna.get_config(<name>)` call. Within a test, it can also be retrieve by using `request.get_config(<name>)` call.

`ConfigBuilder` also provides direct methods for some commonly used Arjuna Options. For example `.firefox()` is equivalent to `.option("browser.name", BrowserName.FIREFOX)`

### Defining and Handling User Options

Just like Arjuna options, you can define your own options in `project.conf` file as well as programmatically. Rest of the fundamentals remain same as Arjuna options. That's the key point! Arjuna provides you the same facilities for your own defined options that it provides to built-in `ArjunaOption`s.

#### User Options in Project Conf
In Arjuna you can define your own option under `userOptions` section in `<Project root directory>/config/project.conf` file.

```javascript

userOptions {
    target.url = "https://google.com"
}
```

#### Adding User Options Programmatically
You can also add user options programmatically using the `ConfigBuilder` object just like we use it for tweaking Ajuna's builtin-options.

Retrieving the values is same as retrieving `ArjunaOption`s.

### Configuration Builder - Adding options from a `.conf` File

`ConfigBuilder` can also load Arjuna options as well user options from `.conf` files. It comes handy when you have a controlled set of configurations which want to create at run-time. It could be also helpful if for some reasons your logic involves clubbing of options from multiple files.

You can load options from any file using `from_file` method of `ConfigBuilder` and providing the file path.

### The Magic `C` Function

#### Purpose 
Arjuna provides a special function `C` for retrieving values from the reference configuration as it is a very common operation to do on test code. You can pass an `ArjunaOption` enum constant or an option name. The name string has all the flexibility seen in previous example.

#### Configuration Query Format

As Arjuna supports a multi-configuration system, it also provides a special query syntax for retrieving configuration values.

You can use the configuration query syntax `<confname>.<option>` to retrieve configuration values for a given configuration. 

Let's say we have custom configuration with name `nconf`. 
- `browser.name` refers to the property in reference configuration.
- You can prefix a configuration name with a configuration name. For example `reference.browser.name` and `nconf.browser.name` will retrieve `browser.name` from `reference` and `nconf` configurations respectively.

### Environment Configurations

#### Purpose
In today's Agile environments, typically testers run automated tests on multiple environments. These environments could have their own respective properties (e.g. Application URL, user name, password and so on.)

In Arjuna, you can define configurations for environments and use them very easily in your test automation framework.

#### Defining and Using Environment Configurations
You can define one or more `environment_name.conf` files exactly like a `project.conf` file. Place these files in `<Project Root>/config/env` directory. Arjuna automatically loads these files.

You can retrieve an environment config by its name using `Arjuna.get_config` or `request.get_config` call. Now you can inquire the values just like you deal with any configuration in Arjuna. You can also retrieve their options using the magic `C` function, for example `C("tevn.browser.name")`

#### Making an environment configuration as the default

You can do a session wide update that the reference configuration should utilize configuration values from a given environment config.

You can do this by providing `--run-env <env_name>` CLI switch.

### Run Configuration: Overriding Configuration with a Configuration File for a Test Run 

With today's integration needs, at times you might need to create a configuration outside of Arjuna test project's structure and instruct Arjuna to do a session wide update that the reference configuration should utilize configuration values from a configuration file at a given path.

You can do this by providing `--run-conf <file name or path>` CLI switch.

### Combining Environment and Run Configuration

If you pass the `--run-env` and `run-conf` switches together:
1. Arjuna first does a reference config update from run-env named conf file.
2. Then it updates the configuration with the one at run-conf path.

## Data Driven Testing
Driving an automated test with data is a critical feature in test automation frameworks.

Here, we will explore various flexible options available in Arjuna for data driven testing.

You can supply `drive_with` argument to the `@test` decorator to instruct Arjuna to associate a `Data Source` with a test. Depending on the needs, as described below, you use Arjuna's markup for different types of data sources.

### Single data record

Sometimes, the need is simple. You have a single data record, but want to separate it from the test code for the sake of clarity.

This need is solved with the `record` markup of Arjuna. You can provide any number of positional or named arugments.

```python
from arjuna import *

@test(drive_with=record(1, True, a='something', b='anything'))
def check_pos_data(request, data):
    pass
```

1. We provide `drive_with` argument to the `@test` decorator.
2. To specify a single data record, we call the `record` factory function.
3. `record` can take any number of positional or keyword arguments.
4. The signature of the test now contains a `data` argument.
5. Within the body of the tests, you access the positional values using indices (e.g. `data[0]`)
6. You can retrieve named values using a dictionary syntax (e.g. `data['a']`) or dot syntax (e.g. `data.a`).
7. Names are case-insensitive. `data['a']`, `data['A']`, `data.a` and `data.A` mean the same thing.

### Multiple Data Records

You use the `records` factory function to provide multiple records. It can contain any number of `record` entries. The test will be repeated as many times as the number of records (2 in this example.)

```python

from arjuna import *

@test(drive_with=
    records(
        record(1,2,sum=3),
        record(4,5,sum=9),
    )
)
def check_records(request, data):
    pass
```

The report will contain separate entries for each test. The name will indicate the data used. (e.g. `test/module/check_04_dd_records.py::check_records[Data-> Indexed:[7, 8] Named:{sum=10}]`)

Retrieval of data values is done exactly the same way as in case of a single data record.


### Driving with Static Data Function

Rather than including static data in Python code, one might want to generate data or pull data from an external service to create data records.

A simple way to achieve this is to write a data function. A static data function always behaves in the same manner.

```python

@test(drive_with=data_function(func))
def check_static_data_func(request, data):
    pass
```

We use `data_function` factory function to associate the data function with the test function Retrieval of values is same as earlier.

### Driving with Static Data Generator
You can also use a Python generator instead of a normal function:

```python

@test(drive_with=data_function(data_generator))
def check_generator_func(request, data):
    pass
```

### Driving with Dynamic Data Function/Generator
Another advanced measure that you can take is creating a data function which acts on the arguments supplied by you to govern the data it returns/generates.

```python
from arjuna import *

@test(drive_with=data_function(dynamic_data_func, 8, "something", a="whatever", b=1))
def check_dynamic_data_func(request, data):
    pass
```

Data functions can take any number of arguments - positional as well as named. You supply the arguments in the `data_function` builder function to control the data function.

### Driving with Static Data Classes

Instead of a function, you can also represent your data generation logic as a data class. The Data Class must implement Python's Iteration Protocol. A static data class always behaves in the same manner.


```python
@test(drive_with=data_class(MyDataClass))
def check_data_class(request, data):
    pass
```

We use `data_class` factory function to associate the data class with the test function. Retrieval of values is same as earlier.

### Driving with Dynamic Data Classes

Another advanced measure that you can take is creating a data class which acts on the arguments supplied by you to govern the data it generates.

```python
# arjuna-samples/arjex_data/test/module/check_07_dd_dynamic_class.py

from arjuna import *

@test(drive_with=data_class(MyDataClass, 8, "something", a="whatever", b=1))
def check_dynamic_data_class(request, data):
    pass
```

Data classes can take any number of arguments - positional as well as named. You supply the arguments in the `data_class` factory function to control the data class.

### Driving with Data Files

For large, static data it might be useful to externalize the data completely outside of Python code.

Arjuna supports data externalization in XLS, TSV/CSV and INI files out of the box.

You can use `data_file` factory function to specify a data file. Arjuna determines the loader based on the file extension.

The files are automatically picked up from `Data Sources directory` which is `<Project Root>/data/source`.

#### Driving with Excel File

An excel data file can contain data in following format. (Only .xls files are supported as of now)

<img src="img/inputxls.png">

```python
from arjuna import *

@test(drive_with=data_file("input.xls"))
def check_drive_with_excel(request, data):
    pass
```

#### Driving with Delimiter-Separated File

An delimiter-separated data file can contain data in following format. The delim 

**.txt**

```text
Left	Right	Sum
1	2	3
4	5	8
```

**.csv**

```text
Left,Right,Sum
1,2,3
4,5,8
```

```python
from arjuna import *

@test(drive_with=data_file("input.txt"))
def check_drive_with_tsv(request, data):
    pass

@test(drive_with=data_file("input.csv", delimiter=","))
def check_drive_with_csv(request, data):
    pass
```

Default delimiter is `tab`. If you use any other delimiter, you can pass it as `delimiter` argument.

#### Driving with INI File

An INI data file can contain data in following format.

```ini

[Record 1]
Left = 1
Right = 2
Sum = 3

[Record 2]
Left = 4
Right = 5
Sum = 8
```

```python
from arjuna import *

@test(drive_with=data_file("input.ini"))
def check_drive_with_ini(request, data):
    pass
```

### Data Files with Exclude Filter for Records

At times, you might want to selectively mark records in data files to be excluded from consideration.

You can do this by adding a column named `exclude` and set it to `y/yes/true` to exclude a record.

For delimiter-separated-files, you can also comment a record by putting a `#` at the beginning.

For INI files, you can also comment a complete record by using `;` which is the commenting symbol for INI files.

### Driving with Multiple Data Sources

You can associate multiple data sources with a single test in Arjuna.

We can achieve this by using the `many_data_sources` factory function.

```python
from arjuna import *

@test(drive_with=many_data_sources(
    record(left=1, right=2, sum=3),
    records(
        record(left=3, right=4, sum=7),
        record(left=7, right=8, sum=10)
    ),
    data_function(myrange),
    data_class(MyDataClass),
    data_file("input.xls")
))
def check_drive_with_many_sources(request, data):
    pass
```

The data sources are picked up sequentially with this construct.

## Contextual Data References

### Purpose
There are various situations in which you need contextual data. Such a need is catered by the concept of Contextual Data References (or simply Data References) in Arjuna.

Consider the following example:
1. You have 3 types of user accounts - `Bronze`, `Silver` and `Gold`.
2. The user account information includes a `User` and `Pwd` to repesented user name and password representing a given account type.
3. In different situations, you want to use the user accounts and retrieve them by the context name from a single source of information.

### Excel Data References

Arjuna supports Excel based data references out of the box. These reference files are automatically loaded when `Arjuna.init()` is called by Arjuna launcher.

There are two types of Excel based Data References that you can create in Arjuna:

**Column Data References**

You place such files in `<Project Root>/data/reference/column` directory. A reference file can be found in this example project.

<img src="img/colref.png">

In a column data reference file, the context of data is represented by columns. Here Account Type's values -  `Bronze`, `Silver` and `Gold` represent the contexts, for which the `User` and `Pwd` values are different.

**Row Data References**

You place such files in `<Project Root>/data/reference/row` directory. A reference file can be found in this example project.

<img src="img/rowref.png">

In a row data reference file, the context of data is represented by cells of the first column. Here Account Type's values - `Bronze`, `Silver` and `Gold` represent the contexts, for which the `User` and `Pwd` values are different.

### The Magic `R` Function
You can access data references in your test code with Arjuna's magic `R` function (similar to `L` and `C` functions seen in other features).

It has the following signature. The first argument is the query. `bucket` and `context` are optional arguments.

```python
R("user", bucket=<bucket_name>, context=<context_name>))
```

1. The name of the file is the `bucket` name. For example, here `cusers` and `rusers` are buckets represenating `cusers.xls` and `rusers.xls` data reference files.
2. You can retrieve values from the data reference with a combination of `query`, `bucket` and `context` combinations.
    - Query can contain just the ref name and bucket and context arguments can be provided.
    - Query can be of format `context.refname` and bucket can be supplied as argument.
    - Query can be of format `bucket.context.refname` without passing bucket and context arguments separately.
3. The only difference between the two styles of references is the format and the way Arjuna loads them. Usage for a test author is exactly the same.

## Localizing Strings

### Purpose
As a part of automating tests, a test author might need to deal with localization of strings that are used for various purposes.

Arjuna supports Excel based localization data out of the box. These files are automatically loaded when `Arjuna.init()` is called by Arjuna launcher.

### Locale Enum

Arjuna associates locale for localization with the Locale enum constant which in turn uses the names from Python.

The default locate is `Locale.EN`. It can be changed in a project configuration as follows:

```
# project.conf

arjunaOptions {
    l10n.locale = hi
}
```

### Excel based Localization

**Sample Localization File**

The localization file follows the format of Excel Column Data Reference files.

You place such files in `<Project Root>/l10n/excel` directory. Two reference files can be found in this example project.

<img src="img/l10_1.png">

First column is always the Reference column. The other columns represent the languages mentioned as `Locale` type in column heading.

In the example file, the columns mentions `en` and `hi` which are Locale value for English and Hindi respectively.

For demonstration purpose, 3 English words are provided with corresponding strings in Hindi.

<img src="img/l10_2.png">

The second file `sample2.xls` has the same data except the localized string for `Correct` in Hindi which is different from `sample1.xls`.

### The `L` function for Localization

You can access data references in your test code with Arjuna's magic `L` function (similar to `C` and `R` functions seen in other features).

It has the following signature. The first argument is the query. `locale`, `bucket` and `strict` are optional arguments.

```python
L("qual", locale=<local enum constant or string>, bucket=<bucket_name>, strict=<True or False>)
```

- `L("Testing")` localizes the string as per the `ArjunaOption.L10_LOCALE` value in reference configuration. In `project.conf`, we have set it as `HI`.
- You can also explcitily mention the locale as `Locale.HI`.
- When a name is repeated across multiple localization files (buckets), the last one holds. `L("Correct")` will give the value from `sample2` file as it is loaded after `sample1`.
- You can explcitily refer to a bucket by providing the `bucket` argument. Each Excel localization file represents a bucket and its name without the extension is the bucket name.
- You can also provide the bucket name by prefixing it before the reference key, for example `sample1.corr`.
- `strict` argument is to switch strict node on or off.

### JSON Based Localization

**Sample Localization Files**

With JSON format, there is a specific structure expected. The sample files are placed in `<Project Root>/l10n/json` directory.

Following is the sample JSON localization structure:

```
json
├── bucket1
│   ├── de-DE.json
│   └── en-GB.json
├── bucket2
│   ├── de-DE.json
│   └── en-GB.json
├── de-DE.json
└── en-GB.json
```

1. Each directory represents a bucket with the name as that of directory. The concept is similar to an Excel file representing a bucket as discussed above.
2. The root directory represents the `root` bucket.
3. For a given bucket, the localization data for a `Locale` is kept in a file named `<locale>.json`.

**Sample JSON Content**

Following is the content of one such file in root directory for German localization:

```JSON
{
  "address": {
    "address": "Adresse",
    "city": "Stadt",
    "coordinates": "Koordinaten",
    "country": "Land",
    "houseNumber": "Hausnummer",
    "latitude": "Breitengrad",
    "location": "Ort",
    "longitude": "Längengrad",
    "postalCode": "Postleitzahl",
    "streetName": "Straße"
  },

  "shared": {
    "back": "zurück",
    "cancel": "Abbrechen"
  }
}
```

1. Each JSON path of keys repesents a string to be localized. 
2. The key names should be kept same across language files.
3. `Key1.Key2...KeyN` is the flattened syntax to refer a localized string e.g. `address.coordinates`

### Using the `L` Function with JSON Localizer

Consider the following localization calls:

```python
L("error.data.lastTransfer", locale=Locale.EN_GB) # From global l10n container
L("error.data.lastTransfer", locale=Locale.DE_DE) # From global l10n container

L("error.data.lastTransfer", locale=Locale.EN_GB, bucket="bucket2") # From bucket2    
L("bucket2.error.data.lastTransfer", locale=Locale.EN_GB) # From bucket2

L("address.coordinates", locale=Locale.EN_GB, bucket="bucket2")
L("address.coordinates", locale=Locale.EN_GB, bucket="root")
L("root.address.coordinates", locale=Locale.EN_GB)
```

1. Use the flattened key syntax as discussed earlier. 
2. The key names should be kept same across language files.
3. `Key1.Key2...KeyN` is the flattened syntax to refer a localized string e.g. `address.coordinates`
4. Files in root localization directory are available in `root` bucket.

### Strict vs Non-strict mode for Localization

By default, Arjuna handles localization in a non-strict mode. This means if localized string is absent for a given reference, it ignores the error and returns the reference as return value.

```python
L("non_existing")
L("non_existing", strict=True, locale=Locale.DE_DE)
```

1. As by default the strict mode if off, `L("non_existing")` returns `non_existing`.
2. You can enforce strict behavior by providing the `strict=True` argument to the `L` function. The second print statement in above code will raise an exception.
3. You can switch on strict mode at the project level by including `l10n.strict = True` in the `project.conf` file.

## Web Gui Automation

### The `WebApp` class

Learning Web UI test automation in Arjuna starts with the concept of `WebApp` object.

A web application is represented using a `WebApp` object. To automate your web application, you create an instance of `WebApp` and call its methods or methods of its objects for automation purpose.

Web automation facilities in Arjuna use Selenium as the underlying browser automation library.

#### Launching a `WebApp`

```python
# arjuna-samples/arjex/test/module/check_01_webapp.py

@test
def check_webpp_nobase_url(request):
    google = WebApp()
    google.launch(blank_slate=True)
    google.go_to_url("https://google.com")
    request.asserter.assert_equal("Google", google.title, "Page title does not match.")
    google.quit()
```

##### Points to Note
1. We create an object of `WebApp`. By default, `WebApp` uses Arjuna's reference `Configuration`. In turn, it uses the corresponding options to launch the underlying automator. You can change this by passing the `Configuration` object using `config` argument of the WebApp constructor.
2. We launch the `WebApp`. We pass `blank_slate` as `True` as no base URL is associated as of now with the `WebApp` (see next section).
3. Here the `WebApp` uses the reference `Configuration` of Arjuna where default browser is Chrome. So, Chrome is launched as the browser.
4. We use its `go_to_url` method to go to Google search page.
5. We use `request.asserter` for asserting the title.
6. We quit the app using `quit` method of `WebApp`.

#### Associating a `WebApp` with a Base URL

We can associated the `WebApp` with a base URL by providing `base_url` arg while creating its object. Now the app knows where to go when it is launched. If this represents your situation (which mostly is the case), then it leads to much simpler code as follows:

```python
# arjuna-samples/arjex/test/module/check_01_webapp.py

@test
def check_webpp_nobase_url(request):
    google = WebApp(base_url="https://google.com")
    google.launch()
    request.asserter.assert_equal("Google", google.title, "Page title does not match.")
    google.quit()
```

During initilization, `WebApp` automatically looks for the `ArjunaOption.APP_URL` option in the `Configuration` object associated with it. It means you can provide this option in any of the following ways:
- Modify Reference `Configuration`
  - Add this option in `project.conf` file.
  - Provide it as a CLI option.
 - Use RunContext to update or create a new `Configuration`. Pass it as argument while instantiating `WebApp`. This is what we will for this example:
 
 
```python
# arjuna-samples/arjex/test/module/check_01_webapp.py

 @test
def check_webpp_base_url_in_custom_config(request):
    cb = request.config.builder
    cb.option(ArjunaOption.APP_URL, "https://google.com")
    config = cb.register()

    google = WebApp(config=config)
    google.launch()
    request.asserter.assert_equal("Google", google.title, "Page title does not match.")
    google.quit()
```

### Element Identification

### The `element` Template

A single node in the DOM of a web UI is represented by a GuiElement object in Arjuna, irrespective of its type. This is unless you need specialized methods which we will see later.

### Gui Element Locators - Using ID, Name, Tag, Class, Link Text, Partial Link Text

Arjuna supports the locators which are supported by Selenium's By object. Apart from these, there are various abstracted locators which Arjuna provides for easier coding.

For this section, we'll use the login page of WordPress CMS. The elements of interest are the **User Name** field and the **Lost Your Password?** link.

<img src="img/wp_login.png" height="500" width="500">

In the above page, the HTML for the **User Name** field is:

```html
<input type="text" name="log" id="user_login" class="input" value="" size="20">
```

and for **Lost Your Password?** link is:

```html
<a href="/wp-login.php?action=lostpassword" title="Password Lost and Found">Lost your password?</a>
```

#### Test Fixture for Example(s) in This Page

We are going to use a test-level fixture for the examples.

Following user options have been added to `project.conf` for this fixture to work

```javascript
        userOptions {
	        wp.app.url = "IP address"
	        wp.login.url = ${userOptions.wp.app.url}"/wp-admin"
        }
```

Below is the `@for_test` fixture code:

```python
# arjuna-samples/arjex/lib/fixture/test.py

@for_test
def wordpress(request):
    # Setup
    wp_url = C("wp.login.url")
    wordpress = WebApp(base_url=wp_url)
    wordpress.launch()
    
    yield wordpress
    
    # Teadown    
    wordpress.quit()
```

##### Points to Note
1. We retrieve the Login page URL for Wordpress from `Configuration`.
2. We create a `WebApp` instance and supply the above URL as the `base_url` argument. Use a WordPress deployment of choice. For example code creation, a VirtualBox image of Bitnami Wordpress was used.
3. We launch the app.
4. We yield this app object so that it is available in the tests.
5. In the teadown section, we quit the app using `quit` method of the app.

#### Identification using ID, Name, Class Name, Tag Name, Link Text, Partial Link Text

```python
# arjuna-samples/arjex/test/module/web_ui_basics/check_02_locators_basic_locate.py

from arjuna import *

def check_basic_identifiers(request, wordpress):
    # user name field.
    # Html of user name: <input type="text" name="log" id="user_login" class="input" value="" size="20">
    wordpress.element(id="user_login")
    wordpress.element(name="log")
    wordpress.element(tag="input")
    wordpress.element(classes="input")

    # Lost your password link
    # Html of link: <a href="/wp-login.php?action=lostpassword" title="Password Lost and Found">Lost your password?</a>
    # Partial Link text match
    wordpress.element(link="password")
    # Full Link text match
    wordpress.element(flink="Lost your password?")
```

##### Points to Note
1. Launch the WebApp. Use a WordPress deployment of choice. For example code creation, a VirtualBox image of Bitnami Wordpress was used.
2. You can create an element by using `<app object>.element(<locator_type>=<locator_value>)` syntax. For example, `wordpress.element(id="user_login")` will find an element with id.
3. The locator strategy is expressed using locator type names supported by Arjuna. You can pass it as a keyword argument `k=v` format to the the `element` call. Here, we are using the following basic locators, which have one to one mapping to Selenium's equivalent identifiers using By object.
- **`id`** : Wraps By.id
- **`name`** : Wraps By.name
- **`tag`** : Wraps By.tag_name
- **`classes`** : Wraps By.class_name, however it supports compound classes. See Arjuna Locator Extensions page for more information.
- **`link`** : Wraps By.partial_link_text. Note that all content/text matches in Arjuna are partial matches (opposite of Selenium).
- **`flink`** : Wraps By.link_text (short for Full Link)

### Gui Element Locators - Using XPath

We use **`xpath`** locator for identification using XPath. It is a direct wrapper on By.xpath in Selenium. Following are various samples.

#### Test Fixture for Example(s) in This Page

Same as Basic locators example.

### Usage

```python
# arjuna-samples/arjex/test/module/web_ui_basics/check_03_locators_xpath.py

from arjuna import *

@test
def check_xpath(request, wordpress):
    # Based on Text
    wordpress.element(xpath="//*[text() = 'Lost your password?']")

    # Based on partial text
    wordpress.element(xpath="//*[contains(text(), 'Lost')]")

    # Based on Title
    wordpress.element(xpath="//*[@title = 'Password Lost and Found']")

    # Based on Value
    wordpress.element(xpath="//*[@value = 'Log In']")

    # Based on any attribute e.g. for
    wordpress.element(xpath="//*[@for = 'user_login']")

    # Based on partial content of an attribute
    wordpress.element(xpath="//*[contains(@for, '_login')]")

    # Based on element type
    wordpress.element(xpath="//*[@type ='password']")
```

### Gui Element Locators - Using CSS Selectors

We use **`selector`** locator for identification using CSS Selector. It is a direct wrapper on By.css_selector in Selenium.

#### Test Fixture for Example(s) in This Page

Same as Basic locators example.

### Usage

```python
# arjuna-samples/arjex/test/module/web_ui_basics/check_04_locators_css_selector.py

from arjuna import *

@test
def check_selector(request, wordpress):

    # Based on any attribute e.g. for
    wordpress.element(selector="*[for = 'user_login']")

    # Based on partial content of an attribute
    wordpress.element(selector="*[for *= '_login']")

    # Based on element type
    wordpress.element(selector="*[type ='password']")

    # Based on compound classes
    wordpress.element(selector=".button.button-large")
```


Arjuna provides various higher level locator strategies in addition to wrapping Selenium's By-style strategies. Following is the list of these extensions:
- **`text`** : Generates Partial Text based XPath
- **`ftext`** : Generates Full Text based XPath
- **`title`** : Generates Title Match CSS Selector
- **`value`** : Generates Value Match CSS Selector
- **`attr`** : Generates Partial Attribute Value Match CSS Selector
- **`fattr`** : Generates Full Attribute Match CSS Selector
- **`classes`** : Supports compound classes (supplied as a single string or as multiple separate strings)
- **`point`** : Runs a JavaScript to find the GuiElement under an XY coordinate
- **`js`** : Runs the supplied JavaScript and returns GuiElement representing the element it returns.

#### Test Fixture for Example(s) in This Page

Same as Basic locators example.

### Usage

```python
# arjuna-samples/arjex/test/module/web_ui_basics/check_05_locators_arjuna_exts.py

from arjuna import *

@test
def check_arjuna_exts(request, wordpress):

    # Based on partial text
    wordpress.element(text="Lost")

    # Based on Full Text
    wordpress.element(ftext="Lost your password?")

    # Based on Title
    wordpress.element(title="Password Lost and Found")

    # Based on Value
    wordpress.element(value="Log In")

    # Based on partial match of content of an attribute
    wordpress.element(attr=Attr("for", "_login"))

    # Based on full match of an attribute
    wordpress.element(fattr=Attr("for", "user_login"))

    # Based on element type
    wordpress.element(type="password")

    # Based on compound classes
    wordpress.element(classes="button button-large")
    wordpress.element(classes=("button", "button-large"))

    # Based on Point (location in terms of X,Y co-ordinates)
    wordpress.element(point=Point(1043, 458))

    # With Javascript
    wordpress.element(js="return document.getElementById('wp-submit')")
```

### Interaction with `element`


To interact with a GuiElement, from automation angle it must be in an interactable state. In the usual automation code, a test author writes a lot of waiting related code (and let's not even touch the `time.sleep`.).

Arjuna does a granular automatic waiting of three types:
- Waiting for the presence of an element when it is attempting to identify a GuiElement
- Waiting for the right state (for example, clickability of an GuiElement when you enter text or want to click it)
- Waiting for interaction to succeed (Arjuna, for example, retries click if interaction exception is raised).

Following user options have been added to `project.conf` for this test to work:

```javascript
        userOptions {
	        wp.app.url = "IP address"
	        wp.login.url = ${userOptions.wp.app.url}"/wp-admin"
	        wp.logout.url = ${userOptions.wp.app.url}"/wp-login.php?action=logout"

            wp.admin {
                name = "<username>"
                pwd = "<password>"
            }
        }
```

We will simulate WordPress login. Following are the steps:
1. Enter user name and password.
2. Click Submit button.
3. As mouse actions have not been discussed so far, we will directly go to the logout URL.
4. In the process, WordPress shows some confirmation and success messages.

#### Test Fixture for Example(s) in This Page

Same as Basic locators example.

#### Usage

```python
# arjuna-samples/arjex/test/module/web_ui_basics/check_06_basicinteract_raw.py

@test
def check_wp_login(request, wordpress):
    user = C("wp.admin.name")
    pwd = C("wp.admin.pwd")
    
    # Login
    user_field = wordpress.element(id="user_login")
    user_field.text = user

    pwd_field = wordpress.element(id="user_pass")
    pwd_field.text = pwd

    submit = wordpress.element(id="wp-submit")
    submit.click()

    wordpress.element(classes="welcome-view-site")

    # Logout
    url = C("wp.logout.url")
    wordpress.go_to_url(url)

    confirmation = wordpress.element(link="log out")
    confirmation.click()

    wordpress.element(text="logged out")
```

##### Points to Note
1. We retrieve user name and password from the user options specified in `project.conf`.
2. We identify different elements as discussed earlier.
3. For setting text of an element we can set the value for its `text` property.
4. To click an element, we can call its `click` method.
5. What you will notice is that there is no waiting logic in the test code.


#### Concise Basic Interactions with a Gui Element - You Can Write Concise Code If You Wish

Code style could be a very personal thing. If you are looking for a concise coding option, you can write the previous code as follows with exact same functionality:

#### Test Fixture for Example(s) in This Page

Same as Basic locators example.

### Usage

```python
# arjuna-samples/arjex/test/module/web_ui_basics/check_07_basicinteract_refined.py

from arjuna import *

@test
def check_wp_login_concise(request, wordpress):
    
    user = C("wp.admin.name")
    pwd = C("wp.admin.pwd")
    
    # Login
    wordpress.element(id="user_login").text = user
    wordpress.element(id="user_pass").text = pwd
    wordpress.element(id="wp-submit").click()
    wordpress.element(classes="welcome-view-site")

    # Logout
    url = C("wp.logout.url")
    wordpress.go_to_url(url)
    wordpress.element(link="log out").click()
    wordpress.element(text="logged out")
```



### Gui Namespace (GNS) - Externalizing Locators


After launching a `WebApp`, apart from basic browser operations, most of times an automated test finds and interacts with Gui elements.

Externalizing of identifiers is built into Arjuna. The object which contains identification information and related meta-data of a Gui is referred to as `GuiNamespace (GNS)` in Arjuna.

#### The GNS File

Arjuna uses YAML as the format for externalization of identifiers. Fow now, we will discuss basic usage of the format.

Following is the high level format for simple usage. We will explore practical implementations in the later sections.

```YAML
labels:

  <label1>:
    <locator type>: <locator data>

  <label2>:
    <locator type>: <locator data>

  <labelN>:
    <locator type>: <locator data>
```

##### Points to note
1. This file has a `YAML` extension.
2. All labels are placed under `labels` heading.
3. Each label represents element identification information which can be later referenced by this label.
3. The label should be a valid Arjuna name.
4. In its basic usage format, the section has a key value pair for a given locator type. For example `id: user_login`.
5. Labels are treated as **case-insensitive** by Arjuna.

#### Change in project.conf

We are going to use a test-level fixture for the examples.

Following user options have been added to `project.conf` for this fixture to work

```javascript
        userOptions {
	        wp.app.url = "IP address"
	        wp.login.url = ${userOptions.wp.app.url}"/wp-admin"
        }
```

### Gui Namespace - Externalizing ID, Name, Tag, Class, Link Text and Partial Link Text

#### Test Fixture for Example(s) in This Page

Below is the `@for_test` fixture code:

```python
# arjuna-samples/arjex/test/module/check_02_guielement.py

@for_test
def wordpress(request):
    # Setup
    wp_url = C("wp.login.url")
    wordpress = WebApp(base_url=wp_url, label="BasicIdentification")
    wordpress.launch()
    
    yield wordpress
    
    # Teadown    
    wordpress.quit()
```

##### Points to Note
1. We retrieve the Login page URL for Wordpress from `Configuration`.
2. We create a `WebApp` instance and supply the above URL as the `base_url` argument. Use a WordPress deployment of choice. For example code creation, a VirtualBox image of Bitnami Wordpress was used.
3. To instruct Arjuna to pick up a GNS file for a given name, we can provide the `label` argument. Now it will look for `BasicIdentification.yaml` in project's Gui Namespace directory.
3. We launch the app.
4. We yield this app object so that it is available in the tests.
5. In the teadown section, we quit the app using `quit` method of the app.

#### The GNS File

Location for the following file is `arjuna-samples/arjex/guiauto/namespace/BasicIdentification.yaml`

```YAML
labels:

  user_id:
    id: user_login

  user_name:
    name: log

  user_tag:
    tag: input

  user_class:
    classes: input

  lost_pass_link:
    link: password

  lost_pass_flink:
    flink: "Lost your password?"
```

#### Usage in code

```python
# arjuna-samples/arjex/test/module/web_ui_basics/check_02_locators_basic.py

@test
def check_basic_identifiers(request, wordpress):
    # user name field.
    # Html of user name: <input type="text" name="log" id="user_login" class="input" value="" size="20">
    element = wordpress.gns.user_id
    element = wordpress.gns.user_name
    element = wordpress.gns.user_tag
    element = wordpress.gns.user_class

    # Lost your password link
    # Html of link: <a href="/wp-login.php?action=lostpassword" title="Password Lost and Found">Lost your password?</a>
    # Partial Link text match
    element = wordpress.gns.lost_pass_link
    # Full Link text match
    element = wordpress.gns.lost_pass_flink
```

##### Points to Note
1. You can directly create an element by using `<app object>.gns.<GNS label>` syntax. For example, `wordpress.gns.user_id` will find an element with the locator information supplied in GNS file for the label `user_id`.
2. The locator strategy is expressed using locator type names supported by Arjuna. These are simple locators and hence are expressed as basic key value pairs, almost equivalent to the way you pass them as keyword arguments in `app.element` calls. Functionality is equivalent as well.

### Gui Namespace - Externalizing XPath

**`xpath`** locator can be externalized as well.

#### Test Fixture for Example(s) in This Page

Below is the `@for_test` fixture code:

```python
# arjuna-samples/arjex/test/module/check_03_locators_xpath.py

@for_test
def wordpress(request):
    # Setup
    wp_url = C("wp.login.url")
    wordpress = WebApp(base_url=wp_url, label="XPath")
    wordpress.launch()
    
    yield wordpress
    
    # Teadown    
    wordpress.quit()
```

##### Points to Note
1. Label is changed to `XPath`.
2. Rest of the code is same as earlier.

### The GNS File

Location for the following file is `arjuna-samples/arjex_app/guiauto/namespace/XPath.yaml`

```YAML
labels:

  lost_pass_text:
    xpath: "//*[text() = 'Lost your password?']"

  lost_pass_text_content:
    xpath: "//*[contains(text(), 'Lost')]"

  lost_pass_title:
    xpath: "//*[@title = 'Password Lost and Found']"

  user_value:
    xpath: "//*[@value = 'Log In']"

  user_attr:
    xpath: "//*[@for = 'user_login']"

  user_attr_content:
    xpath: "//*[contains(@for, '_login')]"

  pass_type:
    xpath: "//*[@type ='password']"
```


### Usage

```python
# arjuna-samples/arjex/test/module/check_03_locators_xpath.py

@test
def check_xpath(request, wordpress):

    # Based on Text
    element = wordpress.gns.lost_pass_text

    # Based on partial text
    element = wordpress.gns.lost_pass_text_content

    # Based on Title
    element = wordpress.gns.lost_pass_title

    # Based on Value
    element = wordpress.gns.user_value

    # Based on any attribute e.g. for
    element = wordpress.gns.user_attr

    # Based on partial content of an attribute
    element = wordpress.gns.user_attr_content

    # Based on element type
    element = wordpress.gns.pass_type
```

### Gui Namespace - Externalizing CSS Selectors

**`selector`** locator can be externalized as well.

#### Test Fixture for Example(s) in This Page

Below is the `@for_test` fixture code:

```python
# arjuna-samples/arjex/test/module/check_04_locators_css_selectors.py

@for_test
def wordpress(request):
    # Setup
    wp_url = C("wp.login.url")
    wordpress = WebApp(base_url=wp_url, label="Selector")
    wordpress.launch()
    
    yield wordpress
    
    # Teadown    
    wordpress.quit()
```

##### Points to Note
1. Label is changed to `Selector`.
2. Rest of the code is same as earlier.

### The GNS File

Location for the following file is `arjuna-samples/arjex_app/guiauto/namespace/Selector.yaml`

```YAML
labels:

  user_attr:
    selector: "*[for = 'user_login']"

  user_attr_content:
    selector: "*[for *= '_login']"

  pass_type:
    selector: "*[type ='password']"

  button_compound_class:
    selector: ".button.button-large"
```

### Usage

```python
# arjuna-samples/arjex/test/module/check_04_locators_css_selectors.py

@test
def check_selector(request, wordpress):

    # Based on any attribute e.g. for
    element = wordpress.gns.user_attr

    # Based on partial content of an attribute
    element = wordpress.gns.user_attr_content

    # Based on element type
    element = wordpress.gns.pass_type

    # Based on compound classes
    element = wordpress.gns.button_compound_class
```

### Gui Namespace - Externalizing Arjuna's Locator Extensions

All of Arjuna's locator extensions can be externalizd in GNS as well.

- Following are externalized as simple key value pairs:
    - **`text`**
    - **`ftext`**
    - **`title`**
    - **`value`**
    - **`js`**
- Following are externlized with content as a YAML mapping with `name` and `value` keys:
    - **`attr`**
    - **`fattr`**
- **`classes`** is externalized as a single string or a YAML list of strings:
- **`point`** is externlized with content as a YAML mapping with `x` and `y` keys.

#### Test Fixture for Example(s) in This Page

Below is the `@for_test` fixture code:

```python
# arjuna-samples/arjex/test/module/check_05_locators_arjuna_exts.py

@for_test
def wordpress(request):
    # Setup
    wp_url = C("wp.login.url")
    wordpress = WebApp(base_url=wp_url, label="ArjunaExtended")
    wordpress.launch()
    yield wordpress

    # Teadown
    wordpress.quit()
```

##### Points to Note
1. Label is changed to `ArjunaExtended`.
2. Rest of the code is same as earlier.

### The GNS File

Location for the following file is `arjuna-samples/arjex_app/guiauto/namespace/ArjunaExtended.yaml`

```YAML
labels:

  lost_pass_text:
    text: Lost

  lost_pass_ftext:
    ftext: "Lost your password?"

  lost_pass_title:
    title: Password Lost and Found

  user_value:
    value: Log In

  user_attr:
    attr:
      name: for
      value: _login

  user_fattr:
    fattr:
      name: for
      value: user_login

  pass_type:
    type: password

  button_classes_str:
    classes: button button-large

  button_classes_list:
    classes: 
      - button 
      - button-large

  elem_xy:
    point:
      x: 1043
      y: 458

  elem_js:
    js: "return document.getElementById('wp-submit')"
```

### Usage

```python
# arjuna-samples/arjex/test/module/check_05_locators_arjuna_exts.py

@test
def check_arjuna_exts(request, wordpress):

    # Based on partial text
    element = wordpress.gns.lost_pass_text

    # Based on Full Text
    element = wordpress.gns.lost_pass_ftext

    # Based on Title
    element = wordpress.gns.lost_pass_title

    # Based on Value
    element = wordpress.gns.user_value

    # Based on partial match of content of an attribute
    element = wordpress.gns.user_attr

    # Based on full match of an attribute
    element = wordpress.gns.user_fattr

    # Based on element type
    element = wordpress.gns.pass_type

    # Based on compound classes
    element = wordpress.gns.button_classes_str
    element = wordpress.gns.button_classes_list

    # Based on Point (location in terms of X,Y co-ordinates)
    element = wordpress.gns.elem_xy

    # With Javascript
    element = wordpress.gns.elem_js
```

### Element Templates

### Matching Multiple Elements as GuiMultiElement

Arjuna provides a special abstraction for representing mutliple ```GuiElement```s together rather than a raw Python list. This provides an opportunity to include higher level methods for test code authors.

#### Test Fixture for Examples in This Page

We are going to use a test-level fixture for the examples.

Below is the `@for_test` fixture code to get logged-in WordPress for a test using the reusable module that we created in the last section. We place it in the `project.lib.fixture.test` module so that it can be used for a any test. 

```python
# arjuna-samples/arjex/lib/fixture/test.py

from arjuna import *
from arjex.lib.app_procedural.wp import WordPress

@for_test
def logged_in_wordpress(request):
    # Setup
    wordpress = create_wordpress_app()
    login(wordpress)
    yield wordpress

    # Teadown
    logout(wordpress)
```

#### Important point for GNS

The following entry in `WordPress.yaml` is of interest:

```YAML
  cat_checkboxes:
    template: multi_element
    name: "delete_tags[]"
```

##### Points to Note
1. To instruct Arjuna to treat an element as a multiple element, under the label entry in GNS file, you can mention `template: multi_element`.

#### Test Code

```python
# arjuna-samples/arjex/test/module/check_09_gui_multielement.py

from arjuna import *

@test
def check_multielement(request, logged_in_wordpress):
    wordpress = logged_in_wordpress
    wordpress.gns.posts.click()
    wordpress.gns.categories.click()

    check_boxes = wordpress.gns.cat_checkboxes
    check_boxes[1].check()
    check_boxes[1].uncheck()
    check_boxes.first_element.uncheck()
    check_boxes.last_element.uncheck()
    check_boxes.random_element.uncheck()
```

##### Points to Note
1. The creation code is same as that for a single element.
3. `GuiMultiElement` supports index based retrieval just like a regular list. Indexes start from computer counting (0).
4. In addition to this, it provides methods like `first_element`, `last_element` and `random_element`.
5. It provides more features that we will cover in advanced section of this tutorial. It also forms the basis of Arjuna's DropDown and RadioGroup abstractions which we cover in next sections.


### Arjuna's DropDown Abstraction - Handling Default HTML Select

DropDown object in Arjuna represents the Select-style control in the UI. Here, we cover handling of a default-HTML select control which has `<select>` as the root tag and `option` as the tag for an option.

#### Test Fixture for Examples in This Page

We are going to use `logged_in_wordpress` test fixture from the GuiMultiElement example.

#### Important point for GNS

The following entry in `WordPress.yaml` is of interest:

```YAML
  role:
    template: dropdown
    id: default_role
```

##### Points to Note
1. To instruct Arjuna to treat an element as a `Dropdown`, under the label entry in GNS file, you can mention `template: dropdown`.

#### Usage

```python
# arjuna-samples/arjex/test/module/check_10_dropdown.py

from arjuna import *

@test
def check_dropdown(request, logged_in_wordpress):
    wordpress = logged_in_wordpress
    wordpress.gns.settings.click()

    role_select = wordpress.gns.role

    role_select.select_text("Subscriber")
    fmsg = "Failed to select Subscriber Role"
    request.asserter.assert_true(role_select.has_visible_text_selected("Subscriber"), fmsg)
    request.asserter.assert_true(role_select.has_value_selected("subscriber"), fmsg)
    request.asserter.assert_true(role_select.has_index_selected(0), fmsg)
    request.asserter.assert_equal(role_select.value, "subscriber", "Unexpected Value attribute of Role.")
    request.asserter.assert_equal(role_select.text,"Subscriber",  "Unexpected Selected Role Text ")

    role_select.select_value("editor")
    role_select.select_index(4)
    role_select.text = "Subscriber"
```

#### Points to Note
1. Creation is same as a Gui Element.
2. We can select an option by its visible text by calling `select_text` method of DropDown.
3. DropDown provides various enquiry methods - `has_visible_text_selected`, `has_value_selected`, has_index_selected`.
4. DropDown also has enquirable properties - `value` and `text`.
5. We assert using `request.asserter`'s appropriate assertion methods.
6. There are other ways of selection as well - `select_value` to select by value attribute of an option, `select_index` to select an option present at provided index.
7. DropDown also has a way of selecting an option by setting its `text` property. This is similar to `.text` property setting of a text-box. It is different from `select_text` method in terms of implementation. `select_text` uses DOM inquiry to match the text of an option and then clicks it to select it. Setting the `.text` property similuates the user action where the user types a string in a focused/highlighted select control to select an option (in technical terms it is equivalent of sendkeys).

### Arjuna's RadioGroup Abstraction - Handling Default HTML Radio Group

RadioGroup object in Arjuna represents the Radio Buttons in the UI that belong to a single selection group (have the same name). Here, we cover handling of a default-HTML RadioGroup control which represents multiple `<input type='radio'>` elements which have the same `name` attribute value.


#### Test Fixture for Examples in This Page

We are going to use `logged_in_wordpress` test fixture from the GuiMultiElement example.

#### Important point for GNS

The following entry in `WordPress.yaml` is of interest:

```YAML
  date_format:
    template: radio_group
    name: date_format
```

##### Points to Note
1. To instruct Arjuna to treat an element as a `RadioGroup`, under the label entry in GNS file, you can mention `template: radio_group`.

#### Usage

```python
# arjuna-samples/arjex/test/module/check_11_radio_group.py

from arjuna import *
from arjex.lib.app_procedural.wp import *

@test
def check_radiogroup(request, logged_in_wordpress):
    wordpress = logged_in_wordpress
    wordpress.gns.settings.click()

    date_format = wordpress.gns.date_format

    fmsg = "Failed to select m/d/Y date format"
    request.asserter.assert_true(date_format.has_value_selected("m/d/Y"), fmsg)
    request.asserter.assert_true(date_format.has_index_selected(2), fmsg)
    request.asserter.assert_equal(date_format.value, "m/d/Y", "Unpexpected Value attribute of Date Format")

    date_format.select_value(r"\c\u\s\t\o\m")
    date_format.select_index(2)
```

#### Points to Note
1. Creation is same as a Gui Element.
2. We can select a a by its visible text by calling `select_text` method of DropDown.
3. DropDown provides various enquiry methods - `has_value_selected`, `has_index_selected`.
4. DropDown also has `value` enquirable property.
5. We assert using `request.asserter`'s appropriate assertion methods.
6. You can use two ways of selecting a radio button - `select_value` to select by value attribute of an option, `select_index` to select a radio button present at provided index.



### Gui Abstraction using `WebApp`, `Page` and `Section` classes


### Arjuna's Gui Loading Model


### Helper Classes, Functions and Enums


### Arjuna Exceptions




