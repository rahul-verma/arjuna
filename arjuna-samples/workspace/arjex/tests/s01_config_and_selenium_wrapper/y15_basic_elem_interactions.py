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

from commons import *
from arjuna import *

init_arjuna()
wordpress = create_wordpress_app()

user, pwd = wordpress.config.get_user_option_value("wp.users.admin").split_as_str_list()

# Login
user_field = wordpress.ui.element(With.id("user_login"))
user_field.wait_until_clickable()
user_field.text = user

pwd_field = wordpress.ui.element(With.id("user_pass"))
pwd_field.wait_until_clickable()
pwd_field.text = pwd

submit = wordpress.ui.element(With.id("wp-submit"))
submit.wait_until_clickable()
submit.click()

wordpress.ui.element(With.class_name("welcome-view-site")).wait_until_visible()

# Logout
url = wordpress.ui.config.get_user_option_value("wp.logout.url").as_str()
wordpress.ui.browser.go_to_url(url)

confirmation = wordpress.ui.element(With.link_ptext("log out"))
confirmation.wait_until_clickable()
confirmation.click()

message = wordpress.ui.element(With.ptext("logged out"))
message.wait_until_visible()

wordpress.quit()