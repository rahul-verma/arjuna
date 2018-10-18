from arjuna.tpi.markup import *
from arjuna.tpi.markup_helpers import *

'''
For demonstration purpose, here failed steps are put in their own test methods 
as once a step fails, subsequent code is not executed.
'''


@test_function
def test_failed_step_1(my):
    # Simplest step
    my.steps.failed("Failed Step.")

    # This would not execute
    my.steps.passed("Passed Step")


@test_function
def test_failed_step_2(my):
    # Providing expectation and observation. They need to be provided together, else an exception is raised.
    # Reported in Step Report
    my.steps.failed(
                    "User defined purpose.",
                    expectation="Some expectation",
                    observation="Some observation"
    )

@test_function
def test_failed_step_3(my):
    # Providing failure message
    my.steps.failed(
                    "User defined purpose.",
                    expectation="Some expectation",
                    observation="Some observation",
                    message="Something terrible happened."
    )

@test_function
def test_failed_step_4(my):
    # Providing user-defined meta-data
    # Reported in Step Report
    my.steps.failed(
                    "User defined purpose.",
                    expectation="Some expectation",
                    observation="Some observation",
                    message="Something terrible happened.",
                    abc=123,
                    testing="something"
    )