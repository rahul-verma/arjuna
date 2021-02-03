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

class WordPress(GuiApp):

    def __init__(self):
        url = C("wp.login.url")
        super().__init__(url=url, gns_dir="gns_adv/app")
        self.launch()

    def login(self):
        user = C("wp.admin.name")
        pwd = C("wp.admin.pwd")

        # Login
        self.gns.user.text = user
        self.gns.pwd.text = pwd
        self.gns.submit.click()
        self.gns.view_site

    def logout(self):
        url = C("wp.logout.url")
        self.go_to_url(url)
        self.gns.logout_confirm.click()
        self.gns.logout_msg

        self.quit()

    def tweak_role_value_in_settings(self, value):
        self.app.gns.settings.click()
        role_select = self.gns.role
        role_select.select_value(value)
        self.asserter.assert_true(role_select.has_value_selected(value), "Selection of {} as Role".format(value))
        return self