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

'''
Here:
Step 1 passes
Step 2 fails
Step 3 Errs

We are using the regular validator.

So once Step 2 fails, execution of test stops. Step 3 is not executed.
'''
@test_function
def test_usual_validator(my):
    validator = my.steps.validate("Higher purpose")
    validator.assert_that(True).is_true()  # Step 1
    validator.assert_that(True).is_false()  # Step 2
    my.steps.erred("Dummy error")  # Step 3

'''
Here:
Step 1 passes
Step 2 fails
Step 3 Errs

We are using the SOFT validator.

So once Step 2 fails, execution of test DOES NOT stop. Step 3 is also executed.

Once test is finished, Arjuna evaluates the steps.

For Step 1 - no issue is reported.
For Step 2 - a failure issue is reported.
For Step 3 - an error issue is reported.

Test itself can be associated with only one primary issue id in Arjuna. 

Here multiple issues exist, so Arjuna chooses to attach the FIRST failure issue id and hence reports
the test with a failure status, although both the issues can be found in issues reported and the 
corresponding steps are also reported with failure and error status respectively.
'''
@test_function
def test_soft_validator_automatic_evaluation(my):
    # Replace validate() call with soft_validate call
    # All fluent assertions that work for regular validator, work in the same manner for soft validator
    validator = my.steps.soft_validate("Higher purpose")
    validator.assert_that(True).is_true()  # Step 1
    validator.assert_that(True).is_false()  # Step 2
    my.steps.erred("Dummy error")  # Step 3