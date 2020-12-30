from arjuna import *

@test
def check_pass(request):
    assert 1 == 1

@test
def check_fail(request):
    assert 1 == 2