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
    my.steps.assert_equal("Should pass but is not suggested as it is brittle.", 0.3333333333333333, 1/3)


@test_function
def asserting_floating_numbers_good_way_but_would_fail(my):
    # Practically, for floating point numbers you want to control precision
    my.steps.assert_equal("This is brittle.", 0.33, 1/3)


@test_function
def asserting_floating_numbers_correct_way(my):
    # Practically, for floating point numbers you want to control precision
    # 1/3 gives you 0.3333333333333333

    # This passes because you constrained precision to 2 decimal places
    my.steps.assert_almost_equal("Consider offset correction.", 0.33, 1/3, max_offset=0.01)

    # This passes because you allow a delta of +/-0.01
    my.steps.assert_almost_equal("Consider offset correction.", 0.32, 1/3, max_offset=0.01)

    # This passes because you allow a delta of +/-0.01
    my.steps.assert_almost_equal("Consider offset correction.", 0.34, 1/3, max_offset=0.01)

    # This passes because Arjuna does ROUND_HALF_EVEN as per offset precision.
    my.steps.assert_almost_equal("Consider offset correction.", 0.315, 1/3, max_offset=0.01)

    # You can allow for larger offset as well
    my.steps.assert_almost_equal("Consider offset correction.", 0.3, 1/3, max_offset=0.03)

    # You can also override the rounding strategy by providing a valid strategy from decimal module
    # E.g. following as per default rounding would fail as actual and expected
    # get rounded to 0.3 and 0.5 respectively.
    # my.steps.assert_almost_equal("Consider custom rounding.", 0.35, 0.46, max_offset=0.1)

    # However, choosing rounding ad ROUND_UP would pass this assertion.
    # So, choose rounding strageies as needed. Default would work most of the times for you.
    import decimal
    my.steps.assert_almost_equal("Consider custom rounding.", 0.35, 0.46, max_offset=0.1, rounded_as=decimal.ROUND_UP)