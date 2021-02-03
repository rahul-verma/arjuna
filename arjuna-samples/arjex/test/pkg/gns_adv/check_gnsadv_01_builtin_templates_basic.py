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

from arjex.lib.gns_adv.app.wp import WordPress

@for_test
def logged_in_wordpress_app(request):
    wordpress = WordPress()
    wordpress.login()
    yield wordpress

    # Teadown
    wordpress.logout()

@test
def check_multielement_coded(request, logged_in_wordpress_app):
    wordpress = logged_in_wordpress_app
    wordpress.gns.posts.click()
    wordpress.gns.categories.click()

    check_boxes = wordpress.gns.cat_checkboxes
    check_boxes[1].check()
    check_boxes[1].uncheck()
    check_boxes.first_element.uncheck()
    check_boxes.last_element.uncheck()
    check_boxes.random_element.uncheck()


@test
def check_dropdown(request, logged_in_wordpress_app):
    wordpress = logged_in_wordpress_app
    wordpress.gns.settings.click()

    role_select = wordpress.gns.role

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
def check_radiogroup(request, logged_in_wordpress_app):
    wordpress = logged_in_wordpress_app
    wordpress.gns.settings.click()

    date_format = wordpress.gns.date_format

    fmsg = "Failed to select m/d/Y date format"
    request.asserter.assert_true(date_format.has_value_selected("m/d/Y"), fmsg)
    request.asserter.assert_true(date_format.has_index_selected(2), fmsg)
    request.asserter.assert_equal(date_format.value, "m/d/Y", "Unpexpected Value attribute of Date Format")

    date_format.select_value(r"\c\u\s\t\o\m")
    date_format.select_index(2)