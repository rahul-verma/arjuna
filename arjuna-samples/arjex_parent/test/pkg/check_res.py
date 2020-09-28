from arjuna import *

@test
def check_local_res(request, local_res):
    assert local_res == 1

@test
def check_linked_res(request, linked1_res, linked2_res):
    assert linked1_res == "linked1"
    assert linked2_res == "linked2"

@test
def check_linked1_res_overriden_linked2(request, l1_res_over_l2):
    assert l1_res_over_l2 == "linked2"

@test
def check_linked1_res_overriden_parent(request, l1_res_over_parent):
    assert l1_res_over_parent == "parent"

@test
def check_linked2_res_overriden_parent(request, l2_res_over_parent):
    assert l2_res_over_parent == "parent"