from arjuna.tpi.markup import *
from arjuna.tpi.markup_helpers import *
from arjuna.tpi.helpers import *


@init_module(author="mouli")
def something(my):
    my.steps.assert_true("Should be true", True)

@init_each_function
def each(my):
    my.steps.assert_false("something", True)

@test_function
def passing_test(my):
    print(my.info.function.props)

@end_each_function
def failing(my):
    my.steps.assert_false("g", True)