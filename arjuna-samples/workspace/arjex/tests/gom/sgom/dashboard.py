from .basepage import WPBasePage
from .settings import SettingsPage

class DashboardPage(WPBasePage):

    def go_to_settings(self):
        self.element("settings").click()
        return SettingsPage(self.automator)