from arjuna import *

@for_module
def module_resource(request):
    d = {'a' : 1}

    yield d

    del d['a']
    assert d == {}

@for_module
def httpbin(request):
    yield Http.session(url="http://httpbin.org")

@for_module
def httpsbin(request):
    yield Http.session(url="https://httpbin.org")