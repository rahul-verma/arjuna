from arjuna.tpi.markup import *
from arjuna.tpi.markup_helpers import *


@test_function
def assert_nothingness(my):
    my.steps.assert_none("Business Purpose", None)
    my.steps.assert_not_none("Business Purpose", 1)


@test_function
def assert_none_fails_for_notnone(my):
    my.steps.assert_none("Should fail for not None value", 1)


@test_function
def assert_notnone_fails_for_none(my):
    my.steps.assert_not_none("Should fail for None value.", None)

