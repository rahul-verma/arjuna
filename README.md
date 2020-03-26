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
1. Arjuna provides the concept of a [test project with a fixed project structure](https://github.com/rahul-verma/arjuna/blob/master/docs/ArjunaFeaturesDoc.md#arjuna-test-project), which gives consistency across implementations as well many re-usable features.
2. Arjuna provides a comprehensive and intuitive [Command Line Interface](https://github.com/rahul-verma/arjuna/blob/master/docs/ArjunaFeaturesDoc.md#arjuna-command-line-interface).
3. You can easily define a [test as a test function](https://github.com/rahul-verma/arjuna/blob/master/docs/ArjunaFeaturesDoc.md#defining-a-test-function).
4. You can take care of setup and cleanup before and after tests as [test fixtures 3 levels - test, module and session](https://github.com/rahul-verma/arjuna/blob/master/docs/ArjunaFeaturesDoc.md#defining-test-fixtures). These test fixtures can be coded centrally so that they become available to all tests.
5. Arjuna provides very comprehensive and advanced features for [Test Configuration](https://github.com/rahul-verma/arjuna/blob/master/docs/ArjunaFeaturesDoc.md#understanding-configuration-system-of-arjuna).
    - You can define a [project level configuration](https://github.com/rahul-verma/arjuna/blob/master/docs/ArjunaFeaturesDoc.md#projectconf---setting-project-level-configuration-options).
    - You can create any number of [custom configurations programmatically](https://github.com/rahul-verma/arjuna/blob/master/docs/ArjunaFeaturesDoc.md#configuration-builder---creating-custom-configurations).
    - In addition to Arjuna's built-in options, you can [define your own user options](https://github.com/rahul-verma/arjuna/blob/master/docs/ArjunaFeaturesDoc.md#defining-and-handling-user-options).
    - You can define any number of [configuration files to load configuration options](https://github.com/rahul-verma/arjuna/blob/master/docs/ArjunaFeaturesDoc.md#configuration-builder---adding-options-from-a-conf-file) from.
    - Arjuna provides [the magic `C` function](https://github.com/rahul-verma/arjuna/blob/master/docs/ArjunaFeaturesDoc.md#the-magic-c-function) with a Configuration query format to easily retrieve configuration values.
    - You can [define environment configurations](https://github.com/rahul-verma/arjuna/blob/master/docs/ArjunaFeaturesDoc.md#environment-configurations) and easily specify an active test environment.
    - You can [create a Run Configuration file and super-impose its options on central configuration](https://github.com/rahul-verma/arjuna/blob/master/docs/ArjunaFeaturesDoc.md#run-configuration--overriding-configuration-with-a-configuration-file-for-a-test-run).
    - You can use configuration queries in Gui Namespace files to create dynamic identifiers.
6. You can do [data driven testing](https://github.com/rahul-verma/arjuna/blob/master/docs/ArjunaFeaturesDoc.md#data-driven-testing) with a multitude of easy to use and powerful constructs to create data sources in Arjuna:
    - Driving with [single data record](https://github.com/rahul-verma/arjuna/blob/master/docs/ArjunaFeaturesDoc.md#single-data-record) or [multiple data records](https://github.com/rahul-verma/arjuna/blob/master/docs/ArjunaFeaturesDoc.md#multiple-data-records)
    - Driving with [Static Data Functions](https://github.com/rahul-verma/arjuna/blob/master/docs/ArjunaFeaturesDoc.md#driving-with-static-data-function)/[Generators](https://github.com/rahul-verma/arjuna/blob/master/docs/ArjunaFeaturesDoc.md#driving-with-static-data-generator) and [Dynamic Data Functions/Generators](https://github.com/rahul-verma/arjuna/blob/master/docs/ArjunaFeaturesDoc.md#driving-with-dynamic-data-function-or-generator).
    - Driving with [Static Data Classes](https://github.com/rahul-verma/arjuna/blob/master/docs/ArjunaFeaturesDoc.md#driving-with-static-data-classes) and [Dynamic Data Classes](https://github.com/rahul-verma/arjuna/blob/master/docs/ArjunaFeaturesDoc.md#driving-with-dynamic-data-classes)
    - [Driving with Data Files](https://github.com/rahul-verma/arjuna/blob/master/docs/ArjunaFeaturesDoc.md#driving-with-data-files) ([Excel Files](https://github.com/rahul-verma/arjuna/blob/master/docs/ArjunaFeaturesDoc.md#driving-with-excel-file)/[Delimiter-Separated Files](https://github.com/rahul-verma/arjuna/blob/master/docs/ArjunaFeaturesDoc.md#driving-with-delimiter-separated-file)/[INI Files](https://github.com/rahul-verma/arjuna/blob/master/docs/ArjunaFeaturesDoc.md#driving-with-ini-file))
    - [Filtering Data Records](https://github.com/rahul-verma/arjuna/blob/master/docs/ArjunaFeaturesDoc.md#driving-with-ini-file#data-files-with-exclude-filter-for-records)
    - Driving by [combinig multiple data sources](https://github.com/rahul-verma/arjuna/blob/master/docs/ArjunaFeaturesDoc.md#driving-with-multiple-data-sources)
7. You can create [Contextual Data References](https://github.com/rahul-verma/arjuna/blob/master/docs/ArjunaFeaturesDoc.md#contextual-data-references) to pull data based on a context string.
    - Currently [Excel format](https://github.com/rahul-verma/arjuna/blob/master/docs/ArjunaFeaturesDoc.md#excel-data-references) is supported.
    - Arjuna provides [the magic `R` function](https://github.com/rahul-verma/arjuna/blob/master/docs/ArjunaFeaturesDoc.md#the-magic-r-function) with a data reference query format to easily retrieve data reference values anywhere.
    - You can use data reference queries in Gui Namespace files to create dynamic identifiers.
8. You can easily [localize your strings](https://github.com/rahul-verma/arjuna/blob/master/docs/ArjunaFeaturesDoc.md#localizing-strings) anywhere in your test project.
    - [Excel localizer](https://github.com/rahul-verma/arjuna/blob/master/docs/ArjunaFeaturesDoc.md#excel-based-localization)
    - [Json localizer](https://github.com/rahul-verma/arjuna/blob/master/docs/ArjunaFeaturesDoc.md#json-based-localization)
    - Arjuna provides [the magic `L` function](https://github.com/rahul-verma/arjuna/blob/master/docs/ArjunaFeaturesDoc.md#the-l-function-for-localization) with a localization query format to easily retrieve localized strings anywhere.
    - Localization can [strict or non-strict](https://github.com/rahul-verma/arjuna/blob/master/docs/ArjunaFeaturesDoc.md#strict-vs-non-strict-mode-for-localization).
    - You can use localization queries in Gui Namespace files to create dynamic identifiers.
9. Arjuna has comprehenstive support for **Web Gui Automation**.
    - Arjuna provides highly customized automation on top of Selenium WebDriver for web automation.
    - Arjuna automatically downloads drivers using WebDriver Manager. Currenlty only **Chrome** and **Firefox** are the supported browsers (in normal as well as headless mode).
    - The starting point for web automation in Arjuna is [the `GuiApp` class](https://github.com/rahul-verma/arjuna/blob/master/docs/ArjunaFeaturesDoc.md#the-webapp-class).
    - Arjuna supports various features for element identification and interaction:
        - A single element is represented as a [`GuiElement`](https://github.com/rahul-verma/arjuna/blob/master/docs/ArjunaFeaturesDoc.md#guielement-and-the-element-template). It provides very [intuitive and Pythonic interaction methods](https://github.com/rahul-verma/arjuna/blob/master/docs/ArjunaFeaturesDoc.md#interaction-with-guielement).
        - You can [locate elements using ID, Name, Tag, Class, Link Text and Partial Link Text, XPath and CSS Selectors](https://github.com/rahul-verma/arjuna/blob/master/docs/ArjunaFeaturesDoc.md#locators---using-id--name--tag--class--link-text--partial-link-text--xpath-and-css-selectors). These are mostly direct wrappers on what Selenium supports.
        - Arjuna provides its own [advanced locator extensions for simple and powerful identifiers](https://github.com/rahul-verma/arjuna/blob/master/docs/ArjunaFeaturesDoc.md#locators---arjunas-locator-extensions).
        - Arjuna [automatically does a dynamic wait during locating elements as well as some basic interactions](https://github.com/rahul-verma/arjuna/blob/master/docs/ArjunaFeaturesDoc.md#automatic-dynamic-waiting).
        - You can find nested elements i.e. an element within an element.
        - You can define dynamic identifiers i.e. identifiers which contain Arjuna format strings which are replaced with their values at run-time. The Arjuna format strings can be simple names or Configuration queries or Data Reference Queries or Localization queries.
    - [Gui Namespace (GNS)](https://github.com/rahul-verma/arjuna/blob/master/docs/ArjunaFeaturesDoc.md#gui-namespace---externalizing-locators) is used to externalize element locators in a [GNS File](https://github.com/rahul-verma/arjuna/blob/master/docs/ArjunaFeaturesDoc.md#the-gns-file) which can be [associated with a `GuiApp`](https://github.com/rahul-verma/arjuna/blob/master/docs/ArjunaFeaturesDoc.md#associating-gns-file-with-webapp)
        - You can [externalize ID, Name, Tag, Class, Link Text and Partial Link Text, XPath and CSS Selectors](https://github.com/rahul-verma/arjuna/blob/master/docs/ArjunaFeaturesDoc.md#externalizing-id--name--tag--class--link-text--partial-link-text--xpath-and-css-selector).
        - You can also [externalize Arjuna's locators extensions](https://github.com/rahul-verma/arjuna/blob/master/docs/ArjunaFeaturesDoc.md#externalizing-arjunas-locator-extensions).
        - You can define dynamic identifiers i.e. identifiers which contain Arjuna format strings which are replaced with their values at run-time. The Arjuna format strings can be simple names or Configuration queries or Data Reference Queries or Localization queries.
        - You can define your own locators. You define them globally or within a GNS file.
    - Various higher-level [element templates](https://github.com/rahul-verma/arjuna/blob/master/docs/ArjunaFeaturesDoc.md#element-templates) are available. These can directly coded in your test or can be defined in a Gui Namespace.
        - [`GuiMultiElement`](https://github.com/rahul-verma/arjuna/blob/master/docs/ArjunaFeaturesDoc.md#guimultielement---handling-multiple-guielements-together) represents multiple `GuiElement`s together. Can be [defined in code](https://github.com/rahul-verma/arjuna/blob/master/docs/ArjunaFeaturesDoc.md#defining-and-using-a-guimultielement-in-code) as well [defined in GNS](https://github.com/rahul-verma/arjuna/blob/master/docs/ArjunaFeaturesDoc.md#defining-guimultielement-in-gns-and-using-it-in-code).
        - [`DropDown`](https://github.com/rahul-verma/arjuna/blob/master/docs/ArjunaFeaturesDoc.md#dropdown---handling-default-html-select) represents an HTML drop-down list. Can be [defined in code](https://github.com/rahul-verma/arjuna/blob/master/docs/ArjunaFeaturesDoc.md#defining-and-using-a-dropdown-in-code) as well [defined in GNS](https://github.com/rahul-verma/arjuna/blob/master/docs/ArjunaFeaturesDoc.md#defining-dropdown-in-gns-and-using-it-in-code)
        - [`RadioGroup`](https://github.com/rahul-verma/arjuna/blob/master/docs/ArjunaFeaturesDoc.md#radiogroup---handling-default-html-radio-group) represents an HTML radio group. Can be [defined in code](https://github.com/rahul-verma/arjuna/blob/master/docs/ArjunaFeaturesDoc.md#defining-and-using-a-radiogroup-in-code) as well [defined in GNS](https://github.com/rahul-verma/arjuna/blob/master/docs/ArjunaFeaturesDoc.md#defining-radiogroup-in-gns-and-using-it-in-code)
    - Arjuna provides various classes so that you can build various types of **Gui Abstractions**.
        - [`Gui`](https://github.com/rahul-verma/arjuna/blob/master/docs/ArjunaFeaturesDoc.md#concept-of-gui-in-arjuna) is a generic abstraction of a Graphical User Interface.
        - [`GuiApp`](https://github.com/rahul-verma/arjuna/blob/master/docs/ArjunaFeaturesDoc.md#the-guiapp-class) represents the complete web application. You can create an object of it or inherit from it to add methods and attributes as needed. A `GuiApp` can be used with or without externalized identifiers or both (partial externalization).
        - [`GuiPage`](https://github.com/rahul-verma/arjuna/blob/master/docs/ArjunaFeaturesDoc.md#the-guipage-class) class represents a web page and is associated with a `GuiApp`. 
        - [`GuiSection`](https://github.com/rahul-verma/arjuna/blob/master/docs/ArjunaFeaturesDoc.md#the-guisection-class) (with aliases `GuiWidget` or `GuiDialog`) represents part of a web page or a dialog. It can be associated with a `GuiApp` or a `GuiPage`.
        - With Arjuna you can create various [Gui abstraction models](https://github.com/rahul-verma/arjuna/blob/master/docs/ArjunaFeaturesDoc.md#gui-abstraction-models), for example:
            - [The App Model](https://github.com/rahul-verma/arjuna/blob/master/docs/ArjunaFeaturesDoc.md#app-model-using-app-class)
            - [The App-Page Model](https://github.com/rahul-verma/arjuna/blob/master/docs/ArjunaFeaturesDoc.md#app-page-model-using-guiapp-and-guipage-classes)
            - [The App-Page-Section Model](https://github.com/rahul-verma/arjuna/blob/master/docs/ArjunaFeaturesDoc.md#app-page-section-model-using-guiapp--guipage-and-guisection-classes)
        - Arjuna has a comprehensive [Gui loading protocol](https://github.com/rahul-verma/arjuna/blob/master/docs/ArjunaFeaturesDoc.md#arjunas-gui-loading-model).
        - `GuiPage` and `GuiSection` can have an `anchor` element defined in corresponding Gui Namespace. 
        - `GuiSection` can have a `root` element defined in corresponding Gui Namespace.
10. Arjuna provides various helper classes, functions and enums to aid in test automation:
    - `XmlNode` and `NodeLocator` for XML parsing.
    - `Formatter` and `Locator` to define locators.
11. Various custom [Arjuna Exceptions](https://github.com/rahul-verma/arjuna/blob/master/docs/ArjunaFeaturesDoc.md#arjuna-exceptions) are implemented to give you precise information about the issues that take place.

## Arjex - The Arjuna Examples Project
The `arjex` project contains lots and lots of example code for using Arjuna features.