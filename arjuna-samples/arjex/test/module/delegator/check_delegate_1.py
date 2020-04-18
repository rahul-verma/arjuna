from arjuna import *


@for_module
def fix_non_dd(request):
    yield 1

@for_module(drive_with=records(record(1), record(2)))
def fix_dd(request):
    yield request.data[0]

@for_test(drive_with=records(record(9), record(10)))
def fix_dd_delegator(request, delegator):
    yield delegator, request.data[0]

@test
def check_delegated_non_dd(request, delegator):
    print(delegator["app.url"], delegator["check"])

@test
def check_delegated_non_dd_fix_non_dd(request, delegator, fix_non_dd):
    print(delegator["app.url"], delegator["check"], fix_non_dd)

@test
def check_delegated_non_dd_fix_dd(request, delegator, fix_dd):
    print(delegator["app.url"], delegator["check"], fix_dd)

@test(drive_with=records(record(7,8), record(9,10)))
def check_delegated_dd(request, data, delegator):
    print(delegator["app.url"], delegator["check"])

@test(drive_with=records(record(1,2), record(3,4)))
def check_delegated_dd_fix_non_dd(request, data, delegator, fix_non_dd):
    print(delegator["app.url"], delegator["check"], fix_non_dd)

@test(drive_with=records(record(1,2), record(3,4)))
def check_delegated_dd_dix_dd(request, data, delegator, fix_dd):
    print(delegator["app.url"], delegator["check"], fix_dd)

@test(drive_with=records(record(1,2), record(3,4)))
def check_delegated_dd_fix_dd_delegator(request, data, fix_dd_delegator):
    print(fix_dd_delegator)
    print(fix_dd_delegator[0]["app.url"], fix_dd_delegator[0]["check"], fix_dd_delegator[1])