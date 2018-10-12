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
    exclude_if=problem_in(functions(dep_that_passes))
)
def depends_on_passing_test(my):
    my.steps.assert_false("Dummy", False)

@test_function(
    exclude_if=problem_in(functions(dep_that_fails))
)
def depends_on_failing_test(my):
    my.steps.assert_false("Dummy", False)


@test_function(
    exclude_if=problem_in(functions(dep_that_errs))
)
def depends_on_erring_test(my):
    my.steps.assert_false("Dummy", False)