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
def check_arjuna_exts_coded(request, wordpress):

    # Based on partial text
    wordpress.element(text="your") 

    # Based on Full Text
    wordpress.element(ftext="Lost your password?") 

    # Based on Full Text
    wordpress.element(btext="Lost your") 

    # Based on Title
    wordpress.element(title="Password Lost and Found")

    # Based on Value
    wordpress.element(value="Log In")

    # Based on partial match of content of an attribute
    wordpress.element(attr=attr("for", "er_l"))

    # Based on full match of an attribute
    wordpress.element(fattr=attr("for", "user_login"))

    # Based on full match of an attribute
    wordpress.element(battr=attr("for", "user_"))

    # Based on full match of an attribute
    wordpress.element(eattr=attr("for", "_login"))

    # Based on compound classes
    wordpress.element(classes="button button-large")
    wordpress.element(classes=("button", "button-large"))

    # Based on Point (location in terms of X,Y co-ordinates)
    wordpress.element(point=Point(1043, 458))

    # With Javascript
    wordpress.element(js="return document.getElementById('wp-submit')")

    # With.NODE
    # Based on node (partial matches of attrs and tag)
    e = wordpress.element(node=node(id="er_l"))
    print(e.source.content.root)

    e = wordpress.element(node=node(tag="input", id="er_l"))
    print(e.source.content.root)

    e = wordpress.element(node=node(tag="input", id="er_l", size=20))
    print(e.source.content.root)

    e = wordpress.element(node=node(attrs={'for': 'er_l'}))
    print(e.source.content.root)

    # Direct args update attrs dict
    e = wordpress.element(node=node(id="er_l", attrs={'id': "wrong"}))
    print(e.source.content.root)

    # With.BNODE
    # Based on node (partial matches at beginning of attrs and tag)
    e = wordpress.element(node=node(id="user_"))
    print(e.source.content.root)

    e = wordpress.element(node=node(tag="input", id="user_"))
    print(e.source.content.root)

    e = wordpress.element(node=node(tag="input", id="user_", size=20))
    print(e.source.content.root)

    e = wordpress.element(node=node(attrs={'for': 'user_'}))
    print(e.source.content.root)

    # Direct args update attrs dict
    e = wordpress.element(node=node(id="user_", attrs={'id': "wrong"}))
    print(e.source.content.root)

    # With.FNODE
    # Based on full node (full match of attrs and tag)
    e = wordpress.element(fnode=node(id="user_login"))
    print(e.source.content.root)

    e = wordpress.element(fnode=node(tag="input", id="user_login"))
    print(e.source.content.root)

    e = wordpress.element(fnode=node(tag="input", id="user_login", size=20))
    print(e.source.content.root)

    e = wordpress.element(fnode=node(attrs={'for': 'user_login'}))
    print(e.source.content.root)

    # Direct args update attrs dict
    e = wordpress.element(fnode=node(id="user_login", attrs={'id': "wrong"}))
    print(e.source.content.root)

    # With.BNODE
    # Based on full node (full match of attrs and tag)
    e = wordpress.element(bnode=node(id="user_"))
    print(e.source.content.root)

    e = wordpress.element(bnode=node(tag="input", id="user_"))
    print(e.source.content.root)

    e = wordpress.element(bnode=node(tag="input", id="user_", size=20))
    print(e.source.content.root)

    e = wordpress.element(bnode=node(attrs={'for': 'user_'}))
    print(e.source.content.root)

    # Direct args update attrs dict
    e = wordpress.element(bnode=node(id="user_", attrs={'id': "wrong"}))
    print(e.source.content.root)

    # Using node with tag, attrs and text
    e = wordpress.element(node=node(tag="a", text="Lost", href="lostpassword", title="Found"))
    print(e.source.content.root)
