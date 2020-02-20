from arjuna import *

@for_module
def mod1_fix(request):
    # Setup
    request.space.fix_mod1_unique = "mod1_unique"
    request.space.fix_mod1_update_inmod2 = "should not be this"
    request.space.fix_mod1_update_func_fix = "should not be this"
    request.space.fix_mod1_update_test1 = "should not be this"
    yield

@for_module
def mod2_fix(request):
    # Setup
    request.space.fix_mod2_unique = "mod2_unique"
    request.space.fix_mod1_update_inmod2 = "updated_in_mod_2"
    request.space.fix_mod2_update_func_fix = "should not be this"
    request.space.fix_mod2_update_test1 = "should not be this"
    yield


@for_test
def func_fix(request):
    request.space.fix_func_unique = "func_unique"
    request.space.fix_mod1_update_func_fix = "mod1_update_in_func"
    request.space.fix_mod2_update_func_fix = "mod2_update_in_func"
    request.space.fix_func_update_test1 = "should not be this"
    yield

@test
def check_spaces_1(my, request, mod1_fix, mod2_fix, func_fix):
    print(my.space.fix_mod1_unique)
    print(my.space.fix_mod2_unique)

    print(my.space.fix_mod1_update_inmod2)

    print(my.space.fix_mod1_update_func_fix)
    print(my.space.fix_mod2_update_func_fix)

    my.module.space.mod_space_add_from_test = "should get in check 2"

@test
def check_spaces_2(my, request, func_fix):
    print(my.space.fix_mod1_unique)
    print(my.space.fix_mod2_unique)

    print(my.space.fix_mod1_update_inmod2)

    print(my.space.fix_mod1_update_func_fix)
    print(my.space.fix_mod2_update_func_fix)


    print(my.space.mod_space_add_from_test)