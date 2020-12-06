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
    wp = WordPress(section_dir="simple")
    home = wp.launch()
    yield home

    # Teadown
    wp.quit()

@test
def check_filters_gns_element_pos(request, home):
    elem = home.gns.epos_1
    print(elem.source.content.root)
    elem = home.gns.epos_2
    print(elem.source.content.root)
    elem = home.gns.epos_3
    print(elem.source.content.root)
    elem = home.gns.epos_4
    print(elem.source.content.root)
    elem = home.gns.epos_5
    print(elem.source.content.root)
    elem = home.gns.epos_6
    print(elem.source.content.root)

@test
def check_filters_gns_multielement_pos(request, home):
    elems = home.gns.mepos_1
    print("!!!!", elems.source.content.root)
    elems = home.gns.mepos_2
    print("!!!!", elems.source.content.root)
    elems = home.gns.mepos_3
    print("!!!!", elems.source.content.root)
    elems = home.gns.mepos_4
    print("!!!!", elems.source.content.root)
    elems = home.gns.mepos_5
    print("!!!!", elems.source.content.root)
    elems = home.gns.mepos_6
    print("!!!!", elems.source.content.root)
    elems = home.gns.mepos_7
    print("!!!!", elems.source.content.root)
    elems = home.gns.mepos_8
    print("!!!!", elems.source.content.root)
    elems = home.gns.mepos_9
    print("!!!!", elems.source.content.root)
    elems = home.gns.mepos_10
    print("!!!!", elems.source.content.root)
    elems = home.gns.mepos_11
    print("!!!!", elems.source.content.root)

@test
def check_filters_gns_element_nested_pos(request, home):
    form = home.element(tags="form")
    elem = form.gns.epos_nested
    print("!!!!", elem.source.content.all)
    elem = form.gns.mepos_nested
    print("!!!!", elem.source.content.all)