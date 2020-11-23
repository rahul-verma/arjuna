from arjuna import *

@for_module
def mres(request):
    request.space.immutable = "testing"
    request.space.mutable = {1:2, 3:4}
    yield

@for_module
def another_mres(request, mres):
    assert request.space.immutable == "testing"
    assert request.space.mutable[3] == 4
    yield

@for_test
def tres(request, mres):
    assert request.space.immutable == "testing"
    assert request.space.mutable[3] == 4
    yield

@test
def check_mod_space_1(request, mres):
    assert request.module.space.immutable == "testing"
    assert request.module.space.mutable[3] == 4

@test
def check_mod_space_2(request, another_mres, tres):
    pass

@test
def check_mod_space_suggested_way(request, mres):
    assert request.space.immutable == "testing"
    assert request.space.mutable[3] == 4

@test
def check_mod_space_3_1_modify(request, mres):
    request.module.space.immutable = "changed"
    request.module.space.mutable[5] = 6
    assert request.space.immutable == "changed"
    assert request.space.mutable[5] == 6

@test
def check_mod_space_3_2_test(request, mres):
    assert request.space.immutable == "changed"
    assert request.space.mutable[5] == 6

@for_module
def mres_multi_1(request):
    request.space.something = "test"
    yield

@for_module
def mres_multi_2(request):
    assert request.space.something == "test"
    request.space.something = "changed"
    yield

@test
def check_space_multi_res(request, mres_multi_1, mres_multi_2):
    assert request.space.something == "changed"


@for_module
def mres_chain_1(request):
    request.space.something = "test"
    yield

@for_module
def mres_chain_2(request, mres_chain_1):
    assert request.space.something == "test"
    request.space.something = "changed"
    yield

@test
def check_space_chain(request, mres_chain_2):
    assert request.space.something == "changed"


@test
def check_crud_add(request):
    # Some object addition code followed by
    request.module.space.created_id = "abc123"

@test
def check_crud_edit(request):
    cid = request.space.created_id
    # Code to edit object for this id
    assert cid == "abc123"

@test
def check_crud_delete(request):
    cid = request.space.created_id
    # Code to delete object for this id
    assert cid == "abc123"
