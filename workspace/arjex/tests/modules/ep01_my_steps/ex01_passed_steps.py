from arjuna.tpi.markup import *
from arjuna.tpi.markup_helpers import *

@test_function
def test_passed_steps(my):
    # Simplest step
    my.steps.passed("User defined purpose.")

    # Providing expectation and observation. They need to be provided together, else an exception is raised.
    # Reported in Step Report
    my.steps.passed(
                    "User defined purpose.",
                    expectation="Some expectation",
                    observation="Some observation"
    )

    # Providing user-defined meta-data
    # Reported in Step Report
    my.steps.passed(
                    "User defined purpose.",
                   expectation="Some expectation",
                   observation="Some observation",
                   abc=123,
                   testing="something"
    )

    # You can see 3 steps in the report with corresponding information