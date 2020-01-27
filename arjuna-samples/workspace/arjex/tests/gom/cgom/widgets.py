from enum import Enum, auto
from arjuna import Widget

class WPBaseWidget(Widget):

    def __init__(self, page):
        super().__init__(page)
        self.externalize_guidef(ns_dir="{}_wordpress/widgets".format(self.app.gns_format.lower()))

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