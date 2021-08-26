from arjuna import *

@for_module
def module_resource(request):
    d = {'a' : 1}

    yield d

    del d['a']
    assert d == {}

@for_module
def httpbin(request):
    yield Http.service(url="http://httpbin.org")

@for_module
def httpbinseam(request):
    yield Http.service(name="httpbin", url="http://httpbin.org")

@for_module
def httpsbin(request):
    yield Http.service(url="https://httpbin.org")

@for_module
def httpsbinseam(request):
    yield Http.service(name="httpbin", url="https://httpbin.org")

@for_module
def narada(request):
    yield Http.service(name="narada", url="http://localhost:9000")