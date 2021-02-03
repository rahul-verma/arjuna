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

@test
def check_fmt_coded(request, logged_in_wordpress):
    logged_in_wordpress.formatter(text="Media").element(link="$text$").click()

@test
def check_fmt_config_coded(request, logged_in_wordpress):
    logged_in_wordpress.element(link="$C.link.name$").click()

@test
def check_fmt_reference_coded(request, logged_in_wordpress):
    logged_in_wordpress.element(link="$R.links.test1.navlink$").click()

@test
def check_fmt_reference_l10n_coded(request, logged_in_wordpress):
    logged_in_wordpress.element(link="$L.links.posting$").click()

@test
def check_fmt_coded_fmt_locate(request, logged_in_wordpress):
    logged_in_wordpress.formatter(text="Media").locate(link="$text$").click()

@test
def check_fmt_config_coded_locate(request, logged_in_wordpress):
    logged_in_wordpress.locate(GuiWidgetDefinition(link="$C.link.name$")).click()

@test
def check_fmt_reference_coded_locate(request, logged_in_wordpress):
    logged_in_wordpress.locate(GuiWidgetDefinition(link="$R.links.test1.navlink$")).click()

@test
def check_fmt_reference_l10n_coded_locate(request, logged_in_wordpress):
    logged_in_wordpress.locate(GuiWidgetDefinition(link="$L.links.posting$")).click()


# Node formatting

@test
def check_fmt_node_coded(request, wordpress):
    e = wordpress.formatter(idx="er_l").element(node=node(id="$idx$"))
    print(e.source.content.root)

    e = wordpress.formatter(idx="er_l").locate(node=node(id="$idx$"))

    # Key and value formatting
    e = wordpress.formatter(attr='id', idx="er_l").element(node=node(attrs={'$attr$': "$idx$"}))
    print(e.source.content.root)

    # Multiple attribute
    e = wordpress.formatter(idx="er_l", sz=20).element(node=node(id="$idx$", size="$sz$"))
    print(e.source.content.root)

    e = wordpress.formatter(idx="er_l", sz=20).locate(node=node(id="$idx$", size="$sz$"))

    # Key and value formatting
    e = wordpress.formatter(attr1='id', idx="er_l", attr2='size', sz=20).element(node=node(attrs={'$attr1$': "$idx$", '$attr2$': "$sz$"}))
    print(e.source.content.root)

    # Multiple attribute and tag
    e = wordpress.formatter(tg="input", idx="er_l", sz=20).element(node=node(tags="$tg$", id="$idx$", size="$sz$"))
    print(e.source.content.root)

    e = wordpress.formatter(tg="input", idx="er_l", sz=20).element(node=node(tags="$tg$", id="$idx$", size="$sz$"))

    # Key and value formatting
    e = wordpress.formatter(tg="input", attr1='id', idx="er_l", attr2='size', sz=20).element(node=node(tags="$tg$", attrs={'$attr1$': "$idx$", '$attr2$': "$sz$"}))
    print(e.source.content.root)

    e = wordpress.formatter(tg="input", attr1='id', idx="er_l", attr2='size', sz=20).element(node=node(attrs={'tags':"$tg$", '$attr1$': "$idx$", '$attr2$': "$sz$"}))
    print(e.source.content.root)

    e = wordpress.formatter(tg="html", cl1='locale-en-us', text='Me').element(node=node(tags="$tg$ *", classes=("$cl1$", "wp-core-ui"), attrs={'.text' : "$text$"}))
    print(e.source.content.root)