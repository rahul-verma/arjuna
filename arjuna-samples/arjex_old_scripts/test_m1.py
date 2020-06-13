from arjuna import *

@for_module
def sss(request):
    # Setup
    log_info("m setup")
    request.resources.something = 432
    yield
    # Teardown
    log_info("m teardown")

@for_test
def rrr(request):
    # Setup
    log_info("t setup")
    request.resources.something = 100
    yield
    # Teardown
    log_info("t teardown")


@test(id="t1", drive_with=record(1,2, number=1, sname="s1"))
def test_1(request, sss, rrr):
    Arjuna.get_data_store().store_shared_object(my.data.sname, my.data.number)
    # 1/0
    my.module_shared_space.test = 3


@test(id="t2", drive_with=record(sname="s1")) #, exclude_if=problem_in("t1"))
def test_2(request, sss, rrr):
    shared_obj = Arjuna.get_data_store().get_shared_object(my.data.sname)
    log_info(shared_obj)


@test(id="t3", drive_with=record(sname="s1"), exclude_if=problem_in("t1"))
def test_3(request, sss):
    shared_obj = Arjuna.get_data_store().get_shared_object(my.data.sname)
    log_info(shared_obj)