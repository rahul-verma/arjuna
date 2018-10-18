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
For demonstration purpose, here erred steps are put in their own test methods 
as once a step fails, subsequent code is not executed.
'''


@test_function
def test_log_step_1(my):
    # Simplest step
    my.steps.log("Something happened.")


@test_function
def test_log_step_2(my):
    # Providing user-defined meta-data
    # Reported in Step Report
    my.steps.log(
                    "Some message.",
                    abc=123,
                    testing="something"
    )