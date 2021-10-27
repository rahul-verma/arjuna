from arjuna import *
from arjex_seamful_demo.lib.hook.entity import Item

@for_test
def narada(request):
    yield Http.service(name="narada", url=C("narada.host.url"), request_content_handler=Http.content.json)

@for_test
def item(request):
    yield Item()


