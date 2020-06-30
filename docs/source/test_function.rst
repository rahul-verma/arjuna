.. _test_function:


Tests are **Test Functions**
============================

Writing a basic test in Arjuna is very easy. Following is a simple test skeleton:


Basic Usage of **@test Decorator**
==================================

.. code-block:: python

    from arjuna import *

    @test
    def check_test_name(request):
        pass

1. Create a test module in **<Project Root Directory>/test/pkg**. The module name should start with the prefix **check_**
2. In the python test module file, import all names from Arjuna: **from arjuna import ***. Ofcourse, as you become more aware of Arjuna's TPI (tester programming interface), you can do selective imports using Python.
3. Create a test. In Arjuna, a test is a function marked with **@test** decorator. It must start with the prefix **check_**. It should take **one mandatory argument**: **request**.
4. The contents of the test function depend on the test that you want to write.


**Running** a Specific Test Function
====================================

You can run this test by running **arjuna** module or running **arjuna_launcher.py** script:

.. code-block:: bash

    python -m arjuna run-selected -p path/to-proj_name -it check_test_name
    python arjuna_launcher.py run-selected -it check_test_name


**Skipping** a Test
===================

You can mark a test as skipped:

.. code-block:: python

    from arjuna import *

    @test(skip=True)
    def check_test_name(request):
        pass


You can also do a conditional skipping:

.. code-block:: python

    from arjuna import *

    @test(skip=skip("abc > 2", reason="Foo bar"))
    def check_test_name(request):
        pass


Handling **Expected Failures** in Tests
=======================================

You can mark a test as a test which is expected to fail:

.. code-block:: python

    from arjuna import *

    @test(xfail=True)
    def check_test_name(request):
        pass


You can also specify advanced conditional expected failures:

.. code-block:: python

    from arjuna import *

    @test(xfail=xfail("abc > 2", reason="Foo bar", raises=SomeException, run=True, strict=True))
    def check_test_name(request):
        pass

Such a test is reported as XFailed. If it passes, it is reported as XPassed.


Specifying **Built-in Test Attributes**
=======================================

Arjuna tests have many built-in attributes, which can be specified as an argument in **@test**, for example:

.. code-block:: python

    from arjuna import *

    @test(id="SomeID", priority=3)
    def check_test_name(request):
        pass

Following is the complete list:

* Overridable Attributes:
    * **id**: Alnum string representing an ID which you want to associate with the test.
    * **priority**: An integer value 1-5 depicting priority of this test, 1 being highest, 5 being lowest.
    * **author**: Author of this test
    * **idea**: The idea describing this test
    * **component**: Primary software component that this test targets.
    * **app_version**: Version of SUT that this test targets
    * **level**: Level of this test.
    * **reviewed**: Has this test been reviewed?
    * **unstable**: Is this test unstable?
* Non-overridable Attributes:
    * **package**: Full qualified package
    * **module**: Name of module containing this test
    * **name**: Name of this test function
    * **qual_name**: Full qualified name of this test function **<package>.<module>.<function>**

**User-Defined Test Attributes**
================================

You can define any number of your own attributes for a test:


.. code-block:: python

    from arjuna import *

    @test(policy="Some policy")
    def check_test_name(request):
        pass


Specifying **Tags, Bugs, Environments**
=======================================

Arjuna tests have built-in tag containers (sets), which can be specified as an argument in **@test**, for example:

.. code-block:: python

    from arjuna import *

    @test(tags={'t1', 't2'}, bugs={'b1','b2'}, envs={'e1','e2'})
    def check_test_name(request):
        pass

Following are the containers:
    * **bugs**: Set of bugs associated with this test
    * **envs**: Set of Environment names on which this test is supposed to run.
    * **tags**: Set of arbitrary tags for this test
