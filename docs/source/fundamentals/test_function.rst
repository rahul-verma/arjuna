.. _test_function:


**Basics** of Writing **Automated Tests** in Arjuna
===================================================

Tests are **Test Functions**
----------------------------

Writing a basic test in Arjuna is very easy. Following is a simple test skeleton:


Basic Usage of **@test Decorator**
----------------------------------

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
------------------------------------

.. code-block:: bash

    pytest -p arjuna --project path/to-proj_name --itest check_test_name

To learn more about other options for controlling which tests are run, refer :ref:`cli_testselect`