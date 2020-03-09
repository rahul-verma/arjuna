# Arjuna

Arjuna is a Python based test automation framework developed by Rahul Verma (www.rahulverma.net). Rahul has implemented smaller variants of features in Arjuna across frameworks and organizations, or given advise around it. However Arjuna being a generic library has the most complete implementation of his ideas, away from project specific contexts and constraints.

Arjuna uses **[pytest](https://docs.pytest.org/en/latest/)** as its recommended test engine. Arjuna also provides its markup for some common use cases on top of pytest. If you like, you can make use of Arjuna with any other test engine or custom frameworks as well.

You'd need Python 3.5+ to make use of Arjuna.

Note: On Linux, the built-in Python3 build has issues with the Python's built-in enum module which is heavily used in Arjuna. One alternative is to install ActiveState Python on linux. Advanced users can go for installing a custom Python build.

## Tutorial

### 1. Arjuna Installation

1. Download and install latest Python (3.5+) from https://python.org
    * If you are insterested to learn python Following are links for tutorials and docs.
    + https://docs.python.org/3.7/tutorial/index.html
    + https://docs.python.org/3.7/index.html
2. Confirm the python version installed by running the command `python --version`. If expected version in not shown, fix this by looking into PATH variables and/or to see whether you have multiple versions of Python installed.
3. Install Arjuna using the following command
    * `pip install arjuna`

### 2. Arjuna - Getting Started

You can find the example code used on this section in [arjuna_start project](https://github.com/rahul-verma/arjuna/tree/master/arjuna-samples/arjex_start/test/module).

1. [Project Structure](https://github.com/rahul-verma/arjuna/blob/master/docs/start/ProjectStructure.md)
2. [Writing Your First Test](https://github.com/rahul-verma/arjuna/blob/master/docs/start/WritingFirstTest.md)

### 3. Arjuna's Configuration System

You can find the example code used on this section in [arjuna_config project](https://github.com/rahul-verma/arjuna/tree/master/arjuna-samples/arjex_config/test/module).

1. [Configuration](https://github.com/rahul-verma/arjuna/blob/master/docs/config/Configuration.md)
2. [project.conf - Project Level Configuration](https://github.com/rahul-verma/arjuna/blob/master/docs/config/ProjectConf.md)
3. [Configuration Builder - Creating Custom Configurations](https://github.com/rahul-verma/arjuna/blob/master/docs/config/ConfigBuilder.md)
4. [Defining and Handling User Options](https://github.com/rahul-verma/arjuna/blob/master/docs/config/UserOptions.md)
5. [Using .conf files with Configuration Builder](https://github.com/rahul-verma/arjuna/blob/master/docs/config/UsingFilesInConfigBuilder.md)
6. [The `C` Magic Function](https://github.com/rahul-verma/arjuna/blob/master/docs/config/TheCMagicFunction.md)
7. [Environments and Dynamic Configurations](https://github.com/rahul-verma/arjuna/blob/master/docs/config/EnvironmentsAndDynamicConfigurations.md)


### 4. Data Driven Testing and Contextual Data References

You can find the example code used on this section in [arjuna_data project](https://github.com/rahul-verma/arjuna/tree/master/arjuna-samples/arjex_data/test/module).

1. [Data Driven Testing](https://github.com/rahul-verma/arjuna/blob/master/docs/data/DataDrivenTesting.md)
2. [Driving with Single or Multiple Data Records](https://github.com/rahul-verma/arjuna/blob/master/docs/data/DataRecords.md)
3. [Driving with Data Functions](https://github.com/rahul-verma/arjuna/blob/master/docs/data/DataFunctions.md)
4. [Driving with Data Classes](https://github.com/rahul-verma/arjuna/blob/master/docs/data/DataClasses.md)
5. [Driving with Data Files](https://github.com/rahul-verma/arjuna/blob/master/docs/data/DataFiles.md)
6. [Driving with Multiple Data Sources](https://github.com/rahul-verma/arjuna/blob/master/docs/data/MultipleDataSources.md)
7. [Contextual Data References and the Magic `R` Function](https://github.com/rahul-verma/arjuna/blob/master/docs/data/ContextualDataReferences.md)
8. [Excel Data References](https://github.com/rahul-verma/arjuna/blob/master/docs/data/ExcelDataReferences.md)

### 5. Localization of Strings
You can find the example code used on this section in [arjuna_l10 project](https://github.com/rahul-verma/arjuna/tree/master/arjuna-samples/arjex_l10/test/module).

1. [Excel Localizer and The Magic `L` Function](https://github.com/rahul-verma/arjuna/blob/master/docs/l10/ExcelLocalizerAndTheLMaficFunction.md)
2. [Json Localizer](https://github.com/rahul-verma/arjuna/blob/master/docs/l10/JsonLocalizer.md)
3. [Strict vs Non-Strict Mode](https://github.com/rahul-verma/arjuna/blob/master/docs/l10/StrictNonStrictMode.md)

### 6. Basic Web UI Automation

You can find the example code used on this section in [arjuna_webui_basics project](https://github.com/rahul-verma/arjuna//tree/master/arjuna-samples/arjex_webui_basics/test/module).

1. [Getting Started with WebApp](https://github.com/rahul-verma/arjuna/blob/master/docs//webui_basics/WebApp.md)
2. [GuiElement - Identification and Interactions](https://github.com/rahul-verma/arjuna/blob/master/docs/webui_basics/GuiElement.md)
2. [Creating Reusable Module](https://github.com/rahul-verma/arjuna/blob/master/docs/webui_basics/ReusableModule.md)
3. [GuiMultiElement](https://github.com/rahul-verma/arjuna/blob/master/docs/webui_basics/GuiMultiElement.md)
4. [Dropdown and RadioGroup](https://github.com/rahul-verma/arjuna/blob/master/docs/webui_basics/DropDownRadioGroup.md)

### 7. Advanced Web UI Automation
1. Finding Nested Elements
2. Alternative and Dynamic Identifiers
3. Executing JavaScript
4. Alerts, Windows, Frames
5. Configuraing Interactions with GuiInteractionConfig
6. Handling Custom DropDowns
7. Retrieving Source code with GuiSource

### 8. Gui Abstraction - GNS, App, Page, Widget and Gui Elements
The following tutorial sub-sections have multiple example projects corresponding to them. Please refer the pages for respective example projects.

1. [Gui Namespace (GNS) - Externalized Identifiers](https://github.com/rahul-verma/arjuna/blob/master/docs/gui_abstraction/GuiNamespace.md)
2. [Creating App Class](https://github.com/rahul-verma/arjuna/blob/master/docs/gui_abstraction/AppClass.md)
3. [Gui and Its Loading Model in Arjuna](https://github.com/rahul-verma/arjuna/blob/master/docs/gui_abstraction/GuiLoadingModel.md)
3. [App Object Model](https://github.com/rahul-verma/arjuna/blob/master/docs/gui_abstraction/AppObjectModel.md)
4. [App-Page Object Model](https://github.com/rahul-verma/arjuna/blob/master/docs/gui_abstraction/AppPageObjectModel.md)
5. [App-Page-Section Object Model](https://github.com/rahul-verma/arjuna/blob/master/docs/gui_abstraction/AppPageSectionObjectModel.md)

## Reference
1. Command Line Options

### Miscellaneous
1. Using Arjuna With Your Test Framework
