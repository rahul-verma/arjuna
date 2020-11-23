from arjuna import *

@for_group
def gres(request):
    request.space.immutable = "testing"
    request.space.mutable = {1:2, 3:4}
    yield

@for_group
def another_gres(request, gres):
    assert request.space.immutable == "testing"
    assert request.space.mutable[3] == 4
    yield

@for_module
def mres(request):
    assert request.space.immutable == "testing"
    assert request.space.mutable[3] == 4
    yield

@for_test
def tres(request, gres):
    assert request.space.immutable == "testing"
    assert request.space.mutable[3] == 4
    yield

@test
def check_group_space_1(request, gres):
    assert request.module.space.immutable == "testing"
    assert request.module.space.mutable[3] == 4

@test
def check_group_space_2(request, another_gres, mres, tres):
    pass

@test
def check_group_space_suggested_way(request, gres):
    assert request.space.immutable == "testing"
    assert request.space.mutable[3] == 4

@test
def check_group_space_3_1_modify(request, gres):
    request.group.space.immutable = "changed"
    request.group.space.mutable[5] = 6
    assert request.space.immutable == "changed"
    assert request.space.mutable[5] == 6

@test
def check_group_space_3_2_test(request, gres):
    assert request.space.immutable == "changed"
    assert request.space.mutable[5] == 6

@for_group
def gres_multi_1(request):
    request.space.something = "test"
    yield

@for_group
def gres_multi_2(request):
    assert request.space.something == "test"
    request.space.something = "changed"
    yield

@test
def check_space_multi_res(request, gres_multi_1, gres_multi_2):
    assert request.space.something == "changed"


@for_group
def gres_chain_1(request):
    request.space.something = "test"
    yield

@for_group
def gres_chain_2(request, gres_chain_1):
    assert request.space.something == "test"
    request.space.something = "changed"
    yield

@test
def check_space_chain(request, gres_chain_2):
    assert request.space.something == "changed"


@test
def check_crud_add(request):
    # Some object addition code followed by
    request.group.space.created_id = "abc123"

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
