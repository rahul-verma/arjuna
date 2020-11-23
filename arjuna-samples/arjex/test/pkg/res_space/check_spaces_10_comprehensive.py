from arjuna import *

@for_group
def gres1(request):
    request.space.g1 = "g1"
    request.space.g1_g2 = "E"
    request.space.g1_m1 = "E"
    request.space.g1_m2 = "E"
    request.space.g1_t1 = "E"
    request.space.g1_t2 = "E"
    request.space.g1_test = "E"
    yield

@for_group
def gres2(request):
    request.space.g2 = "g2"
    request.space.g1_g2 = "g2"
    request.space.g2_m1 = "E"
    request.space.g2_m2 = "E"
    request.space.g2_t1 = "E"
    request.space.g2_t2 = "E"
    request.space.g2_test = "E"
    yield

@for_module
def mres1(request, gres1, gres2):
    request.space.g1_m1 = "m1"
    request.space.g2_m1 = "m1"

    request.space.m1 = "m1"
    request.space.m1_m2 = "E"
    request.space.m1_t1 = "E"
    request.space.m1_t2 = "E"
    request.space.m1_test = "E"
    yield

@for_module
def mres2(request, gres1, gres2):
    request.space.g1_m2 = "m2"
    request.space.g2_m2 = "m2"
    request.space.m1_m2 = "m2"

    request.space.m2 = "m2"
    request.space.m2_t1 = "E"
    request.space.m2_t2 = "E"
    request.space.m2_test = "E"
    yield


@for_test
def tres1(request, mres1, mres2):
    request.space.g1_t1 = "t1"
    request.space.g2_t1 = "t1"
    request.space.m1_t1 = "t1"
    request.space.m2_t1 = "t1"

    request.space.t1 = "t1"
    request.space.t1_t2 = "E"
    request.space.t1_test = "TRES"
    yield

@for_test
def tres2(request, mres1, mres2):
    request.space.g1_t2 = "t2"
    request.space.g2_t2 = "t2"
    request.space.m1_t2 = "t2"
    request.space.m2_t2 = "t2"
    request.space.t1_t2 = "t2"

    request.space.t2 = "t2"
    request.space.t2_test = "TRES"
    yield

@test
def check_spaces_1(request, tres1, tres2):
    assert request.space.g1 == "g1"
    assert request.space.g2 == "g2"

    assert request.space.m1 == "m1"
    assert request.space.m2 == "m2"

    assert request.space.t1 == "t1"
    assert request.space.t2 == "t2"

    assert request.space.g1_g2 == "g2"
    assert request.space.g1_m1 == "m1"
    assert request.space.g1_m2 == "m2"
    assert request.space.g1_t1 == "t1"
    assert request.space.g1_t2 == "t2"

    assert request.space.g2_m1 == "m1"
    assert request.space.g2_m2 == "m2"
    assert request.space.g2_t1 == "t1"
    assert request.space.g2_t2 == "t2"

    assert request.space.m1_m2 == "m2"
    assert request.space.m1_t1 == "t1"
    assert request.space.m1_t2 == "t2"

    assert request.space.m2_t1 == "t1"
    assert request.space.m2_t2 == "t2"

    assert request.space.t1_t2 == "t2"

    request.module.space.g1_test = "test"
    request.module.space.g2_test = "test"
    request.module.space.m1_test = "test"
    request.module.space.m2_test = "test"
    request.space.t1_test = "test"
    request.space.t2_test = "test"

    request.group.space.gtest = "test"
    request.module.space.mtest = "test"

@test
def check_spaces_2(request, tres1, tres2):
    assert request.space.g1_test == "test"
    assert request.space.g2_test == "test"
    assert request.space.m1_test == "test"
    assert request.space.m2_test == "test"

    # Test level modification should not be reflected
    assert request.space.t1_test == "TRES"
    assert request.space.t2_test == "TRES"

    # At test level an explicit modification to module/group space should be seen
    assert request.space.gtest == "test"
    assert request.space.mtest == "test"
