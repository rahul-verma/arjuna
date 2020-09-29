from arjuna import *

@test
def check_local_projopt(request):
    assert C("local.projopt") == 1

@test
def check_linked_projopt(request):
    assert C("linked1.projopt") == "linked1"
    assert C("linked2.projopt") == "linked2"

@test
def check_linked1_projopt_overriden_linked2(request):
    assert C("l1.projopt.over.l2") == "linked2"

@test
def check_linked1_projopt_overriden_parent(request):
    assert C("l1.projopt.over.parent") == "parent"

@test
def check_linked2_projopt_overriden_parent(request):
    assert C("l2.projopt.over.parent") == "parent"