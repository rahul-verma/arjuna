from arjuna.tpi.markup import *
from arjuna.tpi.markup_helpers import *
from arjuna.tpi.helpers import *

@test_function
def dep_that_passes(my):
    assert 1==1

@test_function
def dep_that_fails(my):
    assert 1==2

@test_function
def dep_that_errs(my):
    non_existing

@test_function(
    exclude_if=problem_in(functions(dep_that_passes, dep_that_fails, dep_that_errs))
)
def test_multiple_dep(my):
    my.steps.assert_false("Dummy", False)