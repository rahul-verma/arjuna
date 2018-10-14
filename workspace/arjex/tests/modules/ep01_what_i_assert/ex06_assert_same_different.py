from arjuna.tpi.markup import *
from arjuna.tpi.markup_helpers import *


class Sample:
    pass

s1 = Sample()
s2 = Sample()


@test_function
def assert_sameness(my):
    my.steps.assert_same("Should pass for same objects", s1, s1)
    my.steps.assert_different("Should pass for different objects", s1, s2)

    # You can also use the following instead of assert_different
    my.steps.assert_not_same("Should pass for different objects", s1, s2)


@test_function
def assert_same_fails_for_different_objects(my):
    my.steps.assert_same("Should fail for different objects.", s1, s2)


@test_function
def assert_different_fails_for_same_objects(my):
    my.steps.assert_different("Should fail for same objects.", s1, s1)


@test_function
def assert_same_errs_for_incompatible_values(my):
    my.steps.assert_same("Should err for int and string comparison", s1, 1)


@test_function
def assert_different_errs_for_incompatible_values(my):
    my.steps.assert_different("Should err for int and string comparison", s1, 1)





