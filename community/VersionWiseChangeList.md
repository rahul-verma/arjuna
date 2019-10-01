# Version-wise Change List for Arjuna and Arjuna-Java Bindings
Arjna and Arjuna-Java bindings development goes hand in hand as Arjuna-Java is considered as the reference bindings implementation.

In the following sections, you can find version wise change list for both packages:

### Arjuna v0.7.8 and Arjuna-Java Bindings v0.1.3
1. Identifier Parameterization support for `With`
   * In Java bindings, .format() methods have been added
   * Support for both named as well as positional argument strings.
   * Can be used in Gui model as well along with GNS. Rather than passing element name as string, one would have to use With.gnsName() for parameterization.
   * Name of With.assignedName method has been changed to With.gnsName. As the former was never externally used, so there is not impact on existing user code.
   * For named parameters, casing of names as well as order of parameters does not matter.
   * Example code can be found in arjex.
2. Element Configuration (code and gns)
    * State checking: Implemented for GuiElement, DropDown and RadioGroup. Pre-interaction and Post-interaction state checking can be switched on and off by the client.
    * Type Checking: Client can switch off type checking for controls which Arjuna does for some contexts.
3. More DropDown methods
    * setOptionContainer - To handle custom Dropdown controls like those in Bootstrap.
    * setOptionLocators - To handle with custom drop down controls implemented using div tags.
    * sendOptionText - To handle unstable drop down lists with a lot of options.
4. Reduction in GuiActionType options
    * To control the number of actions, the actions are now qualified with origGuiComponentType JSON parameter in Setu protocol.
    * This measure is to simplify client bindings code by reducing number and complexity of methods needed to be implemented.
    * No impact on test author's code.
5. GuiSource abstraction
    * Created a Source() method for Gui automator and other Gui components.
    * Dealing with precise parts of source, for example, root content, inner content etc should be provided by Source service.
    * This measure is critical to keep number of API calls in client bindings in control.
    * In future, it also creates the basis for TextBlob parsing as a service.
    * There is a slight impact on the test author code. Rather than component.getSource(), the test author would write component.Souce().getFullContent(). Rest of the provisions that were earlier not available at all, are an add-on thereby making it consistent across all gui components. For now getRootContent(), getInnerContent() and getTextContent() methods are other methods supported by GuiSource interface.
6. Bug Fix: Arjuna-Java client does not send unicode strings properly to Setu.
7. Advanced Window Finding
    * Based on Title
    * Based on Partial Title
    * Based on Child Locator (Content)
