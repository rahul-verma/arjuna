from arjuna.tpi.markup import *
from arjuna.tpi.markup_helpers import *

@test_function
def passing_test(my):
    pass

@test_function
def failing_test(my):
    assert 1==2

@test_function
def erring_test(my):
    non_existing_keyword