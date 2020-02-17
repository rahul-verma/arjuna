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
from .base import WPBaseWidget

class TopNav(WPBaseWidget):

    class labels(Enum):
        logout_confirm = auto()
        logout_msg = auto()

    def logout(self):
        url = self.config.get_user_option_value("wp.logout.url").as_str()
        self.go_to_url(url)

        self.element(self.labels.logout_confirm).click()
        self.element(self.labels.logout_msg).wait_until_visible()

        from arjex_app_page_widget.lib.gom.pages.home import Home
        return Home(self)