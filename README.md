# Test Mile Arjuna

Arjuna is a Python based test automation framework developed by Rahul Verma (www.rahulverma.net). It is a based on FaaST (Framework as a Service for Testing), seen as need of the hour in 2019. The FaaST architecture enables integration of multiple programming languages, multiple tools, GUI definition externalization, customized identification types and so on, with finer control of each component. Rahul as the Chief Consultant at Test Mile, has implemented smaller variants of this model across frameworks and organizations, or given advise around it. However Arjuna being a generic library has the most complete implementation of the said model, away from project specific contexts and constraints.

Arjuna includes the Python version of client lib.

Arjuna also includes UniTEE, a test engine that espouses the principles of Test Encapsulation by Rahul, as envisioned in a research paper in 2010.  It combines pragmatism by including decisions which are taken outside of the test for performance reasons.

You'd need Python 3.5+ to make use of Arjuna.

Note: On Linux, the built-in Python3 build has issues with the Python's built-in enum module which is heavily used in Arjuna. One alternative is to install ActiveState Python on linux. Advanced users can go for installing a custom Python build.

Documentation for Arjuna is in progress. You can can find the currrent help doc on Test Mile website at https://testmile.com/arjuna

### Arjuna Installation

1. Download and install latest Python (3.5+) from https://python.org
    * If you are insterested to learn python Following are links for tutorials and docs.
    + https://docs.python.org/3.7/tutorial/index.html
    + https://docs.python.org/3.7/index.html
2. Confirm the python version installed by running the command `python --version`. If expected version in not shown, fix this by looking into PATH variables and/or to see whether you have multiple versions of Python installed.
3. Install the arjuna-python binding using the following command
    * `pip install arjuna`
