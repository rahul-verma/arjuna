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

class WordPress(WebApp):

    def __init__(self):
        url = Arjuna.get_ref_config().get_user_option_value("wp.login.url").as_str()
        super().__init__(base_url=url)

    def launch(self):
        super().launch()
        return Home(self)

class WPBaseWidget(Widget, metaclass=abc.ABCMeta):

    def __init__(self, page, root_element_locator=None):
        super().__init__(page, root_element_locators=root_element_locator)

    def prepare(self):
        self.externalize(gns_dir="widgets")

class LeftNav(WPBaseWidget):

    class labels(Enum):
        settings = auto()

    def __init__(self, page):
        super().__init__(page, With.id("adminmenu"))

    def validate_readiness(self):
        self.element(self.labels.settings)

class TopNav(WPBaseWidget):

    class labels(Enum):
        logout_confirm = auto()
        logout_msg = auto()

    def logout(self):
        url = self.config.get_user_option_value("wp.logout.url").as_str()
        self.go_to_url(url)

        self.element(self.labels.logout_confirm).click()
        self.element(self.labels.logout_msg).wait_until_visible()

        return Home(self)

class WPBasePage(Page, metaclass=abc.ABCMeta):

    def __init__(self, source_gui):
        super().__init__(source_gui=source_gui)

    def prepare(self):
        self.externalize()


class WPFullPage(WPBasePage, metaclass=abc.ABCMeta):

    def __init__(self, source_gui):
        super().__init__(source_gui=source_gui)
        self.__top_nav = TopNav(self)
        self.__left_nav = LeftNav(self)

    @property
    def top_nav(self):
        return self.__top_nav

    @property
    def left_nav(self):
        return self.__left_nav

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

        return Dashboard(self)

    def login_with_default_creds(self):
        user = self.config.get_user_option_value("wp.admin.name").as_str()
        pwd = self.config.get_user_option_value("wp.admin.pwd").as_str()

        return self.login(user, pwd)

class Dashboard(WPFullPage):

    class labels(Enum):
        view_site = auto()

    def validate_readiness(self):
        self.element(self.labels.view_site).wait_until_visible()

@for_test
def dashboard(request):
    # Setup
    wordpress = WordPress()
    home = wordpress.launch()
    dashboard = home.login_with_default_creds()
    yield dashboard

    # Teadown
    dashboard.top_nav.logout()

@test
def test_widget_root_element_working(my, request, dashboard):
    '''
        Left Nav has root element.
        Top Nav does not have a root element.
    '''
    print(dashboard.element(With.xpath("//div")).source.content.root)
    # For XPaths, the XPath needs to be preceded with a '.'
    print(dashboard.left_nav.element(With.xpath(".//div")).source.content.root)
    print(dashboard.top_nav.element(With.xpath("//div")).source.content.root)