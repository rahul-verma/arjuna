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


@for_module
def wordpress(request):
    # Setup
    wordpress = WordPress(section_dir="dyn")
    home = wordpress.launch()
    yield home

    # Teadown
    wordpress.quit()

@for_module
def dashboard(request):
    # Setup
    wordpress = WordPress(section_dir="dyn")
    home = wordpress.launch()
    dashboard = home.login_with_default_creds()
    yield dashboard

    # Teadown
    dashboard.top_nav.logout()
    wordpress.quit()

@test
def check_fmt_gns(request, dashboard):
    dashboard.left_nav.gns.formatter(text="Media").dyn_link.click()

@test
def check_fmt_config_gns(request, dashboard):
    dashboard.left_nav.gns.dyn_link_conf.click()

@test
def check_fmt_reference_gns(request, dashboard):
    dashboard.left_nav.gns.dyn_link_ref.click()

@test
def check_fmt_reference_l10n_gns(request, dashboard):
    dashboard.left_nav.gns.dyn_link_l10n.click()

@test
def check_fmt_gns_node(request, wordpress):
    e = wordpress.gns.formatter(idx="er_l").user_node_f1
    print(e.source.content.root)

    e = wordpress.gns.formatter(attr='id', idx="er_l").user_node_f2
    print(e.source.content.root)

    # Case insensitive
    e = wordpress.gns.formatter(ATTR1='id', idx="er_l", attr2='size', sz=20).user_node_f3
    print(e.source.content.root)

    e = wordpress.gns.formatter(tg="input", attr1='id', idx="er_l", attr2='size', sz=20).user_node_f4
    print(e.source.content.root)

    e = wordpress.gns.formatter(tg="html", cl1='locale-en-us', text='Me').body_node_1
    print(e.source.content.root)

    e = wordpress.gns.formatter(tg="html", cl1='locale-en-us', text='Me').body_node_2
    print(e.source.content.root)
