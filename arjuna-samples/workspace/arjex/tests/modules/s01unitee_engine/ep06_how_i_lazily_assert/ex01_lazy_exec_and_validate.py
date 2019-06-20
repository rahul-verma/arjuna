'''
This file is a part of Test Mile Arjuna
Copyright 2018 Test Mile Software Testing Pvt Ltd

Website: www.TestMile.com
Email: support [at] testmile.com
Creator: Rahul Verma

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

  http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
'''

from arjuna.tpi.markup import *
from arjuna.tpi.markup_helpers import *
from arjuna.tpi.helpers import *

'''
Here:
Step 1 passes
Step 2 errs
Step 3 fails

We are using the SOFT validator WITH EXPLICIT EVALUATION within the test after step 2.

Execution never reaches Step 3.

So, test is reported with ERROR result because of step error in step 2.

You can call evaluate any number of times in a test function.
'''

def _get_step_count():
    steps = unitee.state_mgr.get_current_thread_state().get_steps()
    return len(steps)

@test_function
def test_lazy(my):
    from arjuna.unitee import Unitee
    unitee = Unitee

    # Replace validate() call with soft_validate call
    validator = my.steps.lazy_validate("Higher purpose")
    validator.assert_that(True).is_true()  # Step 1 defined, not executed
    assert _get_step_count() == 0
    validator.assert_that(None).is_false()  # Step 2 defined, not executed
    assert _get_step_count() == 0

    validator.execute() # All steps executed
    assert _get_step_count() == 2

    validator.evaluate()  # All steps evaluated for result

    my.steps.failed("Dummy failure")  # Step 3 not executed as evaluation occurs before it

