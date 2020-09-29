from arjuna import *


@test
def check_nondef_local(request):
    assert C("local_data.someopt") == "parent"
    assert C("local_env.someopt") == "parent"


@test
def check_nondef_linked1(request):
    assert C("l1_data.someopt") == "linked1"
    assert C("l1_env.someopt") == "linked1"


@test
def check_nondef_linked2(request):
    assert C("l2_data.someopt") == "linked2"
    assert C("l2_env.someopt") == "linked2"


@test
def check_nondef_l1_over_l2(request):
    assert C("l1_over_l2_data.someopt") == "linked2"
    assert C("l1_over_l2_env.someopt") == "linked2"


@test
def check_nondef_l1_l2_over_parent(request):
    assert C("l1_parent_data.someopt") == "parent"
    assert C("l1_parent_env.someopt") == "parent"
    assert C("l2_parent_data.someopt") == "parent"
    assert C("l2_parent_env.someopt") == "parent"

    