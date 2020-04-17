from arjuna import *

@for_test
def res(request):
    yield request.data.run_config['app.url'], request.data.run_config['check']

@test(delegate=True)
def check_delegated_non_dd(request, res):
    print(res)

@test(drive_with=records(record(1,2), record(3,4)), delegate=True)
def check_delegated_dd(request, data, res):
    print(res)