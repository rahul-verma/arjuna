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

from arjuna import *
from arjex.lib.gns_adv.app_page_section.app import WordPress

@for_test
def dashboard(request):
    # Setup
    wordpress = WordPress(section_dir="withx")
    home = wordpress.launch()
    dashboard = home.login_with_default_creds()
    yield dashboard

    # Teadown
    dashboard.top_nav.logout()
    wordpress.quit()

@for_test
def wordpress(request):
    # Setup
    wordpress = WordPress(section_dir="withx")
    home = wordpress.launch()
    yield home

    # Teadown
    wordpress.quit()

@test
def check_withx_in_leftnav_gns_file(request, dashboard):
    dashboard.left_nav.gns.first_steps.click()
    dashboard.browser.go_back()

    dashboard.left_nav.gns.posts.click()
    dashboard.left_nav.gns.media.click()
    dashboard.left_nav.gns.pages.click()
    dashboard.left_nav.gns.comments.click()

@test
def check_withx_gns_home_named(request, wordpress):
    e = wordpress.gns.user_node_with1
    print(e.source.content.root)

    e = wordpress.gns.user_node_with2
    print(e.source.content.root)

    e = wordpress.gns.user_node_with3
    print(e.source.content.root)

    e = wordpress.gns.formatter(val2=20).user_node_with4
    print(e.source.content.root)

    e = wordpress.gns.formatter(val2=20).user_node_with4
    print(e.source.content.root)

    e = wordpress.gns.body_node_with_1
    print(e.source.content.root)

    e = wordpress.gns.formatter(text='Me').body_node_with_2
    print(e.source.content.root)

@test
def check_withx_gns_home_positional(request, wordpress):

    e = wordpress.gns.pos_single
    print(e.source.content.root)

    e = wordpress.gns.pos_multi_submit
    print(e.source.content.root)

    e = wordpress.gns.pos_multi_label
    print(e.source.content.root)

    e = wordpress.gns.pos_multi_user_field
    print(e.source.content.root)

    e = wordpress.gns.pos_multi_submit_2
    print(e.source.content.root)