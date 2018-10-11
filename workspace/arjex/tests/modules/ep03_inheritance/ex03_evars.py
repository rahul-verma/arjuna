from arjuna.tpi.markup import *
from arjuna.tpi.markup_helpers import *
from arjuna.tpi.helpers import *

@init_module(
    evars=evars(static_var="s1"),
)
def setup_module(my):
    my.evars['dynamic_var'] = True

@test_function
def demo_immutable_tags(my):
    console.display(my.evars)