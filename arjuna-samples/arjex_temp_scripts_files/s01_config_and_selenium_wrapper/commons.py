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

def init_arjuna():
    return Arjuna.init("/Users/rahulverma/Documents/github_tm/arjuna/arjuna-samples/workspace/arjex")

def create_app():
    app = WebApp()
    app.launch(blank_slate=True)
    return app
    
def create_wordpress_app():
    url = Arjuna.get_ref_config().get_user_option_value("wp.login.url").as_str()
    wordpress = WebApp(base_url=url)
    wordpress.launch()
    return wordpress

def login():
    wordpress = create_wordpress_app()

    user, pwd = wordpress.config.get_user_option_value("wp.users.admin").split_as_str_list()

    # Login
    wordpress.ui.element(With.id("user_login")).text = user
    wordpress.ui.element(With.id("user_pass")).text = pwd
    wordpress.ui.element(With.id("wp-submit")).click()

    wordpress.ui.element(With.class_name("welcome-view-site")).wait_until_visible()
    return wordpress

def logout(wordpress):
    url = wordpress.config.get_user_option_value("wp.logout.url").as_str()
    wordpress.ui.browser.go_to_url(url)

    wordpress.ui.element(With.link_ptext("log out")).click()
    message = wordpress.ui.element(With.ptext("logged out")).wait_until_visible()

    wordpress.quit()
