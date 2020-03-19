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

@for_test
def wordpress(request):
    # Setup
    wp_url = C("wp.login.url")
    wordpress = WebApp(base_url=wp_url, label="ArjunaExtended")
    wordpress.launch()
    yield wordpress

    # Teadown
    wordpress.quit()

@test
def check_arjuna_exts(request, wordpress):

    # Based on partial text
    element = wordpress.gns.lost_pass_text

    # Based on Full Text
    element = wordpress.gns.lost_pass_ftext

    # Based on Title
    element = wordpress.gns.lost_pass_title

    # Based on Value
    element = wordpress.gns.user_value

    # Based on partial match of content of an attribute
    element = wordpress.gns.user_attr

    # Based on full match of an attribute
    element = wordpress.gns.user_fattr

    # Based on element type
    element = wordpress.gns.pass_type

    # Based on compound classes
    element = wordpress.gns.button_classes_str
    element = wordpress.gns.button_classes_list

    # Based on Point (location in terms of X,Y co-ordinates)
    element = wordpress.gns.elem_xy

    # With Javascript
    element = wordpress.gns.elem_js