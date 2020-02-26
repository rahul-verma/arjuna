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
def check_dropdown(request, wordpress):
    wordpress.element(With.link("Settings")).click()

    role_select = wordpress.dropdown(With.id("default_role"))

    role_select.select_text("Subscriber")
    fmsg = "Failed to select Subscriber Role"
    request.asserter.assert_true(role_select.has_visible_text_selected("Subscriber"), fmsg)
    request.asserter.assert_true(role_select.has_value_selected("subscriber"), fmsg)
    request.asserter.assert_true(role_select.has_index_selected(0), fmsg)
    request.asserter.assert_equal(role_select.value, "subscriber", "Unexpected Value attribute of Role.")
    request.asserter.assert_equal(role_select.text,"Subscriber",  "Unexpected Selected Role Text ")

    role_select.select_value("editor")
    role_select.select_index(4)
    role_select.text = "Subscriber"


@test
def check_radiogroup(request, wordpress):
    wordpress.element(With.link("Settings")).click()

    date_format = wordpress.radio_group(With.name("date_format"))

    fmsg = "Failed to select m/d/Y date format"
    request.asserter.assert_true(date_format.has_value_selected("m/d/Y"), fmsg)
    request.asserter.assert_true(date_format.has_index_selected(2), fmsg)
    request.asserter.assert_equal(date_format.value, "m/d/Y", "Unpexpected Value attribute of Date Format")

    date_format.select_value(r"\c\u\s\t\o\m")
    date_format.select_index(2)