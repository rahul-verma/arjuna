from arjuna import *

@test
def check_def_data_env(request):
    assert C("local.data") == "parent"
    assert C("local.env") == "parent"

    assert C("l1.data") == "linked1"
    assert C("l1.env") == "linked1"
    assert C("l2.data") == "linked2"
    assert C("l2.env") == "linked2"

    assert C("l1.l2.data") == "linked2"
    assert C("l1.l2.env") == "linked2"

    assert C("l1.parent.data") == "parent"
    assert C("l1.parent.env") == "parent"
    assert C("l2.parent.data") == "parent"
    assert C("l2.parent.env") == "parent"