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

from enum import Enum, auto
from arjuna import Widget

class WPBaseWidget(Widget):

    def __init__(self, page):
        super().__init__(page)
        self.externalize_def(ns_dir="{}_wordpress/widgets".format(self.app.gns_format.lower()))

class LeftNavSideBar(WPBaseWidget):

    class loc(Enum):
        settings = auto()

    @property
    def settings(self):
        from .settings import SettingsPage
        self.element(self.loc.settings).click()
        return SettingsPage(self)

class TopNavBar(WPBaseWidget):

    class loc(Enum):
        logout_confirm = auto()
        logout_msg = auto()

    def logout(self):
        url = self.config.get_user_option_value("wp.logout.url").as_str()
        self.browser.go_to_url(url)

        self.element(self.loc.logout_confirm).click()
        self.element(self.loc.logout_msg).wait_until_visible()

        from .home import HomePage
        return HomePage(self)