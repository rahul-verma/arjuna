from arjuna import *

@for_test
def local_res(request):
    yield 1

@for_test
def l1_res_over_parent(request):
    yield "parent"

@for_test
def l2_res_over_parent(request):
    yield "parent"