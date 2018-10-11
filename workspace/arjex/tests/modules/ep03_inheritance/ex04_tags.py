from arjuna.tpi.markup import *
from arjuna.tpi.markup_helpers import *
from arjuna.tpi.helpers import *

@init_module(
    tags=tags(1,2,3)
)
def setup_module(my):
    pass

@test_function
def demo_immutable_tags(my):
    console.display(my.tags)