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

    # This passes because Arjuna does half-up-rounding as per offset precion.
    # In this mode of rounding, if >5 digit increments preceding digit by 1.
    # if <5 digit, then preceding digit is not changed.
    # For 5, if preceding digit is an odd number, it is incremented else left as such.
    # Here while rounding to 2 places, there is a '5' after '1', hence making it 2.
    # So, 0.315 is rounded to 0.32.
    # This clubbed with allowed delta of -0.01 passes this test.
    my.steps.assert_almost_equal("Consider offset correction.", 0.315, 1/3, max_offset=0.01)

    # You can allow for larger offset as well
    my.steps.assert_almost_equal("Consider offset correction.", 0.3, 1/3, max_offset=0.03)
