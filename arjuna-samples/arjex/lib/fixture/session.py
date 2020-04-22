from arjuna import *

@for_group
def session_resource(request):
    d = {'a' : 1}

    yield d

    del d['a']
    assert d == {}