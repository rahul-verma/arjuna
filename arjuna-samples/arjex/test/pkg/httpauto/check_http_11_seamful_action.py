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
from arjex.lib.hook.entity import Item


@for_test(default=True)
def items(request, narada):
    yield
    narada.delete("/items")


@test
def check_action_01_action_blank(request, narada):
    narada.perform()


@test
def check_action_01_msg_individual_vals(request, narada):
    '''
    Try out formatting with independently passed attributes.
    '''
    name = Random.ustr()
    input_dict = {'name': name, 'price': 1}
    narada.message.items.send()
    narada.message.item_post_1.send(name=input_dict['name'], price=input_dict['price'])
    narada.message.non_empty_items.send()
    narada.message.item_get_1.send(name=input_dict['name'], price=input_dict['price'])

@test
def check_action_01_action_individual_vals_1(request, narada):
    name = Random.ustr()
    input_dict = {'name': name, 'price': 1}
    narada.action.post_item_coded_data_1.perform(name=input_dict['name'], price=input_dict['price'])

@test
def check_action_01_action_individual_vals_2_flattendict(request, narada):
    name = Random.ustr()
    input_dict = {'name': name, 'price': 1}
    narada.action.post_item_coded_data_1.perform(**input_dict)

@test
def check_action_01_action_individual_vals_3_flattenentity(request, narada):
    narada.action.post_item_coded_data_1.perform(**Item())

@test
def check_action_01_action_individual_vals_filedata_gen_loader(request, narada):
    narada.action.post_item_data_gen_2.perform()

@test
def check_action_01_msg_additional_id(request, narada):
    '''
    Try out formatting with independently passed attributes.
    '''
    name = Random.ustr()
    input_dict = {'name': name, 'price': 1}
    narada.message.items.send()
    narada.message.item_post_1.send(name=input_dict['name'], price=input_dict['price'])
    narada.message.non_empty_items.send()
    narada.message.item_get_1_1.send(id=name, name=input_dict['name'], price=input_dict['price'])

@test
def check_action_01_action_individual_vals_filedata_gen_alias_section(request, narada):
    narada.action.post_item_data_gen_3.perform()

@test
def check_action_02_msg_data_construct_with_dict(request, narada):
    '''
    Try out formatting with independently passed attributes.
    '''
    name = Random.ustr()
    input_dict = {'name': name, 'price': 1}
    narada.message.items.send()
    narada.message.item_post_2.send(data=input_dict)
    narada.message.non_empty_items.send()
    narada.message.item_get_2.send(data=input_dict)

@test
def check_action_02_action_data_construct_with_dict(request, narada):
    name = Random.ustr()
    input_dict = {'name': name, 'price': 1}
    narada.action.post_item_coded_data_2.perform(data=input_dict)

@test
def check_action_03_msg_data_construct_with_entity(request, narada):
    item = Item()
    narada.message.items.send()
    narada.message.item_post_2.send(data=item)
    narada.message.non_empty_items.send()
    narada.message.item_get_2.send(data=item)

@test
def check_action_03_action_data_construct_with_entity(request, narada):
    narada.action.post_item_coded_data_2.perform(data=Item())

@test
def check_action_04_msg_bulk_using_dict(request, narada):
    '''
    Try out formatting with independently passed attributes.
    '''
    name = Random.ustr()
    input_dict = {'name': name, 'price': 1}
    narada.message.items.send()
    narada.message.item_post_3.send(data=input_dict)
    narada.message.non_empty_items.send()
    narada.message.item_get_3.send(data=input_dict)

@test
def check_action_04_msg_bulk_using_entity(request, narada):
    '''
    Try out formatting with independently passed attributes.
    '''
    item = Item()
    narada.message.items.send()
    narada.message.item_post_3.send(data=item)
    narada.message.non_empty_items.send()
    narada.message.item_get_3.send(data=item)

@test
def check_action_04_action_bulk_using_dict(request, narada):
    name = Random.ustr()
    input_dict = {'name': name, 'price': 1}
    narada.action.post_item_coded_data_3.perform(data=input_dict)

@test
def check_action_04_action_coded_bulk_using_entity(request, narada):
    narada.action.post_item_coded_data_3.perform(data=Item())

@test
def check_action_04_msg_bulk_using_entity_other_name(request, narada):
    '''
    Try out formatting with independently passed attributes.
    '''
    item = Item()
    narada.message.items.send()
    narada.message.item_post_4.send(item=item)
    narada.message.non_empty_items.send()
    narada.message.item_get_5.send(item=item)

@test
def check_action_04_action_infile_bulk_using_entity(request, narada):
    narada.action.post_item_data_entity_1.perform()

@test
def check_action_05_msg_mixed_entity_and_other(request, narada):
    '''
    Try out formatting with independently passed attributes.
    '''
    item = Item()
    narada.message.items.send()
    narada.message.item_post_4.send(item=item)
    narada.message.non_empty_items.send()
    narada.message.item_get_6.send(id=item.name, item=item)

@test
def check_action_05_action_mixed_entity_and_other(request, narada):
    item = Item()
    narada.action.post_item_data_entity_2.perform()

@test
def check_action_05_action_mixed_dynamic_entity_and_other(request, narada):
    item = Item()
    narada.action.post_item_data_entity_3.perform()

@test
def check_action_06_action_responses(request, narada):
    responses = narada.action.post_item_coded_data_1.perform(**Item())
    for response in responses:
        print(response)

@test
def check_action_06_action_store(request, narada):
    responses = narada.action.post_item_coded_data_1.perform(**Item())
    for response in responses:
        print(response.response.store)

@test
def check_action_07_dynamic(request, narada):
    narada.action.get_inc_1.perform(value=5)

@test
def check_action_07_msg2datainmsg2(request, narada):
    narada.action.ditem_create.perform()