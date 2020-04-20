from arjuna import *


@for_module
def fix_non_dd(request):
    yield 1

@for_module(drive_with=records(record(1), record(2)))
def fix_dd(request):
    yield request.data[0]

@for_test(drive_with=records(record(9), record(10)))
def fix_dd_group(request, group):
    yield group, request.data[0]

@test
def check_delegated_non_dd(request, group):
    print(group.thread_name, group.config["app.url"], group.config["check"])

@test
def check_delegated_non_dd_fix_non_dd(request, group, fix_non_dd):
    print(group.thread_name, group.config["app.url"], group.config["check"], fix_non_dd)

@test
def check_delegated_non_dd_fix_dd(request, group, fix_dd):
    print(group.thread_name, group.config["app.url"], group.config["check"], fix_dd)

@test(drive_with=records(record(7,8), record(9,10)))
def check_delegated_dd(request, data, group):
    print(group.thread_name, group.config["app.url"], group.config["check"])

@test(drive_with=records(record(1,2), record(3,4)))
def check_delegated_dd_fix_non_dd(request, data, group, fix_non_dd):
    print(group.thread_name, group.config["app.url"], group.config["check"], fix_non_dd)

@test(drive_with=records(record(1,2), record(3,4)))
def check_delegated_dd_dix_dd(request, data, group, fix_dd):
    print(group.thread_name, group.config["app.url"], group.config["check"], fix_dd)

@test(drive_with=records(record(1,2), record(3,4)))
def check_delegated_dd_fix_dd_group(request, data, fix_dd_group):
    print(fix_dd_group[0].thread_name, fix_dd_group[0].config["app.url"], fix_dd_group[0].config["check"], fix_dd_group[1])