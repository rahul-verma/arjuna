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

import unittest
import time

from arjuna import *

class WPBaseTest(unittest.TestCase):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        Arjuna.init("/Users/rahulverma/Documents/github_tm/arjuna/arjuna-samples/workspace/arjex")
        self.__config = Arjuna.get_ref_config()
        self.__app = None

    @property
    def wordpress(self):
        return self.__app

    @property
    def config(self):
        return self.__config

    def setUp(self):
        super().setUp()
        self.__app = WebApp(base_url=self.config.user_options.value("wp.login.url"))
        self.wordpress.launch()
        self.wordpress.ui.externalize(gns_dir="mgns_wordpress_singlefile", gns_file_name="WordPress.yaml")
        self.login_with_default_creds()

    def tearDown(self):
        self.logout()
        #self.app.automator.quit()

    def login_with_default_creds(self):
        user, pwd = self.config.user_options.value("wp.users.admin").split_as_str_list()

        # Login
        self.wordpress.ui.element(With.meta("login").format(RoLe="user")).text = user
        self.wordpress.ui.element(With.meta("password").format(roLE="user")).text = pwd
        self.wordpress.ui.element("submit").click()

        self.wordpress.ui.element("view_site").wait_until_visible()

    def logout(self):
        url = self.config.user_options.value("wp.logout.url")
        self.wordpress.ui.browser.go_to_url(url)

        self.wordpress.ui.element("logout_confirm").click()
        self.wordpress.ui.element("logout_msg").wait_until_visible()


class SimpleAppTest(WPBaseTest):

    def test_author_type_selection(self):
        self.wordpress.ui.element("Settings").click()

        role_select = self.wordpress.ui.dropdown("role")
        role_select.select_value("editor")

        self.assertEqual("editor", role_select.value, "Author type selection failed.")

unittest.main()