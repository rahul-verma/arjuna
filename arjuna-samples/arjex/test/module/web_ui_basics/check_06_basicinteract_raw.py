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
    wordpress = WebApp(base_url=wp_url, label="WordPress")
    wordpress.launch()
    yield wordpress

    # Teadown
    wordpress.quit()

@test
def check_wp_login(request, wordpress):
    '''
        For this test:
        Wordpress related user options have been added to the project.conf
        You should replace the details with those corresponding to your own deployment of WordPress.
        userOptions {
	        wp.app.url = "IP address"
	        wp.login.url = ${userOptions.wp.app.url}"/wp-admin"
	        wp.logout.url = ${userOptions.wp.app.url}"/wp-login.php?action=logout"

            wp.admin {
                name = "<username>"
                pwd = "<password>"
            }
        }
    '''

    user = C("wp.admin.name")
    pwd = C("wp.admin.pwd")
    
    # Login
    user_field = wordpress.gns.user
    user_field.text = user

    pwd_field = wordpress.gns.pwd
    pwd_field.text = pwd

    submit = wordpress.gns.submit
    submit.click()

    wordpress.gns.view_site

    # Logout
    url = C("wp.logout.url")
    wordpress.go_to_url(url)

    confirmation = wordpress.gns.logout_confirm
    confirmation.click()

    wordpress.gns.logout_msg
