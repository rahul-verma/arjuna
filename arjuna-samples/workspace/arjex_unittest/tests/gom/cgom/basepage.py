from arjuna.interact.gui.gom.invoker.gui import SimpleBaseGui

from.mixnins import AsserterMixIn
from .widgets import *

GNS_FMT = None

class WPBasePage(SimpleBaseGui, AsserterMixIn):

    def __init__(self, automator):
        super().__init__(automator, "{}_wordpress".format(GNS_FMT.lower()))

    def logout(self):
        url = self.config.get_user_option_value("wp.logout.url").as_str()
        self.browser.go_to_url(url)

        self.element("logout_confirm").click()
        self.element("logout_msg").wait_until_visible()

class WPFullPage(WPBasePage):

    def __init__(self, automator):
        super().__init__(automator)
        self.__top_nav = TopNavBar(self.automator, self)
        self.__left_nav = LeftNavSideBar(self.automator, self)

    @property
    def top_nav(self):
        return self.__top_nav

    @property
    def left_nav(self):
        return self.__left_nav

