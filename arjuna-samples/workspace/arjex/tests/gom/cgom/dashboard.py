from .basepage import WPFullPage

class DashboardPage(WPFullPage):

    def go_to_settings(self):
        self.element("settings").click()
        return SettingsPage(self.app, self.automator)