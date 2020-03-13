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
def check_wp_login_concise(request, wordpress):
    
    user = C("wp.admin.name")
    pwd = C("wp.admin.pwd")
    
    # Login
    wordpress.user.text = user
    wordpress.pwd.text = pwd
    wordpress.submit.click()
    wordpress.view_site

    # Logout
    url = C("wp.logout.url")
    wordpress.go_to_url(url)
    wordpress.logout_confirm.click()
    wordpress.logout_msg
