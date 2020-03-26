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
    wordpress = GuiApp(base_url=wp_url, label="XPath", gns_dir="gns_basics")
    wordpress.launch()
    yield wordpress

    # Teadown
    wordpress.quit()

@test
def check_xpath(request, wordpress):
    # Based on Text
    element = wordpress.gns.lost_pass_text

    # Based on partial text
    element = wordpress.gns.lost_pass_text_content

    # Based on Title
    element = wordpress.gns.lost_pass_title

    # Based on Value
    element = wordpress.gns.user_value

    # Based on any attribute e.g. for
    element = wordpress.gns.user_attr

    # Based on partial content of an attribute
    element = wordpress.gns.user_attr_content

    # Based on element type
    element = wordpress.gns.pass_type
