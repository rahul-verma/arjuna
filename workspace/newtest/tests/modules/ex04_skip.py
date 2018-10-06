from arjuna.tpi.markup import *
from arjuna.tpi.markup_helpers import *
from arjuna.tpi.helpers import *

@test_function
def passing_test(my):
    pass

@skip
@test_function
def failing_test(my):
    assert 1==2
