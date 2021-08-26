# This file is a part of Arjuna
# Copyright 2015-2021 Rahul Verma

# Website: www.RahulVerma.net

# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at

#   http://www.apache.org/licenses/LICENSE-2.0

# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

# The tests are based on tests for requests library in https://github.com/psf/requests

import io

from arjuna import *

@test
def check_action_01_msg_sequence(request, narada):
    name = Random.ustr()
    content = {'name': name, 'price': 1}
    narada.message.items.send()
    narada.message.item_post.send(name=content['name'], price=content['price'])
    narada.message.non_empty_items.send()
    narada.message.item_get.send(id=name, name=content['name'], price=content['price'])

@test
def check_action_02_from_file(request, narada):
    name = Random.ustr()
    content = {'name': name, 'price': 1}
    narada.action.post_item_coded_data.perform(id=name, name=content['name'], price=content['price'])

@test
def check_action_03_from_file(request, narada):
    narada.action.post_item_data_gen.perform()

@test
def check_action_04_msg_sequence_bulk(request, narada):
    name = Random.ustr()
    content = {'name': name, 'price': 1}
    narada.message.items.send()
    narada.message.item_post_bulk.send(content=content)
    narada.message.non_empty_items.send()
    narada.message.item_get_bulk.send(id=name, content=content)

@test
def check_action_05_from_file(request, narada):
    narada.action.post_item_data_entity.perform()