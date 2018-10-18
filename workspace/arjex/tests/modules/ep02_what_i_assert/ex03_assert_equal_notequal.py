from arjuna.tpi.markup import *
from arjuna.tpi.markup_helpers import *

'''
Explore more situations for this.
'''

@test_function
def assert_equality(my):
    # Integers
    my.steps.assert_equal("Business purpose", 1, 1)
    my.steps.assert_not_equal("Business purpose", 1, 2)

    # Strings
    my.steps.assert_equal("Business purpose", "testing", "testing")
    my.steps.assert_not_equal("Business purpose", "testing", "dev")

    # booleans -> Not suggested. Should use assert_true/assert_false instead
    my.steps.assert_equal("Business purpose", True, True)
    my.steps.assert_not_equal("Business purpose", True, False)


@test_function
def assert_equal_fails_for_nonequal_ints(my):
    my.steps.assert_equal("Should fail for Non equal ints", 1, 2)


@test_function
def assert_notequal_fails_for_equal_ints(my):
    my.steps.assert_not_equal("Should fail for equal ints", 1, 1)


@test_function
def assert_equal_fails_for_nonequal_strings(my):
    my.steps.assert_equal("Should fail for Non equal strings", "testing", "testing ")


@test_function
def assert_notequal_fails_for_equal_strings(my):
    my.steps.assert_not_equal("Should fail for equal strings", "testing", "testing")


@test_function
def assert_equal_fails_for_nonequal_booleans(my):
    my.steps.assert_equal("Should fail for Non equal booleans", True, False)


@test_function
def assert_notequal_fails_for_equal_booleans(my):
    my.steps.assert_not_equal("Should fail for equal booleans", False, False)


@test_function
def assert_equal_errs_for_incompatible_values(my):
    my.steps.assert_equal("Should err for int and string comparison", 1, "testing")


@test_function
def assert_notequal_errs_for_incompatible_values(my):
    my.steps.assert_not_equal("Should err for int and string comparison", 1, "testing")


@test_function
def assert_equal_with_expected_value_as_none(my):
    my.steps.assert_equal("Should fail.", None, 1)


@test_function
def assert_notequal_with_expected_value_as_none(my):
    my.steps.assert_equal("Should pass", None, None)