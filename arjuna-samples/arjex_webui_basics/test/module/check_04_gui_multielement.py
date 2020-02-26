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
def check_multielement(request, wordpress):
    wordpress.element(With.link("Posts")).click()
    wordpress.element(With.link("Categories")).click()

    check_boxes = wordpress.multi_element(With.name("delete_tags[]"))
    check_boxes[1].check()
    check_boxes[1].uncheck()
    check_boxes.first_element.uncheck()
    check_boxes.last_element.uncheck()
    check_boxes.random_element.uncheck()
