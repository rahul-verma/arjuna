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

class LeftNav1(WPBaseWidget):

    class labels(Enum):
        settings = auto()

    def __init__(self, page):
        super().__init__(page, With.id("adminmenu"))

    def validate_readiness(self):
        self.element(self.labels.settings)

class LeftNav2(WPBaseWidget):

    class labels(Enum):
        settings = auto()

    def __init__(self, page):
        super().__init__(page)

    def validate_readiness(self):
        self.element(self.labels.settings)

class LeftNav3(WPBaseWidget):

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
        url = self.config.user_options.value("wp.logout.url")
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
        print(RE_LOC)
        if RE_LOC == "coded":
            self.__left_nav = LeftNav1(self)
        elif RE_LOC == "gns":
            self.__left_nav = LeftNav2(self)
        elif RE_LOC == "both":
            self.__left_nav = LeftNav3(self)

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
        user = self.config.user_options.value("wp.admin.name")
        pwd = self.config.user_options.value("wp.admin.pwd")

        return self.login(user, pwd)

class Dashboard(WPFullPage):

    class labels(Enum):
        view_site = auto()

    def validate_readiness(self):
        self.element(self.labels.view_site).wait_until_visible()

def login():
    wordpress = WordPress()
    home = wordpress.launch()
    dashboard = home.login_with_default_creds()
    return dashboard

def logout(dashboard):
    dashboard.top_nav.logout()
    dashboard.app.quit()

@test
def check_widget_coded_re(request):
    '''
        Left Nav has root element passed in __init__.
        Top Nav does not have a root element.
    '''
    global RE_LOC
    RE_LOC = "coded" 
    dashboard = login()
    exc = None
    try:
        request.asserter.assert_equal('<div id="wpwrap"> </div>', dashboard.element(With.xpath("//div")).source.content.root, "Source of First div with Automator")
        request.asserter.assert_equal('<div class="wp-menu-arrow"/>', dashboard.left_nav.element(With.xpath("//div")).source.content.root, "Source of First div with Widget WITH Root")
        request.asserter.assert_equal('<div id="wpwrap"> </div>', dashboard.top_nav.element(With.xpath("//div")).source.content.root, "Source of First div with Widget WITHOUT Root")
    except Exception as e:
        exc = e
    finally:
        logout(dashboard)
        if exc:
            raise(exc)

@test
def check_widget_gns_re(request):
    '''
        Left Nav has root element defined in GNS.
        Top Nav does not have a root element.
    '''
    global RE_LOC
    RE_LOC = "gns" 
    dashboard = login()
    exc = None
    try:
        request.asserter.assert_equal('<div id="wpwrap"> </div>', dashboard.element(With.xpath("//div")).source.content.root, "Source of First div with Automator")
        request.asserter.assert_equal('<div class="wp-menu-arrow"/>', dashboard.left_nav.element(With.xpath("//div")).source.content.root, "Source of First div with Widget WITH Root")
        request.asserter.assert_equal('<div id="wpwrap"> </div>', dashboard.top_nav.element(With.xpath("//div")).source.content.root, "Source of First div with Widget WITHOUT Root")
    except Exception as e:
        exc = e
    finally:
        logout(dashboard)
        if exc:
            raise(exc)


@test
def check_widget_both_re(request):
    '''
        Left Nav has root element defined in GNS.
        Top Nav does not have a root element.
    '''
    global RE_LOC
    RE_LOC = "both" 
    dashboard = login()
    exc = None
    try:
        request.asserter.assert_equal('<div id="wpwrap"> </div>', dashboard.element(With.xpath("//div")).source.content.root, "Source of First div with Automator")
        request.asserter.assert_equal('<div class="wp-menu-arrow"/>', dashboard.left_nav.element(With.xpath("//div")).source.content.root, "Source of First div with Widget WITH Root")
        request.asserter.assert_equal('<div id="wpwrap"> </div>', dashboard.top_nav.element(With.xpath("//div")).source.content.root, "Source of First div with Widget WITHOUT Root")
    except Exception as e:
        exc = e
    finally:
        logout(dashboard)
        if exc:
            raise(exc)