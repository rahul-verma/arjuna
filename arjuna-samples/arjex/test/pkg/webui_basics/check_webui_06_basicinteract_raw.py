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
def check_wp_login(request, wordpress):
    '''
        For this test:
        Wordpress related user options have been added to the project.yaml
        You should replace the details with those corresponding to your own deployment of WordPress.
        user_options {
	        wp.app.url = "IP address"
	        wp.login.url = ${user_options.wp.app.url}"/wp-admin"
	        wp.logout.url = ${user_options.wp.app.url}"/wp-login.php?action=logout"

            wp.admin {
                name = "<username>"
                pwd = "<password>"
            }
        }
    '''

    user = C("wp.admin.name")
    pwd = C("wp.admin.pwd")
    
    # Login
    user_field = wordpress.element(id="user_login")
    user_field.double_click()
    user_field.text = user

    pwd_field = wordpress.element(id="user_pass")
    pwd_field.text = pwd

    submit = wordpress.element(id="wp-submit")
    submit.click()

    wordpress.element(classes="welcome-view-site")

    # Logout
    url = C("wp.logout.url")
    wordpress.go_to_url(url)

    confirmation = wordpress.element(link="log out")
    confirmation.click()

    wordpress.element(text="logged out")


@test
def check_double_click(request):
    sample = GuiApp()
    sample.launch(blank_slate=True)
    sample.go_to_url("https://www.journaldev.com/wp-content/uploads/jquery/jQuery-double-click-event.html")
    import time
    for i in range(5):
        orig_element = sample.element(classes="divClass1")
        orig_element.double_click()
        time.sleep(2)
        new_elem = sample.element(classes="divClass2")
        new_elem.double_click()  
        time.sleep(2) 
    sample.quit()

