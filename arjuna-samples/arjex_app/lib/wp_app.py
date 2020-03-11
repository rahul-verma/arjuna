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
        url = C("wp.login.url")
        self.__app = WebApp(base_url=url, label="WordPress")
        self.app.launch()

    @property
    def app(self):
        return self.__app

    def login(self):
        user = C("wp.admin.name")
        pwd = C("wp.admin.pwd")

        # Login
        self.app.user.text = user
        self.app.pwd.text = pwd
        self.app.submit.click()
        self.app.view_site

    def logout(self):
        url = C("wp.logout.url")
        self.app.go_to_url(url)
        self.app.logout_confirm.click()
        self.app.logout_msg

        self.app.quit()

    def tweak_role_value_in_settings(self, value):
        self.app.settings.click()
        role_select = self.app.role
        role_select.select_value(value)
        self.app.asserter.assert_true(role_select.has_value_selected(value), "Selection of {} as Role".format(value))

