from arjuna import *

@for_test
def tres(request):
    request.space.immutable = "testing"
    request.space.mutable = {1:2, 3:4}
    yield

@for_test
def another_tres(request, tres):
    assert request.space.immutable == "testing"
    assert request.space.mutable[3] == 4
    yield

@test
def check_test_space_1(request, tres):
    assert request.space.immutable == "testing"
    assert request.space.mutable[3] == 4

@test
def check_test_space_2(request, another_tres):
    pass

@test
def check_test_space_3_1_modify(request, tres):
    request.space.immutable = "changed"
    request.space.mutable[5] = 6
    assert request.space.immutable == "changed"
    assert request.space.mutable[5] == 6

@test(xfail=True)
def check_test_space_3_2_test(request, tres):
    assert request.space.immutable == "changed" # Fails
    assert request.space.mutable[5] == 6 # Will Fail if above is commented.

@for_test
def tres_multi_1(request):
    request.space.something = "test"
    yield

@for_test
def tres_multi_2(request):
    assert request.space.something == "test"
    request.space.something = "changed"
    yield

@test
def check_space_multi_res(request, tres_multi_1, tres_multi_2):
    assert request.space.something == "changed"


@for_test
def tres_chain_1(request):
    request.space.something = "test"
    yield

@for_test
def tres_chain_2(request, tres_chain_1):
    assert request.space.something == "test"
    request.space.something = "changed"
    yield

@test
def check_space_chain(request, tres_chain_2):
    assert request.space.something == "changed"