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

@for_test
def wordpress(request):
    '''
        For this fixture:
        Wordpress related user options have been added to the project.conf
        You should replace the details with those corresponding to your own deployment of WordPress.
        userOptions {
	        wp.app.url = "IP address"
	        wp.login.url = ${userOptions.wp.app.url}"/wp-admin"
        }
    '''

    # Setup
    wp_url = C("wp.login.url")
    wordpress = GuiApp(base_url=wp_url, label="BasicIdentification", gns_dir="gns_basics")
    wordpress.launch()
    yield wordpress

    # Teadown
    wordpress.quit()

@test
def check_basic_identifiers(request, wordpress):
    # user name field.
    # Html of user name: <input type="text" name="log" id="user_login" class="input" value="" size="20">
    wordpress.gns.user_id
     
    element = wordpress.gns.user_name
    element = wordpress.gns.user_tag
    element = wordpress.gns.user_class

    # Lost your password link
    # Html of link: <a href="/wp-login.php?action=lostpassword" title="Password Lost and Found">Lost your password?</a>
    # Partial Link text match
    element = wordpress.gns.lost_pass_link
    # Full Link text match
    element = wordpress.gns.lost_pass_flink