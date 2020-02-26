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

class WordPress:

    def __init__(self):
        url = Arjuna.get_ref_config().get_user_option_value("wp.login.url")
        self.__app = WebApp(base_url=url)
        self.app.launch()
        self.app.externalize(gns_file_name="WordPress.yaml")

    @property
    def app(self):
        return self.__app

    def login(self):
        user = self.app.config.get_user_option_value("wp.admin.name")
        pwd = self.app.config.get_user_option_value("wp.admin.pwd")

        # Login
        self.app.element("login").text = user
        self.app.element("pwd").text = pwd
        self.app.element("submit").click()
        self.app.element("view_site")

    def logout(self):
        url = self.app.config.get_user_option_value("wp.logout.url")
        self.app.go_to_url(url)
        self.app.element("logout_confirm").click()
        self.app.element("logout_msg")

        self.app.quit()

    def tweak_role_value_in_settings(self, value):
        self.app.element("Settings").click()
        role_select = self.app.dropdown("role")
        role_select.select_value(value)
        self.app.asserter.assert_true(role_select.has_value_selected(value), "Selection of {} as Role".format(value))

