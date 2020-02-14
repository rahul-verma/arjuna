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

def create_wordpress_app():
    url = Arjuna.get_ref_config().get_user_option_value("wp.login.url").as_str()
    wordpress = WebApp(base_url=url)
    wordpress.launch()
    wordpress.externalize(gns_file_name="WordPress.gns")
    return wordpress

def login(wordpress):
    user = wordpress.config.get_user_option_value("wp.admin.name").as_str()
    pwd = wordpress.config.get_user_option_value("wp.admin.pwd").as_str()

    # Login
    wordpress.element("login").text = user
    wordpress.element("pwd").text = pwd
    wordpress.element("submit").click()
    wordpress.element("view_site")

def logout(wordpress):
    url = wordpress.config.get_user_option_value("wp.logout.url").as_str()
    wordpress.go_to_url(url)
    wordpress.element("logout_confirm").click()
    wordpress.element("logout_msg")

    wordpress.quit()
