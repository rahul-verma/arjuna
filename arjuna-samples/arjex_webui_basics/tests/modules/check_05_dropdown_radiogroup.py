'''
This file is a part of Arjuna
Copyright 2015-2020 Rahul Verma

Website: www.RahulVerma.net

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

  http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
'''

from arjuna import *
from arjex_webui_basics.lib.wp import *

@for_test
def wordpress(request):
    # Setup
    wordpress = create_wordpress_app()
    login(wordpress)
    yield wordpress

    # Teadown
    logout(wordpress)

@test
def test_dropdown(my, request, wordpress):
    wordpress.element(With.link("Settings")).click()

    role_select = wordpress.dropdown(With.id("default_role"))

    role_select.select_text("Subscriber")
    context = "Selection of Subscriber Role"
    my.asserter.assert_true(role_select.has_visible_text_selected("Subscriber"), context)
    my.asserter.assert_true(role_select.has_value_selected("subscriber"), context)
    my.asserter.assert_true(role_select.has_index_selected(0), context)
    my.asserter.assert_equal(role_select.value, "subscriber", "Value attribute of Role")
    my.asserter.assert_equal(role_select.text,"Subscriber",  "Selected Role Text")

    role_select.select_value("editor")
    role_select.select_index(4)
    role_select.text = "Subscriber"


@test
def test_radiogroup(my, request, wordpress):
    wordpress.element(With.link("Settings")).click()

    date_format = wordpress.radio_group(With.name("date_format"))

    context = "Selection of m/d/Y date format"
    my.asserter.assert_true(date_format.has_value_selected("m/d/Y"), context)
    my.asserter.assert_true(date_format.has_index_selected(2), context)
    my.asserter.assert_equal(date_format.value, "m/d/Y", "Value attribute of Date Format")

    date_format.select_value(r"\c\u\s\t\o\m")
    date_format.select_index(2)