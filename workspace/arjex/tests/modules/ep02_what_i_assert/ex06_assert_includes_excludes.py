from arjuna.tpi.markup import *
from arjuna.tpi.markup_helpers import *


'''
Explore more situations for this.
'''


@test_function
def assert_contains_single_value(my):
    # List containing a value
    my.steps.assert_includes("Business Purpose", [1,2,3], 2)
    my.steps.assert_excludes("Business Purpose", [1,2,3], 4)

    # Tuple containing a value
    my.steps.assert_includes("Business Purpose", (1,2,3), 2)
    my.steps.assert_excludes("Business Purpose", (1,2,3), 4)

    # Set containing a value
    my.steps.assert_includes("Business Purpose", {1,2,3}, 2)
    my.steps.assert_excludes("Business Purpose", {1,2,3}, 4)

    # Dictionary containing a key
    my.steps.assert_includes("Business Purpose", {1:'a', 2:'b', 3:'c'}, 2)
    my.steps.assert_excludes("Business Purpose", {1:'a', 2:'b', 3:'c'}, 4)

    # Dictionary containing key and value pair
    my.steps.assert_includes("Business Purpose", {1:'a', 2:'b', 3:'c'}, {2:'c'})


@test_function
def assert_contains_multi_values(my):
    # Any iterable works. The container can be a list, tuple, set or dictionary
    # The expected values can be passed as a list, tuple, set as well.
    # The expected values can be passed as a dictionary only if the actual container is of type dictionary
    # Here we consider the container as list and play with container for expected values
    my.steps.assert_includes("Business Purpose", [1,2,3], [1,2])
    my.steps.assert_includes("Business Purpose", [1, 2, 3], (1, 2))
    my.steps.assert_includes("Business Purpose", [1, 2, 3], {1, 2})

    # This would throw exception.
    #my.steps.assert_includes("Business Purpose", [1, 2, 3], {1:'a', 2:'c'})

    # This works
    my.steps.assert_includes("Business Purpose", {1:'a', 2:'b', 3:'c'}, {1:'a', 3:'c'})