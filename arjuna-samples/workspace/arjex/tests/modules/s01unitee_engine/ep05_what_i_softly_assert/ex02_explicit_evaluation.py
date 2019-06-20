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

We are using the SOFT validator.

So once Step 2 errs, execution of test DOES NOT stop. Step 3 is also executed.

Once test is finished, Arjuna evaluates the steps.

For Step 1 - no issue is reported.
For Step 2 - an error issue is reported.
For Step 3 - a failure issue is reported.

Test itself can be associated with only one primary issue id in Arjuna. 

Here multiple issues exist, so Arjuna chooses to attach the FIRST failure issue id and hence reports
the test with a failure status, although both the issues can be found in issues reported and the 
corresponding steps are also reported with failure and error status respectively.

In this case, failure existed for Step 3.
'''
@test_function
def test_soft_validator_without_explicit_evaluation(my):
    # Replace validate() call with soft_validate call
    validator = my.steps.soft_validate("Higher purpose")
    validator.assert_that(True).is_true()  # Step 1
    validator.assert_that(None).is_false()  # Step 2
    my.steps.failed("Dummy failure")  # Step 3

    # In this case step 2 causes an error, execution still proceeds because of soft validator. Issue is reported.
    # Step 3 causes an failure, which is captured by Arjuna and reported as an issue.
    # As Failure status takes precendence over error status, test result is reported as failure.


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
@test_function
def test_soft_validator_with_explicit_evaluation(my):
    # Replace validate() call with soft_validate call
    validator = my.steps.soft_validate("Higher purpose")
    validator.assert_that(True).is_true()  # Step 1
    validator.assert_that(None).is_false()  # Step 2
    validator.evaluate()  # ----> EVALUATE CALL
    my.steps.failed("Dummy failure")  # Step 3


'''
You can call evaluate any number of times in a test function.
'''
@test_function
def test_reuse_validator_after_success_evaluation(my):
    # Replace validate() call with soft_validate call
    validator = my.steps.soft_validate("Higher purpose")
    validator.assert_that(True).is_true()  # Step 1
    validator.assert_that(False).is_false()  # Step 2
    validator.evaluate()  # ----> EVALUATE CALL
    # The following step fails
    validator.assert_that(True).is_false() # Step 3
    validator.evaluate()
    # This should not execute
    validator.assert_that(True).is_true()



'''
Multiple Validators in a single test
'''
@test_function
def test_multiple_validators(my):
    from arjuna.unitee import Unitee
    unitee = Unitee
    # Replace validate() call with soft_validate call
    validator_1 = my.steps.soft_validate("Higher purpose")
    validator_1.assert_that(True).is_true()  # Step 1
    validator_1.assert_that(False).is_false()  # Step 2
    validator_1.evaluate()  # ----> EVALUATE CALL

    validator_2 = my.steps.soft_validate("Higher purpose 2")
    validator_2.assert_that(True).is_true()  # Step 3
    # The following step fails
    validator_2.assert_that(True).is_false()  # Step 4
    validator_2.evaluate()
    # This should not execute
    validator_2.assert_that(True).is_true()  # Step 5