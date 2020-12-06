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

@test
def check_filters_coded_element_pos(request, wordpress):
    elem = wordpress.element(tags="input", pos=2)
    print(elem.source.content.all)
    elem = wordpress.element(tags="input", pos="first")
    print(elem.source.content.all)
    elem = wordpress.element(tags="input", pos="last")
    print(elem.source.content.all)
    elem = wordpress.element(tags="input", pos="random")
    print(elem.source.content.all)

    # pos as extractor objects
    elem = wordpress.element(tags="input", pos=pos.at(2))
    print(elem.source.content.all)
    elem = wordpress.element(tags="input", pos=pos.first())
    print(elem.source.content.all)
    elem = wordpress.element(tags="input", pos=pos.last())
    print(elem.source.content.all)
    elem = wordpress.element(tags="input", pos=pos.random())
    print(elem.source.content.all)

    # Meant for multiple elements, but used with element. Returns first element.
    inputs = wordpress.element(tags="*", pos=pos.at(2,4))
    print("!!!!", inputs.source.content.root)
    inputs = wordpress.element(tags="*", pos=pos.slice(2,4))
    print("!!!!", inputs.source.content.root)
    inputs = wordpress.element(tags="*", pos=pos.slice(2,7,2))
    print("!!!!", inputs.source.content.root)
    inputs = wordpress.element(tags="*", pos=pos.odd())
    print("!!!!", inputs.source.content.root)
    inputs = wordpress.element(tags="*", pos=pos.even())
    print("!!!!", inputs.source.content.root)
    elem = wordpress.element(tags="input", pos="odd")
    print(elem.source.content.all)
    elem = wordpress.element(tags="input", pos="even")
    print(elem.source.content.all)

# These are internal tests to check data types that will come from GNS
@test
def check_filters_coded_gns_data_structs(request, wordpress):
    # pos as extractor objects
    elem = wordpress.element(tags="input", pos={"at": 2})
    print(elem.source.content.all)
    elems = wordpress.multi_element(tags="*", pos={"at": [2,4]})
    print("!!!!", elems.source.content.root)

    inputs = wordpress.multi_element(tags="*", pos={"slice": {'stop': "4"}})
    print("!!!!", inputs.source.content.root)
    inputs = wordpress.multi_element(tags="*", pos={"slice": {'start': 2, 'stop': "4"}})
    print("!!!!", inputs.source.content.root)
    inputs = wordpress.multi_element(tags="*", pos={"slice": {'start':2, 'stop': "4", 'step': 2}})
    print("!!!!", inputs.source.content.root)
    elems = wordpress.multi_element(tags="input", pos={"random": {'count': "3"}})
    print("!!!!", elems.source.content.all)

@test
def check_filters_coded_multielement_pos(request, wordpress):
    elems = wordpress.multi_element(tags="*", pos=pos.at(2,4))
    print("!!!!", elems.source.content.root)
    elems = wordpress.multi_element(tags="*", pos=pos.slice(2,4))
    print("!!!!", elems.source.content.root)
    elems = wordpress.multi_element(tags="*", pos=pos.slice(2,7,2))
    print("!!!!", elems.source.content.root)
    elems = wordpress.multi_element(tags="*", pos=pos.odd())
    print("!!!!", elems.source.content.root)
    elems = wordpress.multi_element(tags="*", pos=pos.even())
    print("!!!!", elems.source.content.root)

    # # Meant for element, but used with elements. Returns object that has a single element.
    elems = wordpress.multi_element(tags="input", pos=pos.at(2))
    print("!!!!", elems.source.content.all)
    elems = wordpress.multi_element(tags="input", pos=pos.first())
    print("!!!!", elems.source.content.all)
    elems = wordpress.multi_element(tags="input", pos=pos.last())
    print("!!!!", elems.source.content.all)
    elems = wordpress.multi_element(tags="input", pos=pos.random())
    print("!!!!", elems.source.content.all)

    # Random with count of matches
    elems = wordpress.multi_element(tags="input", pos=pos.random(count=3))
    print("!!!!", elems.source.content.all)

@test
def check_filters_coded_element_nested_pos(request, wordpress):
    form = wordpress.element(tags="form")
    elem = form.element(tags="input", pos=3)
    print(elem.source.content.all)
    elem = form.element(tags="input", pos=pos.at(3))
    print(elem.source.content.all)
    inputs = form.multi_element(tags="*", pos=pos.at(2,4))
    print("!!!!", inputs.source.content.root)