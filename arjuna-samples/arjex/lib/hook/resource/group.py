from arjuna import *

@for_group
def group_resource(request):
    d = {'a' : 1}

    yield d

    del d['a']
    assert d == {}


@for_group
def constant_int(request):
    yield 1