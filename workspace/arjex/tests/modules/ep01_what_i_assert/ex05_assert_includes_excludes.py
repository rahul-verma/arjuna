from arjuna.tpi.markup import *
from arjuna.tpi.markup_helpers import *


'''
Explore more situations for this.
'''
@test_function
def assert_content(my):
    # List
    my.steps.assert_includes("Business Purpose", [1,2,3], 2)
    my.steps.assert_excludes("Business Purpose", [1,2,3], 4)

    # Tuple
    my.steps.assert_includes("Business Purpose", (1,2,3), 2)
    my.steps.assert_excludes("Business Purpose", (1,2,3), 4)

    # Set
    my.steps.assert_includes("Business Purpose", {1,2,3}, 2)
    my.steps.assert_excludes("Business Purpose", {1,2,3}, 4)

    # Dictionary
    my.steps.assert_includes("Business Purpose", {1:'a', 2:'b', 3:'c'}, 2)
    my.steps.assert_excludes("Business Purpose", {1:'a', 2:'b', 3:'c'}, 4)
