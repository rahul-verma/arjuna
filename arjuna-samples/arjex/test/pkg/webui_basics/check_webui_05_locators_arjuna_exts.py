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
def check_arjuna_exts_coded_basic(request, wordpress):

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

@test
def check_arjuna_exts_coded_attr(request, wordpress):

    # Based on partial match of content of an attribute
    wordpress.element(attr=attr(id="er_l"))
    wordpress.element(attr=attr(__for="er_l"))

    # Based on full match of an attribute
    wordpress.element(fattr=attr(__for="user_login"))

    # Based on full match of an attribute
    wordpress.element(battr=attr(__for="user_"))

    # Based on full match of an attribute
    wordpress.element(eattr=attr(__for="_login"))

@test
def check_arjuna_exts_coded_tags(request, wordpress):

    # Based on descendent tags
    wordpress.element(tags="html body form")
    wordpress.element(tags=("html", "body", "form"))
    wordpress.element(tags=("html", "body", "input"))

@test
def check_arjuna_exts_coded_classes(request, wordpress):

    # Based on compound classes
    wordpress.element(classes="button button-large")
    wordpress.element(classes=("button", "button-large"))

@test
def check_arjuna_exts_coded_point(request, wordpress):

    # Based on Point (location in terms of X,Y co-ordinates)
    wordpress.element(point=Point(1043, 458))

@test
def check_arjuna_exts_coded_js(request, wordpress):
    # With Javascript
    wordpress.element(js="return document.getElementById('wp-submit')")

@test
def check_arjuna_exts_coded_node(request, wordpress):
    # With.NODE
    # Based on node (partial matches of attrs and tag)
    e = wordpress.element(node=node(id="er_l"))
    print(e.source.content.root)

    e = wordpress.element(node=node(tags="input", id="er_l"))
    print(e.source.content.root)

    e = wordpress.element(node=node(tags="input", id="er_l"))
    print(e.source.content.root)

    e = wordpress.element(node=node(tags="form input", id="er_l"))
    print(e.source.content.root)

    e = wordpress.element(node=node(tags=('form', 'input'), id="er_l"))
    print(e.source.content.root)

    e = wordpress.element(node=node(tags="input", id="er_l", size=20))
    print(e.source.content.root)

    e = wordpress.element(node=node(attrs={'for': 'er_l'}))
    print(e.source.content.root)

    e = wordpress.element(node=node(__for='er_l'))
    print(e.source.content.root)

    e = wordpress.element(node=node(attrs={'__for': 'er_l'}))
    print(e.source.content.root)

    # Direct args update attrs dict
    e = wordpress.element(node=node(id="er_l", attrs={'id': "wrong"}))
    print(e.source.content.root)

    # With.BNODE
    # Based on node (partial matches at beginning of attrs and tag)
    e = wordpress.element(node=node(id="user_"))
    print(e.source.content.root)

    e = wordpress.element(node=node(tags="input", id="user_"))
    print(e.source.content.root)

    e = wordpress.element(node=node(tags="input", id="user_", size=20))
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

    e = wordpress.element(fnode=node(tags="input", id="user_login"))
    print(e.source.content.root)

    e = wordpress.element(fnode=node(tags="input", id="user_login", size=20))
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

    e = wordpress.element(bnode=node(tags="input", id="user_"))
    print(e.source.content.root)

    e = wordpress.element(bnode=node(tags="input", id="user_", size=20))
    print(e.source.content.root)

    e = wordpress.element(bnode=node(attrs={'for': 'user_'}))
    print(e.source.content.root)

    # Direct args update attrs dict
    e = wordpress.element(bnode=node(id="user_", attrs={'id': "wrong"}))
    print(e.source.content.root)

    # Using node with tag, attrs and text
    e = wordpress.element(node=node(tags="a", text="Lost", href="lostpassword", title="Found"))
    print(e.source.content.root)

    # Using node with star_text
    e = wordpress.element(node=node(star_text="Me"))
    print(e.source.content.root)

    e = wordpress.element(node=node(attrs={'*text' : "Me"}))
    print(e.source.content.root)

    # Using node with dot_text
    e = wordpress.element(node=node(tags="form", dot_text="Me"))
    print(e.source.content.root)

    e = wordpress.element(node=node(tags="body form", attrs={'.text' : "Me"}))
    print(e.source.content.root)

    e = wordpress.element(node=node(tags=("body", "form"), attrs={'.text' : "Me"}))
    print(e.source.content.root)

    # Using classes
    e = wordpress.element(node=node(star_text="Me", classes="forgetmenot"))
    print(e.source.content.root)

    e = wordpress.element(node=node(classes="wp-core-ui", attrs={'.text' : "Me"}))
    print(e.source.content.root)

    e = wordpress.element(node=node(classes="locale-en-us wp-core-ui", attrs={'.text' : "Me"}))
    print(e.source.content.root)

    e = wordpress.element(node=node(tags="html body", classes=("locale-en-us", "wp-core-ui")))
    print(e.source.content.root)

    e = wordpress.element(node=node(tags="html *", classes=("locale-en-us", "wp-core-ui")))
    print(e.source.content.root)

    # Enforce XPath in a situation where CSS Selector is generated by default
    e = wordpress.element(node=node(use_xpath=True, tags="html *", classes=("locale-en-us", "wp-core-ui")))
    print(e.source.content.root)

    e = wordpress.element(node=node(classes=("locale-en-us", "wp-core-ui"), attrs={'.text' : "Me"}))
    print(e.source.content.root)

    e = wordpress.element(node=node(tags="html body", classes=("locale-en-us", "wp-core-ui"), attrs={'.text' : "Me"}))
    print(e.source.content.root)

    e = wordpress.element(node=node(tags="html *", classes=("locale-en-us", "wp-core-ui"), attrs={'.text' : "Me"}))
    print(e.source.content.root)

@test
def check_arjuna_exts_coded_axes(request, wordpress):
    e = wordpress.element(axes=axes(fnode(id="user_login")).up(node(tags="label")))
    print(e.source.content.root)

    e = wordpress.element(axes=axes(node(id="er_log")).up(node(tags="label")))
    print(e.source.content.root)

    e = wordpress.element(axes=axes(bnode(id="user_l")).up(node(tags="label")))
    print(e.source.content.root)

    e = wordpress.element(axes=axes(node(id="er_l")).up(fnode(name="loginform")))
    print(e.source.content.root)

    e = wordpress.element(axes=axes(node(id="user_l")).up(node(name="infor")))
    print(e.source.content.root)

    e = wordpress.element(axes=axes(node(id="user_l")).up(bnode(name="loginf")))
    print(e.source.content.root)

    # All of them together
    e = wordpress.element(axes=axes(node(tags="html")).down(node(classes="button")).up(node(tags="form")).down(node(tags="p")).right(node(tags="p")).left(node(tags="p")).down(node(tags="input")))
    print(e.source.content.root)