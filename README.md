# Arjuna

Arjuna is a Python based test automation framework developed by Rahul Verma (www.rahulverma.net). Rahul has implemented smaller variants of features in Arjuna across frameworks and organizations, or given advise around it. However Arjuna being a generic library has the most complete implementation of his ideas, away from project specific contexts and constraints.

Arjuna provides its test engine features and markup on top of pytest (https://docs.pytest.org/en/latest/).

You'd need Python 3.5+ to make use of Arjuna.

Note: On Linux, the built-in Python3 build has issues with the Python's built-in enum module which is heavily used in Arjuna. One alternative is to install ActiveState Python on linux. Advanced users can go for installing a custom Python build.

### Arjuna Installation

1. Download and install latest Python (3.5+) from https://python.org
    * If you are insterested to learn python Following are links for tutorials and docs.
    + https://docs.python.org/3.7/tutorial/index.html
    + https://docs.python.org/3.7/index.html
2. Confirm the python version installed by running the command `python --version`. If expected version in not shown, fix this by looking into PATH variables and/or to see whether you have multiple versions of Python installed.
3. Install Arjuna using the following command
    * `pip install arjuna`

### Arjuna's Core Features
1. [Project Structure](./docs/core/ProjectStructure.md)
2. [Writing Your First Test](./docs/core/WritingFirstTest.md)
3. [Value Abstraction](./docs/core/ValueAbstraction.md)
3. [Tweaking Configuration Options](./docs/core/TweakingConfigurationOptions.md)
2. [Command Line Options](./docs/core/CommandLineOptions.md)
4. [Data Driven Testing](./docs/core/DataDrivenTesting.md)

### Basic Web UI Automation
1. [Getting Started with WebApp](./docs//webui_basics/GettingStartedWithWebApp.md)
2. [GuiElement Identification and Interactions](./docs/webui_basics/GuiElementIdentificationInteractions.md)
3. [Understanding With Locators](./docs/webui_basics/UnderstandingWithLocators.md)
4. [GuiMultiElement](./docs/webui_basics/GuiMultiElement.md)
5. [Dropdown and RadioGroup](./docs/webui_basics/DropDownRadioGroup.md)

### Advanced Web UI Automation
1. [Finding Nested Elements](./docs/webui_adv/FindingNestedElements.md)
2. [Alternative and Dynamic Identifiers](./docs/webui_adv/AlternativeDynamicIdentifiers.md)
3. [Executing JavaScript](./docs/webui_adv/ExecutingJavaScript.md)
4. [Alerts, Windows, Frames](./docs/webui_adv/AlertsWindowsFrames.md)
5. [Configuraing Interactions with GuiInteractionConfig](./docs/webui_adv/GuiInteractionConfig.md)
6. [Handling Custom DropDowns](./docs/webui_adv/HandlingCustomDropDowns.md)
7. [Retrieving Source code with GuiSource](./docs/webui_adv/GuiSource.md)

### Gui Abstraction - App, Page, Widget and Gui Elements
1. [Externalised Gui Namespace (App Level)](./docs/gui_abstraction/ExternalisedGuiNamespace.md)
2. [App-Page Object Model](./docs/gui_abstraction/AppPageObjectModel.md)
3. [App-Page-Widget Object Model](./docs/gui_abstraction/AppPageWidgetObjectModel.md)

### Miscellaneous
1. Using Arjuna With Your Test Framework
