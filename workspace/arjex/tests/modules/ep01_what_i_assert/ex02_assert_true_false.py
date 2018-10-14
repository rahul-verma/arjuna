from arjuna.tpi.markup import *
from arjuna.tpi.markup_helpers import *

@test_function
def assert_truth(my):
    my.steps.assert_true("Should Pass for True value.", True)
    my.steps.assert_false("Should Pass for False value.", False)

@test_function
def assert_truth_fail_for_true(my):
    my.steps.assert_true("Should Fail for False value.", False)

@test_function
def assert_truth_fail_for_false(my):
    my.steps.assert_false("Should Fail for True value.", True)

@test_function
def assert_truth_non_boolean_raises_exception(my):
    my.steps.assert_true("Should throw error for non-boolean value", 1)