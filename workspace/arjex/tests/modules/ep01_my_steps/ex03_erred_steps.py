from arjuna.tpi.markup import *
from arjuna.tpi.markup_helpers import *

'''
For demonstration purpose, here erred steps are put in their own test methods 
as once a step fails, subsequent code is not executed.
'''


@test_function
def test_erred_step_1(my):
    # Simplest step
    my.steps.erred("Erred Step.")

    # This would not execute
    my.steps.passed("Passed Step")

@test_function
def test_erred_step_2(my):
    # Providing error message
    my.steps.erred(
                    "User defined purpose.",
                    message="Something terrible happened."
    )

@test_function
def test_erred_step_3(my):
    # Providing user-defined meta-data
    # Reported in Step Report
    my.steps.erred(
                    "User defined purpose.",
                    message="Something terrible happened.",
                    abc=123,
                    testing="something"
    )