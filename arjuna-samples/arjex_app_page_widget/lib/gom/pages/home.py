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
from .base import WPBasePage

class Home(WPBasePage):

    class labels(Enum):
        login = auto()
        pwd = auto()
        submit = auto()

    def validate_readiness(self):
        self.element(self.labels.submit).wait_until_visible()

    def login(self, user, pwd):
        self.element(self.labels.login).text = user
        self.element(self.labels.pwd).text = pwd
        self.element(self.labels.submit).click()

        from .dashboard import Dashboard
        return Dashboard(self)

    def login_with_default_creds(self):
        user = self.config.get_user_option_value("wp.admin.name")
        pwd = self.config.get_user_option_value("wp.admin.pwd")

        return self.login(user, pwd)


