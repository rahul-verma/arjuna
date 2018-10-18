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
Explore more situations for this.
'''

@test_function
def asserting_floating_numbers_bad_way(my):
    # This internally gets delegated to approximation matching.
    # This happens when either or both of actual and expected values are of float type.
    my.steps.validate("Brittle float equality check.").assert_that(0.3333333333333333).is_equal_to(1/3)

@test_function
def asserting_floating_numbers_good_way_but_would_fail(my):
    # Practically, for floating point numbers you want to control precision
    my.steps.validate("Brittle float equality check.").assert_that(0.33).is_equal_to(1/3)

@test_function
def asserting_floating_numbers_correct_way(my):
    validator = my.steps.validate("Various floating un/equality checks")

    # Practically, for floating point numbers you want to control precision
    # 1/3 gives you 0.3333333333333333

    # This passes because you constrained precision to 2 decimal places
    validator.assert_that(0.33).with_max_offset(0.01).is_equal_to(1/3)

    # This passes because you allow a offset of +/-0.01
    validator.assert_that(0.32).with_max_offset(0.01).is_equal_to(1/3)

    # This passes because you allow a offset of +/-0.01
    validator.assert_that(0.34).with_max_offset(0.01).is_equal_to(1/3)

    # This passes because Arjuna does ROUND_HALF_EVEN as per offset precision.
    validator.assert_that(0.315).with_max_offset(0.01).is_equal_to(1/3)

    # You can allow for larger offset as well
    validator.assert_that(0.3).with_max_offset(0.03).is_equal_to(1/3)

    # You can also override the rounding strategy by providing a valid strategy from decimal module
    # E.g. following as per default rounding would fail as actual and expected
    # get rounded to 0.3 and 0.5 respectively.
    # validator.assert_that(0.35).with_max_offset(0.1).is_equal_to(0.46)

    # However, choosing rounding ad ROUND_UP would pass this assertion.
    # So, choose rounding strageies as needed. Default would work most of the times for you.
    import decimal
    validator.assert_that(0.35).with_max_offset(0.1).rounded_as(decimal.ROUND_UP).is_equal_to(0.46)

    # Precision of >4
    # The following would throw an exception
    #my.steps.validate(">4 precision offset.").assert_that(0.33332).with_max_offset(0.00001).is_equal_to(1/3)

    # To achieve this, pass the number in a string format.
    my.steps.validate(">4 precision offset.").assert_that(0.33332).with_max_offset("0.00001").is_equal_to(1/3)

    # This gives you the power for much more precision
    my.steps.validate("60 precision offset.")\
        .assert_that(0.333333333333333333333333333333333333333333333333333333333333)\
        .with_max_offset("0.000000000000000000000000000000000000000000000000000000000001")\
        .is_equal_to(1/3)

