# This file is a part of Arjuna
# Copyright 2015-2020 Rahul Verma

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

from arjuna import *

def print_source_info(source):
    print("Root:", source.content.root)
    print("All:", source.content.all)
    print("Inner HTML:", source.content.inner)
    print("Text:",source.content.text)	

@test
def check_current_page_source(request, wordpress):
    print_source_info(wordpress.source)

@test
def check_element_source(request, wordpress):
    node = Html.from_str("<p>abc</p>", partial=True)
    print(node.normalized_text)
    user_box = wordpress.element(attr=NVPair("for","user_login"))
    print(user_box.text)
    print_source_info(user_box.source)


@test
def check_multi_element_source(request, wordpress):
    labels = wordpress.multi_element(tag="label")
    print_source_info(labels.source)


@test
def check_dropdown_source(request, logged_in_wordpress):
    wordpress = logged_in_wordpress
    wordpress.element(link="Settings").click()
    role = wordpress.dropdown(id="default_role")
    print_source_info(role.source)


@test
def check_radio_group_source(request, logged_in_wordpress):
    wordpress = logged_in_wordpress
    wordpress.element(link="Settings").click()
    date_format = wordpress.radio_group(name="date_format")
    print_source_info(date_format.source)
