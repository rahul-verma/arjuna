from arjuna.interact.gui.gom.invoker.gui import SimpleBaseWidget
from.mixnins import AsserterMixIn

GNS_FMT = None

class WPBaseWidget(SimpleBaseWidget, AsserterMixIn):

    def __init__(self, automator, parent):
        super().__init__(automator, parent, "{}_wordpress/widgets".format(GNS_FMT.lower()))


class LeftNavSideBar(WPBaseWidget):

    @property
    def settings(self):
        from .settings import SettingsPage
        self.element("settings").click()
        return SettingsPage(self.automator)

class TopNavBar(WPBaseWidget):

    def logout(self):
        url = self.config.get_user_option_value("wp.logout.url").as_str()
        self.browser.go_to_url(url)

        self.element("logout_confirm").click()
        self.element("logout_msg").wait_until_visible()