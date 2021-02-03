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

import unittest

from cgom.wordpress import WordPress

class WPBaseTest(unittest.TestCase):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.__app = None
        self.dashboard_page = None

    @property
    def app(self):
        return self.__app

    def setUp(self):
        self.__app = WordPress(gns_format="mgns")
        home = self.app.launch()
        self.dashboard_page = home.login_with_default_creds()

    def tearDown(self):
        self.dashboard_page.top_nav.logout()
        # self.automator.quit()

class CompositeGOMTest(WPBaseTest):

    def test_author_type_selection(self):
        self.dashboard_page.left_nav.settings.tweak_settings()

unittest.main()