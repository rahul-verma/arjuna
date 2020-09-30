from arjuna import *


@test
def check_dref_local(request):
    assert R("contextual.bronze.user") == "parent"
    assert R("indexed.0.left") == "parent"

@test
def check_dref_l1(request):
    assert R("l1contextual.bronze.user") == "linked1"
    assert R("l1indexed.0.left") == "linked1"

@test
def check_dref_l2(request):
    assert R("l2contextual.bronze.user") == "linked2"
    assert R("l2indexed.0.left") == "linked2"

@test
def check_dref_l1_l2(request):
    assert R("l1l2contextual.bronze.user") == "linked2"
    assert R("l1l2indexed.0.left") == "linked2"

@test
def check_dref_l1_parent(request):
    assert R("l1parentcontextual.bronze.user") == "parent"
    assert R("l1parentindexed.0.left") == "parent"

@test
def check_dref_l2_parent(request):
    assert R("l2parentcontextual.bronze.user") == "parent"
    assert R("l2parentindexed.0.left") == "parent"