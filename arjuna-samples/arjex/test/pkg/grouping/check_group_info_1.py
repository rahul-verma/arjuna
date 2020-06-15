from arjuna import *


@for_test
def fix_non_dd(request):
    print(request.group.name)
    yield 1

@for_test(drive_with=records(record(1), record(2)))
def fix_dd(request):
    print(request.group.name)
    yield request.data[0]

@test
def check_default_without_fix(request):
    print(request.group.thread_name, request.group.config["app.url"], request.group.config["check"])

@test
def check_delegated_non_dd_fix(request, fix_non_dd):
    print(request.group.thread_name, request.group.config["app.url"], request.group.config["check"], fix_non_dd)

@test(drive_with=records(record(7,8), record(9,10)))
def check_delegated_non_dd_fix_dd_test(request, data, fix_non_dd):
    print(request.group.thread_name, request.group.config["app.url"], request.group.config["check"], data, fix_non_dd)

@test
def check_delegated_dd_fix(request, fix_non_dd, fix_dd):
    print(request.group.thread_name, request.group.config["app.url"], request.group.config["check"], fix_non_dd, fix_dd)

@test(drive_with=records(record(7,8), record(9,10)))
def check_delegated_dd_fix_dd_test(request, data, fix_non_dd, fix_dd):
    print(request.group.thread_name, request.group.config["app.url"], request.group.config["check"], data, fix_non_dd, fix_dd)