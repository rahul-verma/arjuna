# Arjuna Features - Targeted and Under Development
Following is a high level view of features that are to be developed:

The features listed here which are marked as done are available in source code on GitHub, but not available in release distribution yet.

# Java-Bindings and Corresponding Support in Arjuna

## Phase 1 - Selenium Core Completion - Target Oct 18, 2019
1. Identifier Parameterization support for `With` -- DONE
   * In Java bindings, .format() methods have been added
   * Support both named as well as positional argument strings.
   * Can be used in Gui model as well along with GNS. Rather than passing element name as string, one would have to use With.gnsName().
   * Name of With.assignedName method has been changed to With.gnsName. As the former was never externally used, so there is not impact on existing user code.
   * For named parameters, casing of names as well as order of parameters does not matter.
   * Example code can be found in arjex.
2. Element Configuration (code and gns) - In Progress
    * State checking: Implemented for GuiElement, DropDown and RadioGroup. Pre-interaction and Post-interaction state checking can be sqitched on and off by the client. - Done
    * Type Checking: Client can switch off type checking for controls which Arjuna does for some contexts. - Done
    * Support at automator level.
    * Support at configuration level
3. Element should load specific pieces of DOM belonging to it as well as complete outerHTML.
3. DropDown methods
    * setOptionContainer - Done
    * setOptionLocators - Done
    * sendOptionText
4. Finding Frames based on content
5. Finding Windows based on content
6. Action Chains - Named method for common inetractions
9. Nested Elements support
11. wait for Absence, Invisible and Disabled

## Phase 2 - Completion of Pending Core Framework Features in Arjuna - Nov 29, 2019
* Names of CLI options to be changed to baseline and extended
* Classification of Errors and Exceptions
* Single Context GNS
    * Should be the default context
* Element configuration support in GNS
* AND relationship for code and gns
* Option to enable proxy in java bindings
* File based configuration `loadFromConfFile`
    * coded 
    * suite.xml
    * CLI
* Add support for envioronment variables to be consumed in configuration
* Overidabiliy and visibility of configuration options ---> This needs to be implemented before CLI can be discussed: Following are the levels for which it should be clearly defined. Preferrably all configuration settings should be documented as matrix with the mapping:
    * Project.conf
    * Programmatic
    * CLI - Baseline
    * CLI - Extended
* Clean up the setu objects?
* Data Reference

## Phase 3 - Additional Abstractions and Features for Selenium - 24 Dec, 2019 (Jan 1 2020 - 1.0 First production Release)
* Navigation bar menu Abstraction
* WebTable Abstraction
* MultiElement filters
    * ignore
    * consider
* WebDriver Manager
* JavaScript 
    * Finding element or MultiElement `WithJs`
    * Sending primititve args to Javascript
    * Sending element to JavaScript
* Support for Multi-select Dropdown list
* Optimization of option level or radio button level state and attribute checking in DropDown and RadioButton abstractions

## Phase 4 - March 31, 2019 (In Parallel to Next Feature Section)
* Documentation
    * Configuration Options
    * Bindings documentation
* Documentation
    * FaaST protocol
    * Create a sharable Postman collection for FaaST
    
# Extended Arjuna Features, Python Bindings and Corresponding Support in Arjuna

## Phase 1 - March 31, 2019
* Completion of Python Bindings in alignment with Java Bindings
  * Create a list and high level doc of what is expected from Bindings currently
  * List the features here and track feature wise completion after critical testing
* Logger as Service
* Visualization of requests & responses
* UniTEE reporter
    * Treeview
    * Summary
    * See whether html5.Treeview helps?   
## Phase 2 - Tentatively a 6 month schedule
* Arjuna Web Interface 
    * Need help from community contributor who knows web development
* Arjuna as a Remote Service
* Jenkins and GitHub integration
* Arjuna docker Image

# Bug Fixes
None in known and non-fixed stage as of now.



