# Arjuna Features - Targeted and Under Development
Following is a high level view of features that are to be developed:

The features listed here which are marked as done are available in source code on GitHub, but not available in release distribution yet.
    
# Java-Bindings and Corresponding Support in Arjuna

## Phase 1 - Selenium Core Completion - Target Oct 18, 2019
1. Element Configuration (code and gns)
    * Support at automator level.
    * Support at configuration level
2. Advanced Frame related functionality - In Progress
    * Enumerating immediate frames at Dom Root and Frame level
    * Content based frame finding for immediate child frames
3. Initial implementation of Screen and Point abstraction - Done
4. Support for With.POINT for element identification. - Done
5. Support for With.JS for element identification - In progress.
  * Single element - If JS returns multiple elements, should return first one.
  * Multi-element - If JS returns single element, should return it as a list.
6. Action Chains - Named method for common interactions
   * Client-side interfaces and classes - Mostly done
   * FaaST implementation - In progress
   * Arjuna implementation - In progress
7. Nested Elements support
8. wait for Absence, Invisible and Disabled

## Phase 2 - Completion of Pending Core Framework Features in Arjuna - Nov 29, 2019
* Map valid With options to tpye of component. Clear exceptions with troubleshooting to be coded.
* Explicit wait in Arjuna Setu for Frames and Windows, which works under the total limit of gui max wait.
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
* Default type checking for enter/set text, check/unckeck, toggle operations etc.
* Optimization of option level or radio button level state and attribute checking in DropDown and RadioButton abstractions
* 

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



