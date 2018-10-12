from arjuna.tpi.markup import *
from arjuna.tpi.markup_helpers import *
from arjuna.tpi.helpers import *

from arjex.tests.modules.ep05_my_dependencies import failing_module

@init_module(
    exclude_if = problem_in(modules(failing_module))
)
def init_module(my):
    pass

@test_function
def dep_that_passes(my):
    assert 1==1