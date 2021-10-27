from arjuna import *

@test
def check_arjuna_msg_seq(request, narada, item):
    response = narada.message.ditem_post.send(item=item)
    narada.message.ditem_get.send(iid=response.store.iid, item=item)

