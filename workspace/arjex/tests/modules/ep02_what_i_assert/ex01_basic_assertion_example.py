from arjuna.tpi.markup import *
from arjuna.tpi.markup_helpers import *

'''
Arjuna expects you to always provide the business purpose of assertions
unlike other engines which make it optional.
'''

@test_function
def test_basic_assertion_pass(my):
    my.steps.assert_true("Business purpose", True)

@test_function
def test_basic_assertion_fail(my):
    my.steps.assert_true("Business purpose", False)