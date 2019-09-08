# Arjuna Features - Targeted and Under Development
Following is a high level view of features that are to be developed:

The features listed here which are marked as done are available in source code on GitHub, but not available in release distribution yet.

## Priortized and Sequenced
1. Identifier Parameterization support for `With` -- DONE
   * In Java bindings, .format() methods have been added
   * Support both named as well as positional argument strings.
   * Can be used in Gui model as well along with GNS. Rather than passing element name as string, one would have to use With.gnsName().
   * Name of With.assignedName method has been changed to With.gnsName. As the former was never externally used, so there is not impact on existing user code.
   * For named parameters, casing of names as well as order of parameters does not matter.
   * Example code can be found in arjex.
2. Element Configuration (code and gns)
    * State checking
    * Type Checking
3. DropDown methods
    * sendOptionText
    * clickOption
4. Navigation bar menu Abstraction
5. WebTable Abstraction
6. Action Chains - Named method for common inetractions
7. Finding Frames based on content
8. Finding windows based on content
9. Nested Elements support
10. MultiElement filters
    * ignore
    * consider
11. wait for Absence, Invisible and Diabled

## Bug Fixes
None in known and non-fixed stage as of now.

## Subsequent Features (Not necessarily in a sequenced order)
* Classification of Errors and Exceptions
* Single Context GNS
    * Should be the default context
* AND relationship for code and gns
* Option to enable proxy in java bindings
* File based configuration `loadFromConfFile`
    * coded 
    * suite.xml
    * CLI
* WebDriver Manager
* Logger as Service
* Visualization of requests & reponses
* JavaScript 
    * Finding element or MultiElement `WithJs`
    * Sending primititve args to Javascript
    * Sending element to JavaScript
* Data Reference
* Overidabiliy and visibility of configuration options
* Clean up the setu objects?
* Documentation
    * Configuration Options
    * Bindings documentation
* Proxy support for Java bindings
* Arjuna Web Interface 
    * Need help from community contributor who knows web development

## Parallel/Future Tasks
* UniTEE reporter
    * Treeview
    * Summary
    * See whether html5.Treeview helps?
* Documentation
    * FaaST protocol
    * Create a sharable Postman collection for FaaST
* Arjuna as a Remote Service
* Jenkins and GitHub integration
* Arjuna docker Image
