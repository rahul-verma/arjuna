from arjuna import *

@for_test
def linked2_res(request):
    yield "linked2"

@for_test
def l1_res_over_l2(request):
    yield "linked2"

@for_test
def l2_res_over_parent(request):
    yield "linked2"