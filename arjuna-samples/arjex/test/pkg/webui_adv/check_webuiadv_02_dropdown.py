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
def check_dropdown_coded(request, logged_in_wordpress):
    wordpress = logged_in_wordpress
    wordpress.element(link="Settings").click()

    role_select = wordpress.dropdown(id="default_role")

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
def check_dropdown_coded_using_locate(request, logged_in_wordpress):
    wordpress = logged_in_wordpress
    wordpress.element(link="Settings").click()

    role_select = wordpress.locate(GuiWidgetDefinition(type="dropdown", id="default_role"))

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