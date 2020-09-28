from arjuna import *

@for_test
def linked1_res(request):
    yield "linked1"

@for_test
def l1_res_over_l2(request):
    yield "linked1"

@for_test
def l1_res_over_parent(request):
    yield "linked1"