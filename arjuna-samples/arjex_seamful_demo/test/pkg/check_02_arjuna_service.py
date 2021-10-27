from arjuna import *

@test
def check_msg_seq_with_raw_arjuna(request, narada, item):
    response = narada.post(route="/ditem", content=item, xcodes=200)
    iid = response.json['iid']

    response = narada.get(route=f"/ditem/{iid}", xcodes=200)

    updated_item = item.as_dict()
    updated_item['iid'] = iid
    assert response.json == updated_item