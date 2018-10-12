from arjuna.tpi.markup import *
from arjuna.tpi.markup_helpers import *
from arjuna.tpi.helpers import *

from arjex.tests.modules.ep05_my_dependencies import failing_module, passing_module

@init_module(
    exclude_if=problem_in(modules(passing_module,failing_module))
)
def setup_module(my):
    pass

@test_function
def test_simple1(my):
    pass

@test_function
def test_simple2(my):
    pass