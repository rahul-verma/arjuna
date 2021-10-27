from arjuna import *
import requests
import random
import uuid
import copy

@test
def check_msg_seq_with_raw_requests(request):
    narada = requests.session()

    item = {
        "name": str(uuid.uuid4()),
        "price": random.randint(100,500)
    }

    response = narada.post("http://localhost:9000/ditem", json=item)
    assert response.status_code == 200

    iid = response.json()['iid']

    response = narada.get(f"http://localhost:9000/ditem/{iid}")
    assert response.status_code == 200

    updated_item = copy.deepcopy(item)
    updated_item['iid'] = iid
    assert response.json() == updated_item