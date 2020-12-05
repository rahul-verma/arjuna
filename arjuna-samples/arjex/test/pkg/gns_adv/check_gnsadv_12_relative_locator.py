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


from arjex.lib.gns_adv.app_page_section.app import WordPress

@for_test
def home(request):
    # Setup
    wordpress = WordPress(section_dir="simple")
    home = wordpress.launch()
    yield home

    # Teadown
    wordpress.quit()

@for_module
def dashboard(request):
    # Setup
    wordpress = WordPress(section_dir="simple")
    home = wordpress.launch()
    dashboard = home.login_with_default_creds()
    yield dashboard

    # Teadown
    dashboard.top_nav.logout()
    wordpress.quit()

@test
def check_relative_locators_gns_basic_find(request, home):
    e = home.element(tags="input", below=home.gns.user_label)
    print(e.source.content.all)
    e = home.gns.rel_input_1
    print(e.source.content.all)

@test
def check_relative_locators_gns_widget(request, home):
    raise Exception("Not supported yet. Relations can only use labels in GNS.")

@test
def check_relative_locators_gns_chain(request, home):
    e = home.gns.rel_input_chain
    print(e.source.content.all)


@test
def check_relative_locators_gns_find_all(request, home):
    user_label = home.multi_element(tags="*", below=home.gns.user_label)
    print(user_label.source.content.all) 
    elems = home.gns.rel_all_1
    for e in elems:
        print(e.source.content.root)  

@test
def check_relative_locators_gns_or(request, home):
    e = home.gns.rel_or
    print(e.source.content.all) 

@test
def check_relative_locators_gns_table_find(request, dashboard):
    pages = dashboard.left_nav.pages_page
    # test1 = pages.gns.formatter(text="Test1").page_name
    # date_col = pages.gns.formatter(col="date").column
    test1_date = pages.gns.published
    print(test1_date.source.content.all)

    elems = pages.gns.dates.elements
    for e in elems:
        print(e.source.content.all)  

@test
def check_relative_locators_gns_formatter(request, dashboard):
    pages = dashboard.left_nav.pages_page
    test1_date = pages.gns.formatter(ltext="Test1", col="date").published_dyn
    print(test1_date.source.content.all)


@test
def check_relative_locators_gns_nested(request, home):
    # Locate the form and then all input elements

    # Level 1 - Element in App
    form = home.gns.login_form

    # Level 2 - Element in Element
    e = form.gns.sbutton
    print(e.source.content.all)

    # Level 2 -MultiElement in Element
    labels = form.gns.labels

    for label in labels:
        print(label.text)
        print(label.source.content.all)

        # Level 3 - Element in Partial Element
        i = label.gns.input
        print(i.source.content.all)




