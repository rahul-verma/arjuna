from arjuna.tpi.markup import *
from arjuna.tpi.markup_helpers import *
from arjuna.tpi.helpers import *

@skip_me
@init_module
def setup_module(my):
    pass

@test_function
def demo_skip_based_on_module_1(my):
    print("This should not print - 1.")

@test_function
def demo_skip_based_on_module_2(my):
    print("This should not print - 2.")