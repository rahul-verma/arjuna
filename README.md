# Arjuna

Arjuna is a Python based test automation framework developed by Rahul Verma (www.rahulverma.net). Rahul has implemented smaller variants of features in Arjuna across frameworks and organizations, or given advise around it. However Arjuna being a generic library has the most complete implementation of his ideas, away from project specific contexts and constraints.

Arjuna uses **[pytest](https://docs.pytest.org/en/latest/)** as its recommended test engine. Arjuna also provides its markup for some common use cases on top of pytest. If you like, you can make use of Arjuna with any other test engine or custom frameworks as well.

You'd need Python 3.5+ to make use of Arjuna.

Note: On Linux, the built-in Python3 build has issues with the Python's built-in enum module which is heavily used in Arjuna. One alternative is to install ActiveState Python on linux. Advanced users can go for installing a custom Python build.

## Arjuna Installation

1. Download and install latest Python (3.5+) from https://python.org
    * If you are insterested to learn python Following are links for tutorials and docs.
    + https://docs.python.org/3.7/tutorial/index.html
    + https://docs.python.org/3.7/index.html
2. Confirm the python version installed by running the command `python --version`. If expected version in not shown, fix this by looking into PATH variables and/or to see whether you have multiple versions of Python installed.
3. Install Arjuna using the following command
    * `pip install arjuna`

You can find the example code in [arjex project](https://github.com/rahul-verma/arjuna/tree/master/arjuna-samples/arjex).

## Features
1. Arjuna provides the concept of a test project with a fixed project structure, which gives consistency across implementations as well many re-usable features.
2. Arjuna provides a comprehensive and intuitive Command Line Interface.
3. You can easily define a test as a test function.
4. You can take care of setup and cleanup before and after tests as test fixtures 3 levels - test, module and session. These test fixtures can be coded centrally so that they become available to all tests.
5. Arjuna provides very comprehensive and advanced features for Test Configuration.
    - You can define a project level configuration.
    - You can create any number of custom configurations programmatically.
    - In addition to Arjuna's built-in options, you can define your own user options.
    - You can define any number of configuration files to load configuration options from.
    - Arjuna provides the the magic `C` function with a Configuration query format to easily retrieve configuration values.
    - You can define environment configuration files and easily specify an active test environment.
    - You can create a configuration file and super-impose its options on central configuration.
    - You can use configuration queries in Gui Namespace files to create dynamic identifiers.
6. You can do data driven testing with a multitude of easy to use and powerful constructs to create data sources in Arjuna:
    - Driving with single or multiple data recors
    - Driving with Static Data Functions/Generators and Dynamic Data Functions/Generators.
    - Driving with Static Data Classes and Dynamic Data Classes
    - Driving with Data Files (Excel/Delimiter-Separated Files/INI)
    - Filtering Data Records
    - Driving by combinig multiple data sources 
7. You can create Contextual Data References to pull data based on a context string.
    - Currently Excel format is supported.
    - Arjuna provides the the magic `R` function with a data reference query format to easily retrieve data reference values anywhere.
    - You can use data reference queries in Gui Namespace files to create dynamic identifiers.
8. You can easily localize your strings anywhere in your test project.
    - Excel localizer
    - Json localizer
    - Arjuna provides the the magic `L` function with a localization query format to easily retrieve localized strings anywhere.
    - Localization can strict or non-strict.
    - You can use localization queries in Gui Namespace files to create dynamic identifiers.
9. Arjuna has comprehenstive support for Web Gui Automation.
    - Arjuna provides highly customized automation on top of Selenium WebDriver for web automation.
    - Arjuna automatically downloads drivers using WebDriver Manager. Currenlty only **Chrome** and **Firefox** are the supported browsers (in normal as well as headless mode).
    - The starting point for web automation in Arjuna is the `WebApp` class.
    - Arjuna supports various features for element identification:
        - A single element is represented as an `element`. It provides very intuitive and Pythonic interaction methods.
        - You can locate elements using ID, Name, Tag, Class, Link Text and Partial Link Text. Locating with XPath and CSS Selectors is supported as well. These are mostly direct wrappers on what Selenium supports.
        - Arjuna provides its own advanced locator extensions for simple and powerful identifiers.
        - You can find nested elements i.e. an element within an element.
        - You can define dynamic identifiers i.e. identifiers which contain Arjuna format strings which are replaced with their values at run-time. The Arjuna format strings can be simple names or Configuration queries or Data Reference Queries or Localization queries.
    - Gui Namespace (GNS) is used to externalize element locators.
        - You can externalize ID, Name, Tag, Class, Link Text and Partial Link Text, XPath and CSS Selectors.
        - You can also externalize Arjuna's locators extensions.
        - You can define dynamic identifiers i.e. identifiers which contain Arjuna format strings which are replaced with their values at run-time. The Arjuna format strings can be simple names or Configuration queries or Data Reference Queries or Localization queries.
        - You can define your own locators. You define them globally or within a GNS file.
    - Various higher-level element templates are available. These can directly coded in your test or can be defined in a Gui Namespace.
        - `multi_element` represents multiple `elements`s together.
        - `dropdown` represents an HTML drop-down list.
        - `radio_group` represents an HTML radio group.
    - Arjuna provides various classes so that you can build various types of Gui Abstractions.
        - `WebApp` represents the complete web application. You can create an object of it or inherit from it to add methods and attributes as needed. A `WebApp` can be used with or without externalized identifiers or both (partial externalization).
        - `Page` class represents a web page and is associated with a `WebApp`. 
        - `Section` (with aliases `Widget` or `Dialog`) represents part of a web page or a dialog. It can be associated with a `WebApp` or a `Page`.
        - Arjuna has a comprehensive Gui loading protocol.
        - `Page` and `Section` can have an `anchor` element defined in corresponding Gui Namespace. 
        - `Section` can have a `root` element defined in corresponding Gui Namespace.
10. Arjuna provides various helper classes, functions and enums to aid in test automation:
    - `XmlNode` and `NodeLocator` for XML parsing.
    - `Formatter` and `Locator` to define locators.
11. Arjuna Exceptions
    - TBD


## Arjex - The Arjuna Examples Project
The `arjex` project contains lots and lots of example code for using Arjuna features. Following is the list of test-packages and what examples they contain:
    - TBD

### 10. Gui Abstraction - GNS, App, Page, Widget and Gui Elements

1. [Thinking Procedurally -Creating Reusable Module](https://github.com/rahul-verma/arjuna/blob/master/docs/webui_basics/ThinkingProcedurally.md)
2. [Creating App Class](https://github.com/rahul-verma/arjuna/blob/master/docs/gui_abstraction/AppClass.md)
3. [App Object Model](https://github.com/rahul-verma/arjuna/blob/master/docs/gui_abstraction/AppObjectModel.md)
4. [App-Page Object Model](https://github.com/rahul-verma/arjuna/blob/master/docs/gui_abstraction/AppPageObjectModel.md)
5. [App-Page-Section Object Model](https://github.com/rahul-verma/arjuna/blob/master/docs/gui_abstraction/AppPageSectionObjectModel.md)
6. [Gui and Its Loading Model in Arjuna](https://github.com/rahul-verma/arjuna/blob/master/docs/gui_abstraction/GuiLoadingModel.md)

## Reference
1. Command Line Options

### Miscellaneous
1. Using Arjuna With Your Test Framework
