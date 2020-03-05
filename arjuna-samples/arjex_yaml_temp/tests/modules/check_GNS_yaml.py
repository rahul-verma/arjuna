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

RE_LOC = None

class WordPress(WebApp):

    def __init__(self):
        url = C("wp.login.url")
        super().__init__(base_url=url)

    def launch(self):
        super().launch()
        return Home(self)

class WPBaseWidget(Widget, metaclass=abc.ABCMeta):

    def __init__(self, page, root_element_locator=None):
        super().__init__(page, root_element_locators=root_element_locator)

    def prepare(self):
        self.externalize(gns_dir="widgets")

class LoginForm(WPBaseWidget):

    class labels(Enum):
        login = auto()
        pwd = auto()
        submit = auto()

    def __init__(self, page):
        super().__init__(page)

    def login(self, user, pwd):
        self.element(self.labels.login).text = user
        self.element(self.labels.pwd).text = pwd
        self.element(self.labels.submit).click()

        return Dashboard(self)

    def login_with_default_creds(self):
        user = self.config.user_options.value("wp.admin.name")
        pwd = self.config.user_options.value("wp.admin.pwd")

        return self.login(user, pwd)

class WPBasePage(Page, metaclass=abc.ABCMeta):

    def __init__(self, source_gui):
        super().__init__(source_gui=source_gui)

    def prepare(self):
        self.externalize()

class Dashboard(WPBasePage):

    class labels(Enum):
        view_site = auto()

    def validate_readiness(self):
        self.element(self.labels.view_site).wait_until_visible()

class Home(WPBasePage):

    class labels(Enum):
        login = auto()
        pwd = auto()
        submit = auto()

    @property
    def login_form(self):
        return LoginForm(self)

def login():
    wordpress = WordPress()
    home = wordpress.launch()
    dashboard = home.login_form.login_with_default_creds()
    return dashboard

@test
def check_yaml(request):
    login()