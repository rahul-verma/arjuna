import threading
from arjuna import *

@for_test
def res(request):
    print(threading.currentThread().getName())
    conf = request.data.run_config
    print(conf.name)
    yield conf['app.url'], conf['check']

@test(delegate=True)
def check_delegated_non_dd(request, res):
    print(threading.currentThread().getName())
    print(res)

@test(drive_with=records(record(1,2), record(3,4)), delegate=True)
def check_delegated_dd(request, data, res):
    print(threading.currentThread().getName())
    print(res)