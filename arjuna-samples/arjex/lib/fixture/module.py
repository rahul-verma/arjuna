from arjuna import *

@for_module
def module_resource(request):
    d = {'a' : 1}

    yield d

    del d['a']
    assert d == {}