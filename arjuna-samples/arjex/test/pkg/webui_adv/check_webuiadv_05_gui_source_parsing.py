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
def check_parse_gui_source(request, wordpress):
    root = wordpress.source.node

    # Find first node by tag
    print(root.find(Xml.node_locator(tags="input")))

    # Find first node by attr
    print(root.find(Xml.node_locator(value="1")))

    # Find first node by tag and attr
    print(root.find(Xml.node_locator(tags="input", size="20")))

    # Find first node by tag and multiple attrs
    print(root.find(Xml.node_locator(tags="input", size="20", name="log")))

    # Find first node with xpath
    user = root.find_with_xpath("//input")
    print(user)

    # Find nth node with xpath
    submit = root.find_with_xpath("//input", 3)
    print(submit)

    # Inquiring
    link = root.find(Xml.node_locator(tags="a"))
    print(link)
    print(link.text)
    print(link.tag)
    print(link.attrs)
    print(link.attr("href"))
    print(link.has_attr("href"))
    print(link.has_attr("nothing"))

    form = root.find(Xml.node_locator(tags="form"))
    print(form.text)
    print(form.texts)
    print(form.parent)
    for child in form.children:
        print(child)

    redirect = root.find(Xml.node_locator(name="redirect_to"))
    print(redirect.preceding_sibling)
    print(redirect.following_sibling)

    # Find all nodes for a locator
    inputs = root.findall(Xml.node_locator(tags="input", size="20"))
    for i in inputs:
        print(i)

    # Find all with xpath
    inputs = root.findall_with_xpath("//input")
    for i in inputs:
        print(i)

    # Nested Node finding.
    form = root.find(Xml.node_locator(tags="form"))
    print(form.find(Xml.node_locator(type="hidden")))



