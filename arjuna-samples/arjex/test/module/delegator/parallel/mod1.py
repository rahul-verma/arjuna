from arjuna import *

@for_test
def res(request, worker_id):
    print(worker_id)
    conf = request.data.run_config
    print(conf.name)
    yield conf['app.url'], conf['check']

@test(delegate=True)
def check_delegated_non_dd(request, res, worker_id):
    print(worker_id)
    print(res)

@test(drive_with=records(record(1,2), record(3,4)), delegate=True)
def check_delegated_dd(request, data, res, worker_id):
    print(threading.currentThread().getName())
    print(res)