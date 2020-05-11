.. _test_function:


Tests are Test Functions
========================

Writing a basic test in Arjuna is very easy. Following is a simple test skeleton:


Basic Usage of @test Decorator
==============================

.. code-block:: python

    from arjuna import *

    @test
    def check_test_name(request):
        pass

1. Create a test module in **<Project Root Directory>/test/module**. The module name should start with the prefix **check_**
2. In the python test module file, import all names from Arjuna: **from arjuna import ***. Ofcourse, as you become more aware of Arjuna's TPI (tester programming interface), you can do selective imports using Python.
3. Create a test. In Arjuna, a test is a function marked with **@test** decorator. It must start with the prefix **check_**. It should take **one mandatory argument**: **request**.
4. The contents of the test function depend on the test that you want to write.


Running a Specific Test Function
================================

You can run this test using by running **arjuna** module or running **arjuna_launcher.py** script:

.. code-block:: bash

    python -m arjuna run-selected -p path/to-proj_name -it check_test_name
    python arjuna_launcher.py run-selected -it check_test_name
