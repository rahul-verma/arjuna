# Arjuna

![Arjuna](https://github.com/rahul-verma/arjuna/blob/master/Arjuna.png)

Arjuna is a **Python based test automation framework** developed by [Rahul Verma](www.rahulverma.net). It is an open source, Apache Licensed software.

Rahul has implemented smaller variants of features in Arjuna across frameworks and organizations, or given advise around it. However Arjuna being a generic library has the most complete implementation of his ideas, away from project specific contexts and constraints.

For test execution, Arjuna is implemented as a **[pytest](https://docs.pytest.org/en/latest/)** plugin and provides its own markup over pytest as its underlying test engine. If you like, you can make use of Arjuna with any other test engine or custom frameworks as well.

You'd need **Python 3.8+** to make use of Arjuna.

Note: On Linux, the built-in Python3 build has issues with the Python's built-in enum module which is heavily used in Arjuna. One alternative is to install ActiveState Python on linux. Advanced users can go for installing a custom Python build.

## Documentation
Arjuna documentation is integated with ReadTheDocs. 

* Documentation for the **[last released version](https://arjuna-taf.readthedocs.io/en/stable/index.html)**
    * Release build goes through the existing tests and hence is better for production use than master branch.
* Documentation for the **[latest master branch](https://arjuna-taf.readthedocs.io)**
    * Please note that the master branch is an active branch and can have untested code.
    * Contains the latest and greatest upcoming features and updates to existing ones.
