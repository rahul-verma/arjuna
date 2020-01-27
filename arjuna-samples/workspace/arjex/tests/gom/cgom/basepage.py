from arjuna.interact.gui.gom import Page

from .widgets import *

class WPBasePage(Page):

    def __init__(self, app, automator):
        super().__init__(app, automator)
        self.externalize_guidef()

    def logout(self):
        url = self.config.get_user_option_value("wp.logout.url").as_str()
        self.browser.go_to_url(url)

        self.element("logout_confirm").click()
        self.element("logout_msg").wait_until_visible()
        from sgom.home import HomePage
        return HomePage(self.app, self._automator)

class WPFullPage(WPBasePage):

    def __init__(self, app, automator):
        super().__init__(app, automator)
        self.__top_nav = TopNavBar(self)
        self.__left_nav = LeftNavSideBar(self)

    @property
    def top_nav(self):
        return self.__top_nav

    @property
    def left_nav(self):
        return self.__left_nav

